from flask import Flask, render_template, url_for

app = Flask(__name__ )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/trip')
def trip():
    schedule = [
        {
            "date": "July 31, 2025",
            "location": "Boston",
            "address": "Logan International Airport, Terminal E",
            "flight": "LX53",
            "details": "Departure to Zurich at 5:30 PM"
        },
        {
            "date": "August 1, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Arrival at 7:00 AM, transfer to hotel"
        },
        {
            "date": "August 2, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Arrival at 7:00 AM, transfer to hotel"
        },
        {
            "date": "August 3, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Arrival at 7:00 AM, transfer to hotel"
        },
        {
            "date": "August 4, 2025",
            "location": "Zurich",
            "address": "Zurich Airport",
            "flight": "LX53",
            "details": "Arrival at 7:00 AM, transfer to hotel"
        },
        # ...add more days up to August 17...
    ]
    return render_template('trips/aug25/schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
