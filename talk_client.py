"""Client for "Talk to me", the chat with Mia on /talk, served by the
PersonalAssistants API (api-PersonalAssistants).

The browser only ever talks to stas.boston. This server forwards its two calls
with the X-API-Key header, so neither that key nor the Anthropic key ever
reaches the browser, and adds what it saw of the visitor (IP, user agent,
referrer, Origin): the API applies its bot checks and hashes the IP from these,
and never sees the raw request.

Configuration: the same PA_API_URL and PA_API_KEY as the "Pitch me a job" page,
and the same PA_WHOSE_JOB_FINDER_TO_USE: Stanislav's UserId, which picks whose
assistant answers - her name and what she knows are edited on contentedwife.com
under Avatar Agent. Without it the API answers from its built-in text.
"""
import logging

import requests

from job_agent import API_KEY, API_URL, USER_ID

logger = logging.getLogger(__name__)

# A paused database can take most of a minute to resume on the first call
STATUS_TIMEOUT = 75
# (connect, gap between streamed chunks): an answer starts within seconds,
# but the first call of the day may wait for the database as well
ASK_TIMEOUT = (10, 90)

# Only these fields of the browser's request are passed on; the visitor's
# details are filled in here, never taken from the browser
ASK_FIELDS = ('chat_id', 'question', 'page_token', 'signals')


class TalkUnavailable(Exception):
    """The API could not be reached, or is not configured here."""


def configured() -> bool:
    return bool(API_URL and API_KEY)


def status() -> requests.Response:
    if not configured():
        raise TalkUnavailable('not configured')
    try:
        return requests.get(f'{API_URL}/api/v1/talk/status', timeout=STATUS_TIMEOUT,
                            params={'owner_user_id': USER_ID} if USER_ID else None,
                            headers={'X-API-Key': API_KEY})
    except requests.exceptions.RequestException as e:
        logger.warning(f'Talk status failed: {type(e).__name__}: {e}')
        raise TalkUnavailable(str(e)) from e


def ask(data: dict, visitor: dict, admin_token: str = '') -> requests.Response:
    """Forward one question. The response streams: read it with iter_content."""
    if not configured():
        raise TalkUnavailable('not configured')
    body = {k: data.get(k) for k in ASK_FIELDS if k in data}
    body['visitor'] = visitor
    if USER_ID:
        body['owner_user_id'] = USER_ID
    headers = {'X-API-Key': API_KEY, 'Accept': 'text/event-stream'}
    if admin_token:
        headers['X-Talk-Admin-Token'] = admin_token
    try:
        return requests.post(f'{API_URL}/api/v1/talk/ask', json=body, headers=headers,
                             timeout=ASK_TIMEOUT, stream=True)
    except requests.exceptions.RequestException as e:
        logger.warning(f'Talk ask failed: {type(e).__name__}: {e}')
        raise TalkUnavailable(str(e)) from e
