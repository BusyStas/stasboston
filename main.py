from flask import Flask, render_template, url_for
import json

app = Flask(__name__ )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/trip')
def trip():
    with open('trips/aug25/trip_aug25.json', 'r') as f:
        schedule = json.load(f)
    return render_template('trips/aug25/schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
            "steps": [
                {"time": "15:00", "name": "Arrive at airport", "url": "https://www.massport.com/logan-airport"},
                {"time": "17:30", "name": "Flight LX53 departs", "url": "https://www.swiss.com"},
            ]
        },
        {
            "date": "August 1, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Arrival at 7:00 AM, transfer to hotel",
            "steps": [
                {"time": "07:00", "name": "Arrive in Zurich", "url": "https://www.flughafen-zuerich.ch"},
                {"time": "08:00", "name": "Transfer to hotel", "url": "https://www.hotel-example.com"},
            ]
        },
        {
            "date": "August 2, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Free day in Zurich",
            "steps": [
                {"time": "10:00", "name": "Explore Old Town", "url": "https://www.zuerich.com/en/visit/old-town"},
                {"time": "13:00", "name": "Lunch at Zeughauskeller", "url": "https://www.zeughauskeller.ch"},
            ]
        },
        {
            "date": "August 3, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Day trip to Lucerne",
            "steps": [
                {"time": "09:00", "name": "Train to Lucerne", "url": "https://www.sbb.ch"},
                {"time": "10:00", "name": "Walk Chapel Bridge", "url": "https://www.luzern.com/en/"},
            ]
        },
        {
            "date": "August 4, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Visit museums",
            "steps": [
                {"time": "11:00", "name": "Swiss National Museum", "url": "https://www.landesmuseum.ch"},
                {"time": "15:00", "name": "Kunsthaus Zürich", "url": "https://www.kunsthaus.ch"},
            ]
        },
        # ...add more days up to August 17...
    ]
    return render_template('trips/aug25/schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
