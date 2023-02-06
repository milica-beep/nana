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
@jwt_required()
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
        cat['_id'] = ObjectId(cat['_id']['$oid'])

    level['_id'] = ObjectId(level['_id']['$oid'])

    if not title:
        return {'title': 'This field is required.'}, 400
    
    if not preparation:
        return {'preparation': 'This field is required.'}, 400
    
    user_id = get_jwt_identity()

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
    
    return json.loads(json_util.dumps({'recipes': latest_recipes})), 200

@recipe_route.route('/recipe/get-latest-by-cat', methods=['GET'])
def get_by_cat():
    page = int(request.args.get('page'))
    catId = request.args.get('categoryId')
    limit = 5
    print(catId)

    recipes_collection = db.recipes

    latest_recipes = list(recipes_collection.find({'categories': {'$elemMatch': {'_id': ObjectId(catId)}}}).sort('timestamp', pymongo.DESCENDING).skip(page*limit).limit(limit))
    
    return json.loads(json_util.dumps({'recipes': latest_recipes})), 200

@recipe_route.route('/recipe/get-recipe', methods=['GET'])
def get_recipe_by_id():
    recipe_id = request.args.get('id')

    recipes_collection = db.recipes

    recipe = recipes_collection.find_one({'_id': ObjectId(recipe_id)})

    return json.loads(json_util.dumps(recipe)), 200

@recipe_route.route('/recipe/update-recipe', methods=['POST'])
@jwt_required()
def update_recipe():
    req = request.get_json()

    id = req['_id']['$oid']
    title = str(req['title'])
    ingredients = req['ingredients']
    preparation = str(req['preparation'])
    preparation_time = str(req['preparationTime'])
    brief_summary = str(req['briefSummary'])
    timestamp = datetime.datetime.today().replace(microsecond=0)

    categories = req['categories']
    level = req['level']

    for cat in categories:
        cat['_id'] = ObjectId(cat['_id']['$oid'])

    level['_id'] = ObjectId(level['_id']['$oid'])

    if not title:
        return {'title': 'This field is required.'}, 400
    
    if not preparation:
        return {'preparation': 'This field is required.'}, 400

    user_id = get_jwt_identity()

    rec_id = ObjectId(id)

    recipe_collection = db.recipes

    recipe = recipe_collection.find_one({'_id': rec_id})

    if(str(user_id) != str(recipe['userId'])):
        return jsonify({'error': 'Unauthorized'}), 401

    recipe_collection.update_one({'_id': rec_id}, {'$set' : {'title': title,'ingredients': ingredients, 'preparation': preparation,'preparationTime': preparation_time,'briefSummary': brief_summary,'categories': categories,'level': level,'timestamp': timestamp}})

    return json.loads(json_util.dumps({'message': 'ok'})), 200

