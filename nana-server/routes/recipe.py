import datetime
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
import pymongo
from mongo_db import db
from bson.objectid import ObjectId
from bson import json_util

recipe_route = Blueprint('recipe', __name__)

@recipe_route.route('/recipe/get-categories', methods=['GET'])
def get_categories():
    categories_collection = db.categories

    categories = list(categories_collection.find({}))

    return json.loads(json_util.dumps({'categories': categories})), 200

@recipe_route.route('/recipe/get-levels', methods=['GET'])
def get_levels():
    levels_collection = db.levels

    levels = list(levels_collection.find({}))

    return json.loads(json_util.dumps({'levels': levels})), 200

@recipe_route.route('/recipe/create', methods=['POST'])
def create():
    req = request.get_json()

    title = str(req['title'])
    ingredients = req['ingredients']
    preparation = str(req['preparation'])
    preparation_time = str(req['preparationTime'])
    brief_summary = str(req['briefSummary'])
    timestamp = datetime.datetime.today().replace(microsecond=0)

    categories = req['categories']
    level = req['level']

    for cat in categories:
        print(cat)
        cat['_id'] = ObjectId(cat['_id']['$oid'])

    level['_id'] = ObjectId(level['_id']['$oid'])

    if not title:
        return {'title': 'This field is required.'}, 400
    
    if not preparation:
        return {'preparation': 'This field is required.'}, 400
    
   # user_id = get_jwt_identity()
    user_id = ObjectId('63de22ca32e742dafa9c2d18')

    new_recipe = {
        'title': title,
        'ingredients': ingredients,
        'preparation': preparation,
        'preparationTime': preparation_time,
        'briefSummary': brief_summary,
        'categories': categories,
        'level': level,
        'userId': user_id,
        'timestamp': timestamp
    }

    recipes_collection = db.recipes

    recipes_collection.insert_one(new_recipe)

    return {'message':'OK'}, 200

@recipe_route.route('/recipe/get-latest', methods=['GET'])
def get_recipes():
    page = int(request.args.get('page'))
    limit = 5

    recipes_collection = db.recipes

    latest_recipes = list(recipes_collection.find().sort('timestamp', pymongo.DESCENDING).skip(page*limit).limit(limit))
    print(latest_recipes)
    
    return json.loads(json_util.dumps({'recipes': latest_recipes})), 200