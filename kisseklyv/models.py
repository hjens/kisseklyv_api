from kisseklyv import db

class Kisse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    def as_dict(self):
        return {
            "kisse_id": self.id,
            "description": self.description
        }

    def __repr__(self):
        return f"Kisse (id={self.id}): {self.description}"