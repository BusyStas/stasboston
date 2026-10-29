from flask import Flask, render_template, url_for, abort, request, jsonify, Response, stream_with_context
import json
import os
import re
import time
from collections import defaultdict, deque
from datetime import datetime, date

import job_agent
import talk_client

app = Flask(__name__ )

# Blog posts, newest first. Each post's body lives in templates/posts/<slug>.html.
POSTS = [
    {
        "slug": "ai-feature-trap",
        "title": "The AI Feature Trap: When Seat Licenses Meet Token Bills",
        "date": date(2026, 10, 28),
        "summary": "Adding AI is supposed to cut costs, but companies that ship it inside flat-priced products watch their bills grow with every click. Who has adjusted, who can't, and how to spot the next squeeze.",
    },
    {
        "slug": "digital-nomad-visas-us-citizens-2026",
        "title": "Digital Nomad Visas for US Citizens (2026)",
        "date": date(2026, 10, 26),
        "summary": "How digital nomad visas work for Americans who keep a US job or US clients, and how Spain, Portugal, Thailand, Panama, Estonia, Vietnam and Singapore compare.",
    },
    {
        "slug": "free-cloud-tiers",
        "title": "Hunting Freebies in the Clouds",
        "date": date(2026, 10, 25),
        "summary": "The permanent free tiers worth building on: Azure for a free SQL database, Google Cloud Run for web apps, AWS for serverless glue, plus Oracle and Cloudflare compared.",
    },
    {
        "slug": "invisible-wallet-business",
        "title": "The Invisible Wallet Business: Privy, Stripe and Who Owns the Rest",
        "date": date(2026, 10, 24),
        "summary": "The crypto wallets most people will use are ones they never see. Who builds them, who now owns them, and how fast Privy, the leader inside Stripe, is growing.",
    },
    {
        "slug": "phone-couldnt-buy-coffee",
        "title": "The Day My Phone Couldn't Buy a Coffee",
        "date": date(2026, 10, 23),
        "summary": "Field notes on paying abroad from Poland, Turkey and Moldova: where a good card stops working, why taxis need offline payments, and the travel app someone should build.",
    },
    {
        "slug": "write-code-on-solana",
        "title": "Everything You Need to Write Code on Solana",
        "date": date(2026, 10, 22),
        "summary": "What Solana is, what its programs can and can't do, and the toolkit to build them: Rust, Agave, Anchor, LiteSVM, Surfpool, Trident and verified builds.",
    },
    {
        "slug": "smartest-developer",
        "title": "Stop Telling Your Smartest Developer What to Do",
        "date": date(2026, 10, 10),
        "summary": "We hire smart people and AI for their judgment, then dictate every decision. Give them the outcome, the constraints and the definition of done instead.",
    },
    {
        "slug": "ai-price-collapse",
        "title": "Will AI Make Everything Cheaper? Who Wins, Who Loses",
        "date": date(2026, 10, 4),
        "summary": "AI is collapsing the price of thinking work, but not of land, licenses or physical labor. The investing question is who keeps the savings.",
    },
]
for _post in POSTS:
    _post["date_label"] = f'{_post["date"]:%B} {_post["date"].day}, {_post["date"].year}'
    with open(os.path.join(app.root_path, 'templates', 'posts', f'{_post["slug"]}.html'), encoding='utf-8') as _f:
        _post["word_count"] = len(re.sub(r'<[^>]+>', ' ', _f.read()).split())
    _post["read_minutes"] = max(1, round(_post["word_count"] / 230))

@app.route('/')
def index():
    return render_template('index.html', posts=POSTS, pitch_enabled=job_agent.configured(),
                           talk_enabled=talk_client.configured())

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=POSTS)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in POSTS if p["slug"] == slug), None)
    if post is None:
        abort(404)
    more_posts = [p for p in POSTS if p is not post][:3]
    return render_template('blog_post.html', post=post, more_posts=more_posts)

@app.route('/pitch-a-job')
def pitch_a_job():
    return render_template('pitch_a_job.html')

@app.route('/health/warm-up')
def warm_up():
    """Background ping from the pitch page: starts the paused database resuming. Always 200."""
    response = jsonify(job_agent.warm_up())
    response.headers['Cache-Control'] = 'no-store'
    return response

