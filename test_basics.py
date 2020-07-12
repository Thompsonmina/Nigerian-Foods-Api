# basic tests for the functionality of the api

import os 
import unittest
import sqlalchemy
from application import app, db, Food, Category

TEST_DB = "test.db"

class ModelFunctionality(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# configurations
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + TEST_DB
	
		db.drop_all()
		db.create_all()

	def tearDown(self):
		db.session.rollback()
		for category in Category.query.all():
			db.session.delete(category)
			db.session.commit()

		for food in Food.query.all():
			db.session.delete(food)
			db.session.commit()

	def test_category_object_exists(self):
		rice_based = Category(name="rice_based")
		rice_based.save()
		rice_based = Category.query.filter_by(name="rice_based").one()
		self.assertIsInstance(rice_based, Category)
		self.assertEqual("rice_based", rice_based.name)

	def test_category_object_not_constructed_well(self):
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			rice_based = Category()
			rice_based.save()

	def test_category_object_is_deleted(self):
		bean_based = Category(name="bean_based")
		bean_based.save()
		bean_based = Category.query.filter_by(name="bean_based").one()
		bean_based.remove()

		self.assertIsNone(Category.query.filter_by(name="bean_based").first())
		self.assertEqual(0, len(Category.query.all()))

	def test_category_is_unique(self):
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			drinks = Category(name="drinks")
			drinks.save()
			water = Category(name="drinks")
			water.save()

	def test_food_object_exists(self):
		food = Food(name="jollof", url="url", category_id=1,
 			calories="123", carbs="678", protein="78", sugar="987", 
 			fat="678", sodium="12")
		
		food.save()
		food = Food.query.filter_by(name="jollof").one()
		self.assertIsInstance(food, Food)
		self.assertEqual("jollof", food.name)

	def test_food_object_not_constructed_well(self):
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			food = Food(name="jollof", url="url", category_id=1)
			food.save()


	def test_food_object_is_deleted(self):
		food = Food(name="jollof", url="url", category_id=1,
 			calories="123", carbs="678", protein="78", sugar="987", 
 			fat="678", sodium="12")
		food.save()
		jollof = Food.query.filter_by(name="jollof").one()
		jollof.remove()

		self.assertIsNone(Category.query.filter_by(name="bean_based").first())
		self.assertEqual(0, len(Category.query.all()))

	def test_food_is_unique(self):
		with self.assertRaises(sqlalchemy.exc.IntegrityError):
			food = Food(name="jollof", url="url", category_id=1,
 			calories="123", carbs="678", protein="78", sugar="987", 
 			fat="678", sodium="12")
			food.save()

			dish = Food(name="jollof", url="url", category_id=1,
 			calories="123", carbs="678", protein="78", sugar="987", 
 			fat="678", sodium="12")
			dish.save()


class ApiFunctionality(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		# configurations
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + TEST_DB
		self.app = app.test_client()
		db.drop_all()
		db.create_all()


		self.FOOD_ITEM = "soy milk"
		self.CATEGORY = "beverages"
		self.SINGLE_FOOD_URL = "/api/foods/" + self.FOOD_ITEM
		self.FOOD_BY_CATEGORY_URL = "/api/food_category/" + self.CATEGORY
		self.ALL_FOODS_URL = "/api/foods"

		category = Category(name=self.CATEGORY)
		category.save()
		food = Food(name=self.FOOD_ITEM, url="url", category_id=1, 
			calories="123", carbs="678", protein="78", sugar="987",
			fat="678", sodium="12")
		food.save()

	def test_index(self):
		response = self.app.get("/", content_type="html/text")
		self.assertEqual(response.status_code, 200)
		
	def test_single_food_request(self):
		response = self.app.get(self.SINGLE_FOOD_URL)
		self.assertEqual(response.status_code, 200)
		self.assertIn(self.FOOD_ITEM.encode(), response.data)

	def test_bad_single_food_request(self):
		response = self.app.get(self.SINGLE_FOOD_URL + "bleh bleh")
		self.assertEqual(response.status_code, 404)
		
	def test_category_request(self):
		response = self.app.get(self.FOOD_BY_CATEGORY_URL)
		self.assertEqual(response.status_code, 200)
		self.assertIn(self.CATEGORY.encode(), response.data)

	def test_bad_category_request(self):
		response = self.app.get(self.FOOD_BY_CATEGORY_URL + "blehbleh")
		self.assertEqual(response.status_code, 404)

	def test_all_foods_request(self):
		response = self.app.get(self.ALL_FOODS_URL)
		self.assertEqual(response.status_code, 200)
		self.assertIsNotNone(response.data)


if __name__ == "__main__":
	unittest.main()