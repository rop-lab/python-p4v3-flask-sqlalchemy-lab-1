from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database to get earthquakes with magnitude greater than or equal to the provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_data = [{
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    } for quake in earthquakes]

    # Return a JSON response with count of matching earthquakes and their data
    return jsonify({
        "count": len(earthquakes),
        "quakes": quake_data
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
