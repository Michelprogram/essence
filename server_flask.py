from flask import Flask,render_template,request,url_for,redirect,jsonify
from json import loads
from OBJ_Essence import *
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        try:
            carburant = request.form["Gazole"]

        except KeyError:
            pass

        try:
            carburant = request.form["SP98"]
        except KeyError:
            pass

        try:
            carburant = request.form["SP95"]
        except KeyError:
            pass

        essence = Essence(carburant,request.form["Longitude"],request.form["Latitude"])
        essence.find_station()

        return redirect(url_for("map",long=essence.longitude,latt=essence.latitude))

    return render_template("index.html")

@app.route('/map<float:long><float:latt>')
def map(long,latt):
    return render_template("map.html",longittude=long,lattitude=latt)

@app.route("/data")
def data():
    with open("data.json","r",encoding="utf8") as json_file:
        data = loads(json_file.read())
    return jsonify(data)
