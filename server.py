import os

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, Markup, request
from flask_socketio import SocketIO, emit

from yelp_query import yelper
 yelp = yelper()

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

socketio = SocketIO(app)

@app.context_processor
def getVars():
    return {
        "owner": "UMW Goats",
        "now": datetime.now()
    }

@socketio.on("search", namespace="/socketio")
def search(query):
    emit("addResult", "result")

@app.route('/getRestaurants', methods=['GET', 'POST'])
def restaurants():
    data = [
            {'value':'30','content':'1 ' + Markup('<span class="fa fa-star"></span>')},
            {'value':'10','content':'2 ' + Markup(' <span class="fa fa-star"></span><span class="fa fa-star"></span>')},
            {'value':'5','content':'3 ' + Markup('<span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span>')},
            {'value':'20','content':'4 ' + Markup('<span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span>')},
            {'value':'40','content':'5 ' + Markup('<span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span>')}
           ]

    overall = 40
    location = 'Brooklyn+Bridge,New+York,NY';
    return render_template('charts.html', data = data, overall = overall)

@app.route("/", methods=['GET', 'POST'])
def mainIndex():
    if request.method == 'POST':
        category = request.form['category']

        if category == 'restaurant':
            data = getRestaurant(location);

        elif category == 'shopping':
            data = getShopping(location);

        elif category == 'nightlife':
            data = getNightLife(location);

        elif category == 'travel':
            data = getTravel(location);

        elif category == 'housing':
            data = getHousing(location);

        elif category == 'safety':
            data = getSafety(location);

        else:
            data = [
                    {'value':'10','content':'1 ' + Markup('<span class="fa fa-star"></span>')},
                    {'value':'20','content':'2 ' + Markup(' <span class="fa fa-star"></span><span class="fa fa-star"></span>')},
                    {'value':'30','content':'3 ' + Markup('<span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span>')},
                    {'value':'20','content':'4 ' + Markup('<span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span>')},
                    {'value':'10','content':'5 ' + Markup('<span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span>')}
                    ]

    qualityOfLife = getQuality(location);


    locationMapFormat = 'Brooklyn+Bridge,New+York,NY';

    return render_template('charts.html', livingQuality=qualityOfLife, buttons=buttonItems, data = data, location = locationMapFormat)


if __name__ == "__main__":
    socketio.run(app, host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
