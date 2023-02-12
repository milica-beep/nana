import datetime
import random

from bson import ObjectId
from pymongo import MongoClient
from passlib.hash import sha256_crypt

client = MongoClient('localhost', 27017)
db = client.nana

# create indexes 
recipe_collection = db.recipes
user_collection = db.users

recipe_collection.create_index('title')
user_collection.create_index('email')

print('Creating data...')

usrs = [
    {
        'email': 'user1@example.com',
        'password': sha256_crypt.hash('123'),
        'name': 'John',
        'lastname': 'Doe'
    },
    {
        'email': 'user2@example.com',
        'password': sha256_crypt.hash('123'),
        'name': 'Jane',
        'lastname': 'Smith'
    },
    {
        'email': 'user3@example.com',
        'password': sha256_crypt.hash('123'),
        'name': 'Bob',
        'lastname': 'Johnson'
    },
    {
        'email': 'user4@example.com',
        'password': sha256_crypt.hash('123'),
        'name': 'Amy',
        'lastname': 'Williams'
    },
    {
        'email': 'user5@example.com',
        'password': sha256_crypt.hash('123'),
        'name': 'Sarah',
        'lastname': 'Brown'
    }
]

user_collection.insert_many(usrs)
print('Users created!')

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
categories_collection = db.categories
categories_collection.insert_many(cats)

print('Categories created!')

lvls = [
    {'name': 'Beginner'},
    {'name': 'Intermediate'},
    {'name': 'Chef'},
]

levels_collection = db.levels

levels_collection.insert_many(lvls)

print('Levels created!')

levels = list(levels_collection.find({}))
categories = list(categories_collection.find({}))
users = list(user_collection.find({}))

# for getting random date
start_date = datetime.datetime.now() - datetime.timedelta(days=20)
end_date = datetime.datetime.now() - datetime.timedelta(days=5)

