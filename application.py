import os
from  dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api

load_dotenv(find_dotenv())

app = Flask(__name__)

# Check for environment variable
if not os.getenv("SQLALCHEMY_DATABASE_URI"):
    raise RuntimeError("DATABASE_URL is not set")

# configure database settings
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


migrate = Migrate(app, db)
api = Api(app)

from models import Food, Category


@app.route("/")
def index():
	return render_template("index.html")


class Foods(Resource):
	""" deals with all operations concerning working with a single food in the database"""
	def get(self, foodName):
		""" return a json representaion of a food object, 
			food object contains an image url, nutrional information and a category attributes """
		try:
			foodName = foodName.lower()
			food = Food.query.filter_by(name=foodName).one()
		except:
			return {"message": "food resource not found", "status":404}, 404
		return food.foodRepresentation()

	
class FoodCategory(Resource):
	""" deals with all operations concerning working with a category of foods in the database"""
	def get(self, categoryName):
		""" returns a list of all the foods that belong to the category that was requested"""
		try:
			categoryName = categoryName.lower()
			category = Category.query.filter_by(name=categoryName).one()
		except:
			return {"message": "category not found", "status":404}, 404

		return category.getAllFoods()


class AllFoods(Resource):
	""" deals with all operations concerning working with a single food in the database"""
	def get(self):
		""" returns a list of every food in the database"""
		foods = Food.query.all()
		return [food.foodRepresentation() for food in foods]

# add the endpoints for each group of api operations
api.add_resource(Foods, "/api/foods/<string:foodName>")
api.add_resource(FoodCategory, "/api/food_category/<string:categoryName>")
api.add_resource(AllFoods, "/api/foods")

if __name__ == "__main__":
	app.run()