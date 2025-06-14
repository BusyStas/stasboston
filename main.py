from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/trip')
def trip():
    return render_template('trips/aug25/trip_zurich_2025.html')

if __name__ == '__main__':
    app.run(debug=True)