recipes = [
    {
        'title': 'Chicken Alfredo',
        'ingredients': [
            '1 lb boneless chicken breast, cut into bite-sized pieces',
            '1 cup heavy cream',
            '1 cup grated Parmesan cheese',
            '2 cloves garlic, minced',
            '1 teaspoon salt',
            '1 teaspoon black pepper',
            '1 pound fettuccine pasta, cooked al dente'
        ],
        'preparation': '''
            1. In a large saucepan, heat the heavy cream and minced garlic over medium heat.
            2. Add the chicken to the pan and cook until it is no longer pink, about 8-10 minutes.
            3. Stir in the grated Parmesan cheese and continue cooking until the cheese is melted and the sauce is thick and creamy.
            4. Season with salt and pepper to taste.
            5. Serve the sauce over cooked fettuccine pasta.
        ''',
        'preparationTime': '30 min',
        'briefSummary': 'This classic Italian dish features tender chicken in a rich, creamy Parmesan sauce, served over a bed of fettuccine pasta.',
        'level': random.choice(levels),
        'categories': [random.choice(categories)],
        'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
        'title': 'Beef Tacos',
        'ingredients': [
            '1 lb ground beef',
            '1 teaspoon chili powder',
            '1 teaspoon cumin',
            '1/2 teaspoon paprika',
            '1/2 teaspoon onion powder',
            '1/2 teaspoon garlic powder',
            '1/2 teaspoon salt',
            '1/4 teaspoon black pepper',
            '8 soft taco shells',
            '1 cup shredded lettuce',
            '1 cup shredded cheddar cheese',
            '1 diced tomato',
            '1 diced avocado',
            '1/2 cup sour cream'
        ],
        'preparation': '''
            1. In a large skillet, cook the ground beef over medium heat until browned and fully cooked.
            2. Drain any excess fat and return the beef to the pan.
            3. Add the chili powder, cumin, paprika, onion powder, garlic powder, salt, and pepper to the pan. Stir to combine.
            4. Spoon the beef mixture into each taco shell and top with shredded lettuce, shredded cheese, diced tomato, diced avocado, and a dollop of sour cream.
            5. Serve immediately.
        ''',
        'preparationTime': '20 min',
        'briefSummary': 'These delicious beef tacos feature seasoned ground beef and a variety of fresh toppings, all nestled in a soft taco shell.',
        'level': random.choice(levels),
        'categories': [random.choice(categories)],
        'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
        'title': 'Vegetarian Stir Fry',
    'ingredients': [
    '1 tablespoon oil',
    '1 onion, sliced',
    '2 cloves garlic, minced',
    '1 red bell pepper, sliced',
    '1 yellow bell pepper, sliced',
    '1 cup sliced mushrooms',
    '1 cup sliced carrots',
    '1 cup snow peas',
    '1 cup tofu, cut into cubes',
    '1/4 cup soy sauce',
    '1/4 cup hoisin sauce',
    '2 tablespoons cornstarch'
    ],
    'preparation': '''
    1. Heat the oil in a large wok or skillet over high heat.
    2. Add the onion, garlic, red bell pepper, yellow bell pepper, mushrooms, carrots, and snow peas to the pan. Stir fry for 2-3 minutes.
    3. Add the tofu to the pan and continue stir frying for an additional 2-3 minutes.
    4. In a small bowl, whisk together the soy sauce, hoisin sauce, and cornstarch.
    5. Pour the sauce into the pan and stir to combine.
    6. Continue stir frying until the sauce has thickened and the vegetables are tender but still crisp.
    7. Serve over cooked rice or noodles.
    ''',
    'preparationTime': '20 min',
    'briefSummary': 'This quick and easy stir fry is packed with colorful vegetables and tofu, all tossed in a savory sauce.',
    'level': random.choice(levels),
    'categories': [random.choice(categories)],
    'userId': ObjectId(random.choice(users)['_id']),
    'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
    'title': 'Lasagna',
    'ingredients': [
    '1 lb ground beef',
    '1 onion, diced',
    '2 cloves garlic, minced',
    '1 can (28 oz) crushed tomatoes',
    '1 teaspoon dried basil',
    '1 teaspoon dried oregano',
    '1 teaspoon salt',
    '1/2 teaspoon black pepper',
    '1 package (9 oz) oven-ready lasagna noodles',
    '1 container (15 oz) ricotta cheese',
    '2 cups shredded mozzarella cheese',
    '1/2 cup grated Parmesan cheese'
    ],
    'preparation': '''
    1. Preheat the oven to 375°F (190°C).
    2. In a large skillet, cook the ground beef, onion, and garlic over medium heat until the beef is browned and fully cooked. Drain any excess fat.
    3. Add the crushed tomatoes, basil, oregano, salt, and pepper to the skillet. Stir to combine.
    4. In a large baking dish, layer the cooked lasagna noodles, ricotta cheese, the beef mixture, and the mozzarella cheese. Repeat until all ingredients have been used, ending with a layer of mozzarella cheese on top.
    5. Sprinkle the grated Parmesan cheese over the top of the lasagna.
    6. Cover the dish with foil and bake for 25 minutes.
    7. Remove the foil and continue baking for an additional 25 minutes, or until the cheese is melted and the lasagna is heated through.
    8. Let the lasagna cool for 10 minutes before serving.
    ''',
    'preparationTime': '60 min',
    'briefSummary': 'This classic Italian dish features layers of tender lasagna noodles, a rich meat sauce, and plenty of melted cheese. Perfect for feeding a crowd or meal prepping for the week.',
    'level': random.choice(levels),
    'categories': [random.choice(categories)],
    'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
    'title': 'Chicken Fajitas',
    'ingredients': [
    '1 lb boneless, skinless chicken breasts, sliced into strips',
    '2 bell peppers, sliced into strips',
    '1 onion, sliced into strips',
    '2 tablespoons oil',
    '1 teaspoon chili powder',
    '1 teaspoon cumin',
    '1 teaspoon paprika',
    '1/2 teaspoon garlic powder',
    '1/2 teaspoon salt',
    '1/4 teaspoon black pepper',
    '8 flour tortillas, warmed',
    'Sour cream and shredded cheese, for serving (optional)'
    ],
    'preparation': '''
    1. In a large bowl, toss together the chicken strips, bell peppers, onion, oil, chili powder, cumin, paprika, garlic powder, salt, and pepper.
    2. Heat a large skillet over high heat. Add the chicken mixture to the pan and cook, stirring occasionally, until the chicken is cooked through and the vegetables are tender, about 10 minutes.
    3. Serve the chicken and vegetables in the warm flour tortillas, topped with sour cream and shredded cheese if desired.
    ''',
    'preparationTime': '30 min',
    'briefSummary': 'These sizzling chicken fajitas are loaded with juicy chicken, crisp peppers and onions, and a bold blend of spices.',
    'level': random.choice(levels),
    'categories': [random.choice(categories)],
    'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
        'title': 'Cauliflower Fried Rice',
        'ingredients': [
            '1 head cauliflower, grated',
            '2 tablespoons oil',
            '1 onion, diced',
            '2 cloves garlic, minced',
            '2 carrots, diced',
            '2 eggs, beaten',
            '1/4 cup soy sauce',
            '2 tablespoons sesame oil',
            '1 teaspoon ginger, grated',
            '1/2 teaspoon black pepper',
            '2 green onions, sliced'
        ],
        'preparation': '''
        1. In a large skillet, heat the oil over medium heat.
        2. Add the onion, garlic, and carrots to the pan. Stir fry for 2-3 minutes.
        3. Push the vegetables to one side of the pan and pour the beaten eggs into the empty side of the pan. Scramble the eggs until fully cooked, then mix them with the vegetables.
        4. Add the grated cauliflower to the pan and continue stir frying for an additional 2-3 minutes.
        5. In a small bowl, whisk together the soy sauce, sesame oil, ginger, and black pepper.
        6. Pour the sauce into the pan and stir to combine.
        7. Continue stir frying until the cauliflower is tender and the sauce has been absorbed, about 5-7 minutes.
        8. Stir in the sliced green onions.
        9. Serve immediately.
        ''',
        'preparationTime': '30 min',
        'briefSummary': 'This classic Italian dish features layers of tender lasagna noodles, a rich meat sauce, and plenty of melted cheese. Perfect for feeding a crowd or meal prepping for the week.',
        'level': random.choice(levels),
        'categories': [random.choice(categories)],
        'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
        'title': 'Stuffed Bell Peppers',
        'ingredients': [
            '4 large bell peppers', 
            '1 lb ground beef', 
            '1 small onion, diced', 
            '1 clove garlic, minced', 
            '1 cup cooked rice', 
            '1 can diced tomatoes', 
            '1 tsp salt', 
            '1 tsp black pepper'],
        'preparation': '1. Preheat oven to 375°F.\n2. Cut the tops off of the bell peppers and remove the seeds and membranes.\n3. In a large skillet, brown the ground beef over medium heat. Add the onion and garlic and cook until softened.\n4. Stir in the cooked rice, diced tomatoes, salt, and pepper.\n5. Fill each bell pepper with the ground beef mixture.\n6. Place the bell peppers in a baking dish and bake for 30-35 minutes, or until the peppers are tender.\n7. Serve hot.',
        'preparationTime': '45 min',
        'briefSummary': 'Stuffed bell peppers are a classic comfort food that are easy to make and delicious. This recipe uses a mixture of ground beef, rice, tomatoes, and spices to fill tender bell peppers and bake to perfection in the oven.',
        'level': random.choice(levels),
        'categories': [random.choice(categories)],
        'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
    },
    {
        'title': 'Spaghetti Carbonara',
        'ingredients': [
            '1 pound spaghetti',
            '4 large eggs',
            '1 cup grated parmesan cheese',
            '1 pound bacon, diced',
            'Salt and pepper to taste'
        ],
        'preparation': '1. Cook the spaghetti in a large pot of salted boiling water according to package instructions.\n2. While the spaghetti is cooking, cook the bacon in a large pan over medium heat until crispy.\n3. In a large bowl, whisk together the eggs, parmesan cheese, salt, and pepper.\n4. Drain the spaghetti and add it to the bowl with the egg mixture.\n5. Add the bacon and toss to combine.\n6. Serve immediately, garnished with additional parmesan cheese and black pepper.',
        'preparationTime': '30 minutes',
        'briefSummary': 'A creamy and delicious spaghetti carbonara made with spaghetti, eggs, parmesan cheese, bacon, and seasonings.',
        'level': random.choice(levels),
        'categories': [random.choice(categories)],
        'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
  },
  {
        'title': 'Grilled Cheese Sandwich',
        'ingredients': [
            '2 slices of bread',
            '2 slices of cheddar cheese',
            '1 tablespoon butter'
        ],
        'preparation': '1. Heat a pan over medium heat.\n2. Spread the butter on one side of each slice of bread.\n3. Place one slice of bread, buttered side down, in the pan.\n4. Top with one slice of cheddar cheese, followed by the second slice of bread, buttered side up.\n5. Cook until the bread is golden brown and the cheese is melted, about 3-4 minutes per side.\n6. Serve hot.',
        'preparationTime': '10 minutes',
        'briefSummary': 'A classic grilled cheese sandwich made with cheddar cheese and butter on two slices of bread.',
        'level': random.choice(levels),
        'categories': [random.choice(categories)],
        'userId': ObjectId(random.choice(users)['_id']),
        'timestamp': (start_date + (end_date - start_date) * random.random()).replace(microsecond=0)
  },]

recipe_collection.insert_many(recipes)
print('Recipes created!')