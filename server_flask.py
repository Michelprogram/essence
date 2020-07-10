from flask import Flask,render_template
from OBJ_Essence import find_station
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")
