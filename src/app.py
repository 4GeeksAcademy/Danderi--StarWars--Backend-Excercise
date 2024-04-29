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
        user_id = request.args.get('user_id')  # Se debe asignar un params desde el postman con el id del user que tiene favoritos
        
        user_favorites = Favorites.query.filter_by(user_id=user_id).all() # Buscar todos los favoritos del usuario actual
        
        serialized_favorites = [favorite.serialize() for favorite in user_favorites] # Serializar los resultados

        return jsonify(serialized_favorites), 200
    except:
        return jsonify({'message': 'Server error'}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])  
def add_fav_planet(planet_id):
        try:
            user_id = request.args.get('user_id')
            existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()

            if existing_favorite:
                return jsonify({"message": "Is already a favorite planet of the user"}), 400
            
            planet = Planets.query.get(planet_id)
            if not planet:
                return jsonify({"message": "Planet does not exist"}), 404
            
            new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"message": "Planet set as favorite"}), 200

        except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
        try:
            user_id = request.args.get('user_id')
            existing_favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()

            if existing_favorite:
                return jsonify({"message": "Is already a favorite people of the user"}), 400
            
            people = People.query.get(people_id)
            if not people:
                return jsonify({"message": "People does not exist"}), 404
            
            new_favorite = Favorites(user_id=user_id, people_id=people_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"message": "people set as favorite"}), 200

        except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_fav_vehicles(vehicle_id):
        try:
            user_id = request.args.get('user_id')
            existing_favorite = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

            if existing_favorite:
                return jsonify({"message": "Is already a favorite vehicle of the user"}), 400
            
            vehicle = Vehicles.query.get(vehicle_id)
            if not vehicle:
                return jsonify({"message": "Vehicle does not exist"}), 404
            
            new_favorite = Favorites(user_id=user_id, vehicle_id=vehicle_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"message": "vehicles set as favorite"}), 200

        except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    try:
        user_id = request.args.get('user_id')
        favorite_to_delete = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        
        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
            return jsonify({"message": "Favorite Planet deleted"}), 200
        else:
            return jsonify({"message": "Favorite Planet not found"}), 404
    
    except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    try:
        user_id = request.args.get('user_id')
        favorite_to_delete = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
        
        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
            return jsonify({"message": "Favorite People deleted"}), 200
        else:
            return jsonify({"message": "Favorite People not found"}), 404
    
    except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(vehicle_id):
    try:
        user_id = request.args.get('user_id')
        favorite_to_delete = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
        
        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
            return jsonify({"message": "Favorite Vehicle deleted"}), 200
        else:
            return jsonify({"message": "Favorite Vehicle not found"}), 404
    
    except Exception as e:
            print(str(e))
            return jsonify({"message": "Server error"}), 500


@app.route('/create/planet/', methods=['POST'])
def create_planet():
    try:
        data = request.json
        
        if 'name' not in data:
            return jsonify({"message": "Missing required field: name"}), 400
        
        new_planet = Planets(
            name=data.get('name'),
            gravity=data.get('gravity'),
            population=data.get('population'),
            climate=data.get('climate'),
            diameter=data.get('diameter')
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({"message": "Planet created successfully", "planet": new_planet.serialize()}), 201
    
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Failed to create planet", "error": str(e)}), 500


@app.route('/create/people/', methods=['POST'])
def create_people():
    try:
        data = request.json

        if 'name' not in data:
            return jsonify({"message": "Missing required field: name"}), 400  

        new_people = People(
            name=data['name'],
            eye_color=data.get('eye_color'),
            height=data.get('height'),
            skin_color=data.get('skin_color'),
            gender=data.get('gender')
        )

        db.session.add(new_people)
        db.session.commit()

        return jsonify({"message": "People created successfully", "People": new_people.serialize()}), 201  
    
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Failed to create People", "error": str(e)}), 500  


@app.route('/create/vehicle/', methods=['POST'])
def create_vehicle():
    try:
        data = request.json

        if 'name' not in data:
            return jsonify({"message": "Missing required field: name"}), 400  

        new_vehicle = Vehicles(
            name=data['name'],
            model=data.get('model'),
            passengers=data.get('passengers'),
            cost_in_credits=data.get('cost_in_credits'),
            crew=data.get('crew'),
            length=data.get('length')
        )

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({"message": "Vehicle created successfully", "Vehicle": new_vehicle.serialize()}), 201
    
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Failed to create Vehicle", "error": str(e)}), 500 


@app.route('/update/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    try:
        data = request.json
        person = People.query.get(people_id)

        if person is None:
            return jsonify({'message': 'Person not found'}), 404  

        if 'name' in data:
            person.name = data['name']
        if 'eye_color' in data:
            person.eye_color = data['eye_color']
        if 'height' in data:
            person.height = data['height']
        if 'skin_color' in data:
            person.skin_color = data['skin_color']
        if 'gender' in data:
            person.gender = data['gender']

        db.session.commit()

        return jsonify({'message': 'Person updated successfully'}), 200  
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server error'}), 500  



@app.route('/update/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    try:
        data = request.json
        planet = Planets.query.get(planet_id)

        if planet is None:
            return jsonify({'message': 'Planet not found'}), 404  

        if 'name' in data:
            planet.name = data['name']
        if 'gravity' in data:
            planet.gravity = data['gravity']
        if 'population' in data:
            planet.population = data['population']
        if 'climate' in data:
            planet.climate = data['climate']
        if 'diameter' in data:
            planet.diameter = data['diameter']

        db.session.commit()

        return jsonify({'message': 'Planet updated successfully'}), 200  
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server error'}), 500


@app.route('/update/vehicle/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        data = request.json
        vehicle = Vehicles.query.get(vehicle_id)

        if vehicle is None:
            return jsonify({'message': 'Vehicle not found'}), 404  

        if 'name' in data:
            vehicle.name = data['name']
        if 'model' in data:
            vehicle.model = data['model']
        if 'passengers' in data:
            vehicle.passengers = data['passengers']
        if 'cost_in_credits' in data:
            vehicle.cost_in_credits = data['cost_in_credits']
        if 'crew' in data:
            vehicle.crew = data['crew']
        if 'length' in data:
            vehicle.length = data['length']

        db.session.commit()

        return jsonify({'message': 'Vehicle updated successfully'}), 200  
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server error'}), 500

@app.route('/delete/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    try:
        person = People.query.get(people_id)

        if person is None:
            return jsonify({'message': 'Person not found'}), 404  

        db.session.delete(person)
        db.session.commit()

        return jsonify({'message': 'Person deleted successfully'}), 200  
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server error'}), 500  


@app.route('/delete/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        planet = Planets.query.get(planet_id)

        if planet is None:
            return jsonify({'message': 'Planet not found'}), 404  

        db.session.delete(planet)
        db.session.commit()

        return jsonify({'message': 'Planet deleted successfully'}), 200  
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server error'}), 500 


@app.route('/delete/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        vehicle = Vehicles.query.get(vehicle_id)

        if vehicle is None:
            return jsonify({'message': 'Vehicle not found'}), 404  

        db.session.delete(vehicle)
        db.session.commit()

        return jsonify({'message': 'Vehicle deleted successfully'}), 200  
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Server error'}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)




