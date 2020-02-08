from kisseklyv import db

class Kisse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    people = db.relationship("Person", backref="kisse", lazy="dynamic")

    def as_dict(self):
        return {
            "object_type": "kisse",
            "id": self.id,
            "description": self.description,
            "people": [person.as_dict() for person in self.people]
        }

    def klyv(self):
        return {"data": "test"}

    def __repr__(self):
        return f"Kisse (id={self.id}): {self.description}"


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    kisse_id = db.Column(db.Integer, db.ForeignKey("kisse.id"))
    expenses = db.relationship("Expense", backref="person", lazy="dynamic")

    def as_dict(self):
        return {
            "object_type": "person",
            "id": self.id,
            "name": self.name,
            "kisse_id": self.kisse_id
        }

    def __repr__(self):
        return f"Person (id={self.id}): {self.name}. Kisse_id: {self.kisse_id}"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))

    def as_dict(self):
        return {
            "object_type": "expense",
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "person_id": self.person_id
        }

    def __repr__(self):
        return f"Expense (id={self.id}): {self.description}"

