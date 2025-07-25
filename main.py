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
    return render_template('trips/aug25/trip_sofia_2025.html', schedule=schedule)

 

if __name__ == '__main__':
    app.run(debug=True)
