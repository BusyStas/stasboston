from flask import Flask, render_template, url_for
import json
from datetime import datetime

app = Flask(__name__ )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/trip')
def trip():
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
