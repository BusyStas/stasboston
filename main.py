from flask import Flask, render_template, url_for

app = Flask(__name__)

# Define the root route to serve the index.html
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
