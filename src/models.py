from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    description = db.Column(db.Text)
    gender = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    height = db.Column(db.Float)
    birth_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img_url": self.img_url,
            "description": self.description,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "birth_year": self.birth_year
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    description = db.Column(db.Text)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img_url": self.img_url,
            "description": self.description,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Character)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }

