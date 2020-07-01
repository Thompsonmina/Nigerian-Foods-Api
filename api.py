import os
from  dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from models import *

class Names(Resource):
	def get(self, itemName):
		return jsonify({itemName: Item.query.filter_by(name=itemName).first().name})

	def post(self, itemName):
		item = Item(name=itemName)
		db.session.add(item)
		db.session.commit()
		return jsonify(True)

api.add_resource(Names, "/<string:itemName>")

if __name__ == "__main__":
	app.run()