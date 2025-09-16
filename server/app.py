# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return jsonify(body), 200



# Add views 
@app.route('/earthquakes', methods=['GET'])
def earthquakes():
    data = get_earthquake_data()  # fetch from your function
    if not data:
        return jsonify({"earthquakes": [], "count": 0, "message": "Earthquake not found"}), 404

    return jsonify({
        "earthquakes": data,
        "count": len(data)
    }), 200

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        body = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        return jsonify(body), 200
    else:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    body = [{
        'id': eq.id,
        'magnitude': eq.magnitude,
        'location': eq.location,
        'year': eq.year
    } for eq in earthquakes]

    return jsonify({
        'quakes': body,
        'count': len(body)
    }), 200




if __name__ == '__main__':
    app.run(port=5555, debug=True)
