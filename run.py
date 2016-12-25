from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello there</h1>'

@app.route('/home')
def home():
    return render_template('home_page.html')

if __name__ == '__main__':
    app.run(debug=True)