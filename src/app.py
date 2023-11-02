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
from models import db, User, Character, Planet, Favorite
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

#get a list of all blog users
@app.route('/user', methods=['GET'])
def handle_hello():
    names = []
    users = User.query.all()
    for i in users:
        names.append(i.serialize())
    return jsonify(names), 200
    

#get the favorites of the current user
@app.route('/user/favorite', methods=['GET'])
def user_favorites():
    items = []
    favorites = Favorite.query.all()
    for i in favorites:
        items.append(i.serialize())
    return jsonify(items), 200

#get all characters
@app.route('/character', methods = ['GET'])
def handle_characters():
    names = []
    characters = Character.query.all()
    for i in characters:
        names.append(i.serialize())
    return jsonify(names), 200
   
#get specific character
@app.route('/character/<int:character_id>', methods = ['GET'])
def handle_character(character_id):
    person = Character.query.get(character_id)
    return jsonify(person.serialize()), 200

#get all planets
@app.route('/planet', methods = ['GET'])
def handle_planets():
    names = []
    planets = Planet.query.all()
    for i in planets:
        names.append(i.serialize())
    return jsonify(names), 200


#get specific planet
@app.route('/planet/<int:planet_id>', methods = ['GET'])
def handle_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

#add character to favorites
@app.route('/favorite/character/<int:character_id>', methods = ['POST'])
def add_character(character_id):
    favorite = Favorite(user_id = 2, character_id = character_id)
    if Favorite.query.filter_by(character_id = character_id).first() == None:
        db.session.add(favorite)
        db.session.commit()
        return jsonify("Added Favorite!"), 200
    else:
        return jsonify("Favorite was already added"), 400

#add planet to favorites
@app.route('/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_planet(planet_id):
    favorite = Favorite(user_id = 2, planet_id = planet_id)
    if Favorite.query.filter_by(planet_id = planet_id).first() == None:
        db.session.add(favorite)
        db.session.commit()
        return jsonify("Added Favorite!"), 200
    else:
        return jsonify("Favorite was already added"), 400

#delete character from favorites
@app.route('/favorite/character/<int:character_id>', methods = ['DELETE'])
def delete_character(character_id):
    favoritesList = Favorite.query.all()
    toDelete = None
    for item in favoritesList:
        if item.serialize()['character_id'] == character_id:
            toDelete = item
    if toDelete == None:
        return jsonify("Invalid character ID"), 400
    else:
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify("Favorite deleted."), 200

#delete planet from favorites
@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_planet(planet_id):
    favoritesList = Favorite.query.all()
    toDelete = None
    for item in favoritesList:
        if item.serialize()['planet_id'] == planet_id:
            toDelete = item
    if toDelete == None:
        return jsonify("Invalid planet ID"), 400
    else:
        db.session.delete(toDelete)
        db.session.commit()
        return jsonify("Favorite deleted."), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
