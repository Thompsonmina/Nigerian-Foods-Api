from api import db

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), nullable=False)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def remove(self):
		db.session.add(self)
		db.session.commit()

	def __repr__(self):
		return "<user %r>" % self.name
