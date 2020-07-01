from api import db
from models import *

def add(name):
	item = Item(name=name)
	db.session.add(item)
	db.session.commit()

for name in ["dog", "apple", "kiwi", "jake", "cup", "up", "red"]:
	add(name)

