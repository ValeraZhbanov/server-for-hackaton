
# Надо сделать 
#    pip install flask, flask_sqlalchemy
#  Но так просто будет только если уже есть питон
import requests
from flask import Flask, current_app, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport = db.Column(db.String(4), nullable=False)
    railway_carriage = db.Column(db.Integer, nullable=False)
    place = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Passenger %r>' % self.id

    def to_json(self):
        return {
            "id":self.id,
            "passport":self.passport,
            "railway_carriage":self.railway_carriage,
            "place":self.place,
        }


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    total_travel_time = db.Column(db.Time, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    next_stop = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Route %r>' % self.id

    def to_json(self):
        return {
            "id":self.id,
            "departure_time":str(self.departure_time),
            "arrival_time":str(self.arrival_time),
            "total_travel_time":str(self.total_travel_time),
            "speed":self.speed,
            "next_stop":self.next_stop,
        }


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(15), nullable=False)
    icon = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Purchase %r>' % self.id

    def to_json(self):
        return {
            "id":self.id,
            "type":self.type,
            "name":self.name,
            "price":self.price,
            "icon":self.icon,
        }


class Entertainment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Entertainment %r>' % self.id

    def to_json(self):
        return {
            "id":self.id,
            "type":self.type,
            "name":self.name,
            "filename":self.filename,
        }


@app.route("/")
def index():
    res = requests.post('http://localhost:5000/login',json = {
        "passport":"124","railway_carriage":1,"place":2})
    return res.json()

@app.route("/login", methods=['POST'])
def login():
    _Json = request.get_json()
    print(_Json)
    return Passenger.query.filter_by(passport=_Json["passport"],railway_carriage=_Json["railway_carriage"],place=_Json["place"]).first().to_json()

@app.route("/passenger/<int:id>")
def passenger(id):
    return Passenger.query.get(id).to_json()

@app.route("/passengers")
def passengers():
    return jsonify([_Passenger.to_json() for _Passenger in Passenger.query.all()])

@app.route("/route/<int:id>")
def route(id):
    return Route.query.get(id).to_json()

@app.route("/routes")
def routes():
    return jsonify([_Route.to_json() for _Route in Route.query.all()])

@app.route("/purchase/<int:id>")
def purchase(id):
    return Purchase.query.get(id).to_json()

@app.route("/purchases")
def purchases():
    return jsonify([_Purchase.to_json() for _Purchase in Purchase.query.all()])

@app.route("/entertainment/<int:id>")
def entertainment(id):
    return Entertainment.query.get(id).to_json()

@app.route("/entertainments")
def entertainments():
    return jsonify([_Entertainment.to_json() for _Entertainment in Entertainment.query.all()])


def init_db():
    db.create_all()

    for _It in range(1, 20):
        _Passenger = Passenger()
        _Passenger.passport = str(1235 + _It)
        _Passenger.railway_carriage = _It
        _Passenger.place = _It * 2

        _Route = Route()
        _Route.departure_time = time(_It, 8, 24, 78915)
        _Route.arrival_time = time(_It, 8, 24, 78915)
        _Route.total_travel_time = time(_It, 8, 24, 78915)
        _Route.speed = 100 + _It
        _Route.next_stop = "Следующая остановка " + str(_It)

        _Purchase = Purchase()
        _Purchase.type = _It % 4
        _Purchase.name = "Товар " + str(_Purchase.type)
        _Purchase.price = _It * 100
        _Purchase.icon = "files/123hofhosfh32rh9wec" + str(_It)

        _Entertainment = Entertainment()
        _Entertainment.type = _It % 4
        _Entertainment.name = "Развлечение " + str(_It)
        _Entertainment.filename = "files/123hofhosfh32rh9wec" + str(_It) 

        db.session.add(_Passenger)
        db.session.add(_Route)
        db.session.add(_Purchase)
        db.session.add(_Entertainment)

    db.session.commit()

#init_db()

app.run(debug=True)