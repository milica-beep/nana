from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_route
from routes.recipe import recipe_route
app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

if __name__ == '__main__':

    app.register_blueprint(auth_route)
    app.register_blueprint(recipe_route)

    app.run(debug='true')