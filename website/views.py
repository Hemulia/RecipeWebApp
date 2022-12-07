from flask import Blueprint, render_template, redirect,request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Recipe, Ingredient
from . import db
import json

views = Blueprint('view', __name__)


@views.route('/')
@login_required
def home():
    # get all the recipes form data
    recipes = Recipe.query.all()
    #count the price for one serving
    for recipe in recipes:
        recipe.price_per_person = recipe.price / recipe.people
    return render_template("home.html", user=current_user, recipes=recipes)


@views.route("/addrecipe", methods=["GET", "POST"])
@login_required
def add_name():
    if request.method == "POST":
        # get the form data
        title = request.form.get("title")
        instructions = request.form.get("instructions")
        price = request.form.get("price")
        people = request.form.get("people")
        time = request.form.get("time")
        
        #check that input data type is valid
        if not people.isdigit(): 
            flash("Please use a valid number", category='error')
        elif "," in price:
            flash("Please use a dot (.) as the decimal separator for the price", category='error')
        elif "," in time:
            flash("Please add time in minutes not in hours", category='error')
        else:

            # add the recipe to the database
            recipe = Recipe(title=title, instructions=instructions, price=price,people=people, time=time, user_id=current_user.id)
            db.session.add(recipe)
            db.session.commit()

            # redirect to the next page in the recipe creation process
            return redirect(url_for("view.addingredients", recipe_id=recipe.id))

    # render the form page
    return render_template("addrecipe.html", user=current_user)

@views.route("/addingredients/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def addingredients(recipe_id):
    # get the recipe from the database
    recipe = Recipe.query.get(recipe_id)

    if request.method == "POST":
        # get the form data
        ingredient_name = request.form.get("name")
        # add the ingredient to the database
        ingredient = Ingredient(name=ingredient_name, recipe_id=recipe_id)
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient saved", category='info')
    return render_template('addingredients.html', user=current_user,)

@views.route('/delete-recipe')
def delete_recipe():
    # get the recipe from the database
    recipe_id = request.args.get('recipe_id')
    recipe = Recipe.query.get(recipe_id)
    # delete recipe
    db.session.delete(recipe)
    db.session.commit()
    return redirect('/')

