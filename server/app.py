from flask import Flask, make_response
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
@app.route("/earthquakes/<int:id>")
def fliter_earthquake_by_id(id):
    
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake:
        body= earthquake.to_dict()
        status=200
    else:
        body={"message": f"Earthquake {id} not found"}
        status=404

    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quake_data = []
    for earthquake in db.session.query(Earthquake).filter_by(magnitude=magnitude).all():
        quake_data.append(earthquake.to_dict())
        body= {"count": len(quake_data), "results": quake_data}
    return make_response (body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