# Each pitch costs a Claude call, so one visitor gets a handful per hour.
# In memory per instance: enough to stop a stuck button or a casual script.
PITCH_LIMIT, PITCH_WINDOW_SECONDS = 5, 3600
_pitches = defaultdict(deque)

def _rate_limited(ip: str) -> bool:
    now = time.monotonic()
    hits = _pitches[ip]
    while hits and now - hits[0] > PITCH_WINDOW_SECONDS:
        hits.popleft()
    if len(hits) >= PITCH_LIMIT:
        return True
    hits.append(now)
    return False

@app.route('/pitch-a-job', methods=['POST'])
def pitch_a_job_submit():
    data = request.get_json(silent=True) or {}
    if data.get('website'):  # honeypot field, invisible to people
        return jsonify(error='Rejected.'), 400

    name = (data.get('name') or '').strip()[:200]
    contact = (data.get('contact') or '').strip()[:500]
    position = (data.get('position') or '').strip()[:60000]
    url = (data.get('url') or '').strip()[:1000]

    if not name or not contact:
        return jsonify(error='Please tell me your name and how to reach you.'), 400
    if len(position) < 40:
        return jsonify(error='Please paste a bit more about the job so my AI agent has something to read.'), 400
    if url and not re.match(r'^https?://', url):
        url = 'https://' + url
    if url and not re.match(r'^https?://\S+$', url):
        return jsonify(error="That job URL doesn't look right."), 400
    if data.get('consent') is not True:
        return jsonify(error='Please confirm the storage notice first.'), 400

    ip = (request.headers.get('X-Forwarded-For') or request.remote_addr or '').split(',')[0].strip()
    if _rate_limited(ip):
        return jsonify(error="You've sent several jobs already. Please try again in an hour."), 429

    try:
        return jsonify(job_agent.evaluate_offer(name, contact, position, url))
    except job_agent.AgentError as e:
        return jsonify(error=str(e)), 502

@app.route('/talk')
def talk():
    return render_template('talk.html', talk_enabled=talk_client.configured())

# Talk to me: the browser calls these two, and they forward to the API with
# its key. The daily limit, the bot checks and the saving all happen there.
TALK_BODY_LIMIT = 4096
TALK_OFFLINE = {'code': 'Offline', 'message': "Mia is offline right now. Please reach out on LinkedIn instead."}

def _talk_json(upstream) -> Response:
    """The API's JSON answer, passed through with its status code."""
    response = Response(upstream.content, status=upstream.status_code,
                        mimetype=upstream.headers.get('Content-Type', 'application/json'))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/api/talk/status')
def talk_status():
    try:
        return _talk_json(talk_client.status())
    except talk_client.TalkUnavailable:
        return jsonify(TALK_OFFLINE), 503

