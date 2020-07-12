from application import db
from flask import jsonify

class Food(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(64), nullable=False, unique=True)
	url = db.Column(db.Text, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
	calories = db.Column(db.String(32), nullable=False)
	carbs = db.Column(db.String(16), nullable=False)
	protein = db.Column(db.String(16), nullable=False)
	fat = db.Column(db.String(16), nullable=False)
	sodium = db.Column(db.String(16), nullable=False)
	sugar = db.Column(db.String(6), nullable=False)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def remove(self):
		db.session.delete(self)
		db.session.commit()

	def foodRepresentation(self):
		return {self.name:  
					{"category":Category.query.get(self.category_id).name,
				 	 "img_url":self.url,
				 	 "nutritonal_information": {"calories":self.calories, 
				 	 "carbs":self.carbs, "protein":self.protein, "fat":self.fat,
				 	 "sodium":self.sodium, "sugar": self.sugar}
				 	}
				}

	def __repr__(self):
		return f"< {self.name} calories:{self.calories}>"

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), nullable=False, unique=True)
	foods = db.relationship("Food", backref="category", lazy=True)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def remove(self):
		db.session.delete(self)
		db.session.commit()

	def getAllFoods(self):
		return {self.name: [food.foodRepresentation() for food in self.foods]}



	def __repr__(self):
		return f"< category: {self.name}>"
