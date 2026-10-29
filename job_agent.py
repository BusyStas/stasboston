"""Client for the PersonalAssistants API (api-PersonalAssistants), used by the
"Pitch me a job" page.

The API key stays on this server: the browser only ever talks to stas.boston,
which calls the API with the X-API-Key header.

Configuration (Cloud Run environment variables):
    PA_API_URL   e.g. https://personalassistants-api-xxxxx.us-east1.run.app
    PA_API_KEY   this site's key from the personalassistants-api-keys secret
    PA_WHOSE_JOB_FINDER_TO_USE   Stanislav's UserId in PersonalAssistants: the API
                                 serves many users, and this picks whose Job Finder
                                 (profile, weights, saved jobs) a pitch is scored
                                 against and saved to
"""
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

API_URL = os.environ.get('PA_API_URL', '').rstrip('/')
API_KEY = os.environ.get('PA_API_KEY', '')
USER_ID = int(os.environ.get('PA_WHOSE_JOB_FINDER_TO_USE', '').strip() or 0)

# The API refuses a posting without a web address. When the visitor declines
# to give one, the posting is filed under this page and the notes say so.
NO_URL_SOURCE = 'https://stas.boston/pitch-a-job'

# A warm-up knock gives up after ~5s on the API side; this only has to outlast it.
WARMUP_TIMEOUT = 8
# One Claude call, plus a database that may still be resuming.
ANALYZE_TIMEOUT = 240
DEFAULT_TIMEOUT = 60


class AgentError(Exception):
    """A failure worth showing the visitor as a plain sentence."""


def configured() -> bool:
    return bool(API_URL and API_KEY and USER_ID)


def _call(method: str, path: str, timeout: int = DEFAULT_TIMEOUT, **kwargs):
    response = requests.request(method, f'{API_URL}{path}', timeout=timeout,
                                headers={'X-API-Key': API_KEY}, **kwargs)
    response.raise_for_status()
    return response.json() if response.content else None


def warm_up() -> dict:
    """Knock on the database so it is resuming before the visitor submits. Never raises."""
    if not configured():
        return {'warm': False, 'status': 'not_configured'}
    try:
        payload = _call('GET', '/api/v1/db-warmup', timeout=WARMUP_TIMEOUT) or {}
        return {'warm': bool(payload.get('warm')), 'status': payload.get('status')}
    except requests.exceptions.Timeout:
        return {'warm': False, 'status': 'timeout'}
    except (requests.exceptions.RequestException, ValueError) as e:
        logger.warning(f'Database warm-up ping failed: {e}')
        return {'warm': False, 'status': 'unreachable'}


def _sender_notes(name: str, contact: str, url_given: bool) -> str:
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [f'Pitched via stas.boston on {stamp}',
             f'From: {name}',
             f'Contact: {contact}']
    if not url_given:
        lines.append('No job URL was shared.')
    return '\n'.join(lines)[:4000]


def evaluate_offer(name: str, contact: str, position: str, url: str) -> dict:
    """Analyse a pitched job, save it with the sender in its notes, and rank it
    against every other posting already saved.

    Returns {match_rank, better_than (0-100 or None), compared_with, title, company}.
    """
    if not configured():
        raise AgentError('My AI agent is offline right now. Please reach out on LinkedIn instead.')

    source_url = url or NO_URL_SOURCE
    try:
        analysis = _call('POST', '/api/v1/jobs/postings/analyze', timeout=ANALYZE_TIMEOUT, json={
            'user_id': USER_ID, 'raw_text': position, 'source_url': source_url})

        saved = _call('POST', '/api/v1/jobs/postings', json={
            'user_id': USER_ID,
            'raw_text': position,
            'source_url': source_url,
            'fields': analysis['fields'],
            'scores': analysis['scores'],
            'targets': analysis['targets'],
            'ai_model': analysis.get('ai_model'),
            # Shows on Job Openings as pitched by a visitor (the API also
            # marks anything saved with this site's key that way)
            'source': 'Pitch',
        })
        posting_id = saved['job_posting_id']

        _call('PATCH', f'/api/v1/jobs/postings/{posting_id}', json={
            'user_id': USER_ID, 'field_name': 'Notes',
            'notes': _sender_notes(name, contact, bool(url))})

        postings = _call('GET', '/api/v1/jobs/postings', params={'user_id': USER_ID}) or []
    except requests.exceptions.Timeout:
        raise AgentError('My AI agent took too long to answer. Please try again in a minute.')
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.error(f'Job offer evaluation failed: {e}')
        raise AgentError('Something went wrong while my AI agent was reading the job. Please try again.')

    rank = int(analysis.get('match_rank') or 0)
    others = [int(p.get('match_rank') or 0) for p in postings if p.get('job_posting_id') != posting_id]
    better_than = round(100 * sum(r < rank for r in others) / len(others)) if others else None

    fields = analysis.get('fields') or {}
    return {
        'match_rank': rank,
        'better_than': better_than,
        'compared_with': len(others),
        'title': fields.get('title'),
        'company': fields.get('company'),
    }
