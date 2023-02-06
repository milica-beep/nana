from mongo_db import db

print('Creating data...')
cats = [
    {'name' : 'Breakfast'},
    {'name' : 'Lunch'},
    {'name' : 'Dinner'},
    {'name' : 'Salads'},
    {'name' : 'Cakes'},
    {'name' : 'Vegan'},
    {'name' : 'Vegeterian'},
    {'name' : 'Children'}
]
categories = db.categories
categories.insert_many(cats)

print('Categories created!')

lvls = [
    {'name': 'Beginner'},
    {'name': 'Intermediate'},
    {'name': 'Chef'},
]

levels = db.levels

levels.insert_many(lvls)

print('Levels created!')
