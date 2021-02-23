import http.server
import socketserver

from flask import Flask
from flask.templating import render_template

import dilate
# dilate.dilateImage()

PORT = 8080

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<title>')
def hello(title):
    return render_template('index.html', title=title)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
