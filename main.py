from flask import Flask, render_template, url_for, abort
import json
from datetime import datetime, date

app = Flask(__name__ )

# Blog posts, newest first. Each post's body lives in templates/posts/<slug>.html.
POSTS = [
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

@app.route('/')
def index():
    return render_template('index.html', posts=POSTS)

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=POSTS)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in POSTS if p["slug"] == slug), None)
    if post is None:
        abort(404)
    return render_template('blog_post.html', post=post)

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

 

if __name__ == '__main__':
    app.run(debug=True)
