from mongo_db import db

print('Creating data...')
cats = [
    {'name' : 'breakfast'},
    {'name' : 'lunch'},
    {'name' : 'dinner'},
    {'name' : 'salads'},
    {'name' : 'cakes'},
    {'name' : 'vegan'},
    {'name' : 'vegeterian'},
    {'name' : 'children'}
]
categories = db.categories
categories.insert_many(cats)

print('Categories created!')

lvls = [
    {'name': 'beginner'},
    {'name': 'intermediate'},
    {'name': 'chef'},
]

levels = db.levels

levels.insert_many(lvls)

print('Levels created!')
