"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    try:
        characters = People.query.all()
        new_character_list = []
        for character in characters:
            new_character_list.append(character.serialize())
        return jsonify(new_character_list), 200
    except:
        return jsonify({'message': 'Server error'}), 500

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    try:
        character = People.query.get(people_id)
        if character:
            return jsonify(character.serialize()), 200
        else:
            return jsonify({"message": "Character not found"}), 404
    except:
        return jsonify({"message": "Server error"}), 500

@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets = Planets.query.all()
        new_planets_list = []
        for planet in planets:
            new_planets_list.append(planet.serialize())
        return jsonify(new_planets_list), 200
    except:
        return jsonify({"message": "Server error"}), 500


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    try:
        planet = Planets.query.get(planet_id)
        if planet:
            return jsonify(planet.serialize()), 200
        else:
            return jsonify({"message": "Planet not found"}), 404
    except:
        return jsonify({"message": "Server error"}), 500

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        machines = Vehicles.query.all()
        new_machines_list = []
        for machine in machines:
            new_machines_list.append(machine.serialize())
        return jsonify(new_machines_list), 200
    except:
        return jsonify({"message": "Server error"}), 500


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_single_vehicle(vehicle_id):
    try:
        machine = Vehicles.query.get(vehicle_id)
        if machine:
            return jsonify(machine.serialize()), 200
        else:
            return jsonify({"message": "Vehicle not found"}), 404
    except:
        return jsonify({"message": "Server error"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        starwars_fans = User.query.all()
        new_starwars_fans_list = []
        for starwars_fan in starwars_fans:
            new_starwars_fans_list.append(starwars_fan.serialize())
        return jsonify(new_starwars_fans_list), 200
    except:
        return jsonify({'message': 'Server error'}), 500


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    try:
        # Suponiendo que el usuario actual está autenticado y su ID se obtiene de alguna manera
        user_id = request.args.get('user_id')  # Aquí deberías obtener el ID del usuario actual de alguna manera
        print(user_id)
        # Buscar todos los favoritos del usuario actual
        user_favorites = Favorites.query.filter_by(user_id=user_id).all()

        # Serializar los resultados
        serialized_favorites = [favorite.serialize() for favorite in user_favorites]

        return jsonify(serialized_favorites), 200
    except:
        return jsonify({'message': 'Server error'}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