@app.route('/api/talk/ask', methods=['POST'])
def talk_ask():
    if (request.content_length or 0) > TALK_BODY_LIMIT or len(request.get_data()) > TALK_BODY_LIMIT:
        return jsonify(code='BodyTooLarge', message='That request is too large.'), 413
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(code='BadRequest', message='Expected a JSON body.'), 400

    visitor = {
        'ip': (request.headers.get('X-Forwarded-For') or request.remote_addr or '').split(',')[0].strip(),
        'user_agent': request.headers.get('User-Agent', '')[:500],
        'referrer': request.headers.get('Referer', '')[:1000],
        'origin': request.headers.get('Origin', '')[:200],
    }
    try:
        upstream = talk_client.ask(data, visitor, request.headers.get('X-Talk-Admin-Token', ''))
    except talk_client.TalkUnavailable:
        return jsonify(TALK_OFFLINE), 503

    if not upstream.headers.get('Content-Type', '').startswith('text/event-stream'):
        return _talk_json(upstream)

    def relay():
        try:
            for chunk in upstream.iter_content(chunk_size=None):
                yield chunk
        finally:
            upstream.close()

    response = Response(stream_with_context(relay()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Accel-Buffering'] = 'no'
    return response

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/trip')
def trip():
    with open('templates/trips/jul26/trip_jul26.json', 'r') as f:
        schedule = json.load(f)
    for day in schedule:
        try:
            date_obj = datetime.strptime(day["date"], "%B %d, %Y")
            weekday = date_obj.strftime("%A")
            day["date_with_weekday"] = f'{day["date"]} ({weekday})'
        except Exception:
            day["date_with_weekday"] = day["date"]
    return render_template('trips/jul26/trip_july26.html', schedule=schedule)

@app.route('/trip/day/<day_id>')
def trip_day(day_id):
    day_templates = {
        'jul23': 'trips/jul26/day_jul23.html',
        'jul24': 'trips/jul26/day_jul24.html',
        'jul28': 'trips/jul26/day_jul28.html',
        'jul29': 'trips/jul26/day_jul29.html',
        'aug4': 'trips/jul26/day_aug4.html',
        'aug5': 'trips/jul26/day_aug5.html',
        'aug6': 'trips/jul26/day_aug6.html',
        'aug7': 'trips/jul26/day_aug7.html',
        'aug9': 'trips/jul26/day_aug9.html',
    }
    template = day_templates.get(day_id)
    if template:
        return render_template(template)
    from flask import redirect
    return redirect('/trip')

@app.route('/trip/2025')
def trip_2025():
    with open('templates/trips/aug25/trip_aug25.json', 'r') as f:
        schedule = json.load(f)
    # Add weekday to date string
    for day in schedule:
        try:
            date_obj = datetime.strptime(day["date"], "%B %d, %Y")
            weekday = date_obj.strftime("%A")
            day["date_with_weekday"] = f'{day["date"]} ({weekday})'
        except Exception:
            day["date_with_weekday"] = day["date"]
    return render_template('trips/aug25/trip_sofia_2025.html', schedule=schedule)

 
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Pages search engines are pointed at. The trip itineraries stay reachable by
# link but are left out: they are plans for friends, not pages to be found
SITE_URL = 'https://stas.boston'

@app.context_processor
def inject_site_urls():
    """Canonical address of the current page, always on stas.boston, so search
    engines don't index the run.app copy of the same page."""
    return {'site_url': SITE_URL, 'canonical_url': SITE_URL + request.path}

@app.route('/feed.xml')
def feed_xml():
    """Atom feed of the blog, for feed readers and aggregators."""
    def esc(text):
        return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                .replace('"', '&quot;'))
    updated = f"{POSTS[0]['date'].isoformat()}T12:00:00Z" if POSTS else '2026-01-01T00:00:00Z'
    entries = ''.join(
        f"""  <entry>
    <title>{esc(p['title'])}</title>
    <link href="{SITE_URL}{url_for('blog_post', slug=p['slug'])}"/>
    <id>{SITE_URL}{url_for('blog_post', slug=p['slug'])}</id>
    <published>{p['date'].isoformat()}T12:00:00Z</published>
    <updated>{p['date'].isoformat()}T12:00:00Z</updated>
    <summary>{esc(p['summary'])}</summary>
  </entry>
""" for p in POSTS)
    body = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Stanislav Prikhodko: Thoughts on AI, Crypto and Money</title>
  <link href="{SITE_URL}{url_for('blog')}"/>
  <link rel="self" href="{SITE_URL}/feed.xml"/>
  <id>{SITE_URL}{url_for('blog')}</id>
  <updated>{updated}</updated>
  <author><name>Stanislav Prikhodko</name><uri>{SITE_URL}/</uri></author>
{entries}</feed>
"""
    return Response(body, mimetype='application/atom+xml')

@app.route('/robots.txt')
def robots_txt():
    body = ("User-agent: *\n"
            "Allow: /\n"
            "Disallow: /health/\n"
            "Disallow: /api/\n"
            "\n"
            f"Sitemap: {SITE_URL}/sitemap.xml\n")
    return Response(body, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    pages = [(url_for('index'), None), (url_for('blog'), POSTS[0]['date'] if POSTS else None)]
    pages += [(url_for('blog_post', slug=p['slug']), p['date']) for p in POSTS]
    pages += [(url_for('pitch_a_job'), None), (url_for('talk'), None), (url_for('shop'), None),
              (url_for('privacy'), None)]
    entries = ''.join(
        f"  <url><loc>{SITE_URL}{path}</loc>"
        + (f"<lastmod>{d.isoformat()}</lastmod>" if d else '')
        + "</url>\n"
        for path, d in pages)
    body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + entries + '</urlset>\n')
    return Response(body, mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True)
