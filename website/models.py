from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref

class Recipe(db.Model, ):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    people = db.Column(db.Integer)
    time = db.Column(db.Integer)
    instructions = db.relationship("Instruction", backref="recipe")
    ingredients = db.relationship("Ingredient", backref="recipe")

    def __repr__(self):
        return f'<Recipe "{self.title}">'

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'
    
class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    recipes = db.relationship('Recipe')

