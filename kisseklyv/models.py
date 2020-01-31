from kisseklyv import db

class Kisse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    people = db.relationship("Person", backref="kisse", lazy="dynamic")

    def as_dict(self):
        return {
            "kisse_id": self.id,
            "description": self.description,
            "people": [person.name for person in self.people]
        }

    def __repr__(self):
        return f"Kisse (id={self.id}): {self.description}"


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    kisse_id = db.Column(db.Integer, db.ForeignKey("kisse.id"))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "kisse_id": self.kisse_id
        }

    def __repr__(self):
        return f"Person (id={self.id}): {self.name}. Kisse_id: {self.kisse_id}"