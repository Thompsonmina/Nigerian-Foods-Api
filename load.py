import pickle

from application import Food, Category

def loadPickle(picklefile):
	with open(picklefile, "rb") as file:
		return pickle.load(file)

def add_food(name, category, link, **kwargs):
	item = Food(name=name, url=link, **kwargs, category_id=Category.query.filter_by(name=category).one().id)
	item.save()

def add_category(name):
	item = Category(name=name)
	item.save()

def main():
	categories = ["rice-based", "soups and stews", "bean-based", 
				"meat-based", "yam-based", "cassava-based", "snacks", 
				"beverages", "others"]


	for name in categories:
		category = Category.query.filter_by(name=name).one()
		print(category.getAllFoods())
		break

	food = Food.query.filter_by(name="soy milk").one()
	print(food.foodRepresentation())

main()