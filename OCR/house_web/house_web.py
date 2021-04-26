from flask import Flask
from flask import render_template
from flask import request
import webbrowser,json,os

app = Flask(__name__)

@app.route('/')
def index():
    data = "data.json"
    return render_template('index.html',data=data)


webbrowser.open('http://127.0.0.1:5000')
app.run()