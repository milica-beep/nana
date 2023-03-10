import datetime
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pymongo
from mongo_db import get_db
from bson.objectid import ObjectId
from bson import json_util

recipe_route = Blueprint('recipe', __name__)

@recipe_route.route('/recipe/get-categories', methods=['GET'])
@jwt_required()
def get_categories():
    db = get_db()
    categories_collection = db.categories

    categories = list(categories_collection.find({}))

    return json.loads(json_util.dumps({'categories': categories})), 200

@recipe_route.route('/recipe/get-levels', methods=['GET'])
@jwt_required()
def get_levels():
    db = get_db()
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
    
    user_id = ObjectId(get_jwt_identity())

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

    db = get_db()
    recipes_collection = db.recipes

    recipes_collection.insert_one(new_recipe)

    return {'message':'OK'}, 200

@recipe_route.route('/recipe/get-latest', methods=['GET'])
@jwt_required()
def get_recipes():
    page = int(request.args.get('page'))
    limit = 5

    db = get_db()
    recipes_collection = db.recipes

    latest_recipes = list(recipes_collection.find().sort('timestamp', pymongo.DESCENDING).skip(page*limit).limit(limit))
    
    return json.loads(json_util.dumps({'recipes': latest_recipes})), 200

@recipe_route.route('/recipe/get-latest-by-cat', methods=['GET'])
@jwt_required()
def get_by_cat():
    page = int(request.args.get('page'))
    catId = request.args.get('categoryId')
    limit = 5

    db = get_db()
    recipes_collection = db.recipes

    latest_recipes = list(recipes_collection.find({'categories': {'$elemMatch': {'_id': ObjectId(catId)}}}) \
                                            .sort('timestamp', pymongo.DESCENDING) \
                                            .skip(page*limit) \
                                            .limit(limit))
    
    return json.loads(json_util.dumps({'recipes': latest_recipes})), 200

@recipe_route.route('/recipe/get-recipe', methods=['GET'])
@jwt_required()
def get_recipe_by_id():
    recipe_id = request.args.get('id')

    db = get_db()
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

    user_id = ObjectId(get_jwt_identity())

    rec_id = ObjectId(id)

    db = get_db()
    recipe_collection = db.recipes

    recipe = recipe_collection.find_one({'_id': rec_id})

    if(str(user_id) != str(recipe['userId'])):
        return jsonify({'error': 'Unauthorized'}), 401

    recipe_collection.update_one({'_id': rec_id}, {'$set' : {'title': title,'ingredients': ingredients, 'preparation': preparation,'preparationTime': preparation_time,'briefSummary': brief_summary,'categories': categories,'level': level,'timestamp': timestamp}})

    return json.loads(json_util.dumps({'message': 'ok'})), 200

@recipe_route.route('/recipe/delete-recipe', methods=['DELETE'])
@jwt_required()
def delete_recipe():
    recipe_id = request.args.get('id')

    db = get_db()
    recipes_collection = db.recipes

    recipes_collection.delete_one({'_id': ObjectId(recipe_id)})

    return jsonify({
        'message': 'Ok'
    })

@recipe_route.route('/recipe/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('query')

    db = get_db()
    recipes_collection = db.recipes

    recipes = list(recipes_collection.find({'title': {'$regex': query, '$options': 'i'}}))

    return json.loads(json_util.dumps({'recipes': recipes})), 200

