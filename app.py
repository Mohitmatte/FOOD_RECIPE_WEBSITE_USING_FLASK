from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from urllib.parse import unquote

#create the flask app
app = Flask(__name__)

# replace with your api key
api_key = "444d3c2f0b1f4b9ab682fda8afc7ea86"

#define the route for the home button
@app.route("/home",methods=["GET"])
def home():
    return render_template("index.html",recipes=[],search_query="")

#define the main route for the app
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form.get("search_query"," ")
        recipes = search_recipes(search_query)
        return render_template("index.html", recipes=recipes, search_query=search_query)


    search_query=request.args.get("search_query", "")   
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template("index.html", recipes=recipes, search_query=search_query)

def search_recipes(search_query):
    url=f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': api_key,
        'query': search_query,
        'number': 10,
        'offset': 0,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['results']
    
    return [] 


@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    search_query = request.args.get("search_query", "")
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': api_key,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe = response.json()
        return render_template("view_recipe.html", recipe=recipe,search_query=search_query)

    return "Error fetching recipe details", 500

if __name__ == "__main__":
    app.run(debug=True)
