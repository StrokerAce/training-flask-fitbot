from flask import Flask, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, WriteError

app = Flask(__name__)

db = MongoClient('localhost', 27017, username = 'fitbotUser', password = 'fitbotUserPass', authSource = 'fitbot_db')['fitbot_db']

recipes = db.recipes

@app.route("/addRecipe", methods=['POST'])
def addRecipe():
    if request.is_json:
        recipe = request.get_json()
        try:
            recipes.insert_one(recipe).inserted_id
            return "Successfully added recipe:\n" + str(recipe)
        except WriteError as write_error:
            return write_error._message, 400
        except Exception:
            return traceback.format_exception(*sys.exc_info()), 500
    else:
        return "Message body is not JSON", status.HTTP_400_BAD_REQUEST

@app.route("/getAllRecipes", methods=['GET'])
def getAllRecipes():
    try:
        all_recipes = recipes.find()
        return str(list(all_recipes))
    except Exception:
        return traceback.format_exception(*sys.exc_info()), 500
