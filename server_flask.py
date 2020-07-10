from flask import Flask,render_template,request,url_for,redirect
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

        essence = Essence(carburant)
        essence.find_station()

        return redirect(url_for("map"))

    return render_template("index.html")

@app.route('/map')
def map():
    print("salut")
    return render_template("map.html")
