
from flask import Flask, redirect, render_template, request, jsonify, flash
import sqlite3
from model.recipe import Recipe
from model.ingredient import Ingredient

app = Flask(__name__)
conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)
c = conn.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes/search")
def recipe_lists():
    q = request.args.get("q")
    if q:
        c.execute("""SELECT * FROM recipes WHERE name LIKE ?""", ('%'+q+'%',))
    else:
        c.execute("""SELECT * FROM recipes""")
    recipes = jsonify([Recipe(*recipe).to_dict() for recipe in c.fetchall()])
    print(recipes.json)
    return recipes


@app.route("/recipe/add", methods=["GET", "POST"])
def recipe_add():
    if request.method == "POST":
        try:
            veggie = request.form["veggie"]
        except:
            veggie = False
        try:
            Recipe(None, request.form["name"], veggie).addToDatabase()
        except ValueError:
            return render_template("recipes_create.html", error="already_exists")

        return redirect("/recipes")
    return render_template("recipes_create.html")


if __name__ == "__main__":
    app.run(debug="True")

conn.close()
