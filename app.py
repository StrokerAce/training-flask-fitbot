from bson import ObjectId
from flask import Flask, request
from pymongo import MongoClient
from pymongo.errors import WriteError

app = Flask(__name__)

# TODO: Obtain parameters from config or cmd line
# Get DB connection
db = MongoClient('localhost', 27017, username = 'fitbotUser', password = 'fitbotUserPass', authSource = 'fitbot_db')['fitbot_db']

# Get recipes collection
recipes = db.recipes

# Add a new recipe to the recipes collection
@app.route("/addRecipe", methods=['POST'])
def addRecipe():
    if request.is_json:
        recipe = request.get_json()
        try:
            id = recipes.insert_one(recipe).inserted_id
            return "Successfully added recipe:\n" + str(recipe)
        except WriteError as write_error:
            return write_error._message, 400
        except Exception:
            return traceback.format_exception(*sys.exc_info()), 500
    else:
        return "Message body is not JSON", status.HTTP_400_BAD_REQUEST

# Get a recipe based on the document _id    
@app.route("/getRecipe/<string:id>", methods=['GET'])
def getRecipe(id):
    try:

        if not ObjectId.is_valid(id):
            return "Invalid ObjectId: " + id, 400

        recipe = recipes.find_one(ObjectId(id))

        if recipe is None:
            return "No recipe found with id: {id}", 400
        else:
            return str(recipe)
    except Exception:
        return traceback.format_exception(*sys.exc_info()), 500    

# Get all recipes
@app.route("/getAllRecipes", methods=['GET'])
def getAllRecipes():
    try:
        all_recipes = recipes.find()
        return str(list(all_recipes))
    except Exception:
        return traceback.format_exception(*sys.exc_info()), 500
