import flask_restful
from flask_restful import reqparse
from kisseklyv import models
from kisseklyv import db
from kisseklyv import hashid


class KisseResource(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("description")
        args = parser.parse_args()

        kisse = models.Kisse(description=args["description"])
        db.session.add(kisse)
        db.session.commit()

        return kisse.as_dict(), 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True)
        parser.add_argument("description", required=True)
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        kisse = db.session.query(models.Kisse).get(id)
        if kisse is not None:
            kisse.description = args["description"]
            db.session.commit()
            return "", 200
        else:
            return "", 404

    def delete(self):
        # TODO: ta bort alla personer som hör hit
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True)
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        kisse = db.session.query(models.Kisse).get(id)
        if kisse is not None:
            db.session.delete(kisse)
            db.session.commit()
            return "", 204
        else:
            return "", 404

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True)
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        kisse = db.session.query(models.Kisse).get(id)
        if kisse is not None:
            return kisse.as_dict()
        else:
            return "", 404


class PersonResource(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("kisse_id")
        args = parser.parse_args()

        kisse_id = hashid.get_id_from_hashid(args["kisse_id"])
        person = models.Person(name=args["name"],
                               kisse_id=kisse_id)
        if not self._person_kisse_exists(person):
            return f"No Kisse with id {person.kisse_hashid} exists.", 400
        if not self._person_is_unique_within_kisse(person):
            return f"A person with the name {person.name} already exists in that Kisse.", 400
        else:
            db.session.add(person)
            db.session.commit()

            return person.as_dict(), 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("id")
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        person = db.session.query(models.Person).get(id)
        if person is not None:
            person.name = args["name"]
            db.session.commit()
            return "", 200
        else:
            return "", 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True)
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        person = db.session.query(models.Person).get(id)
        if person is not None:
            db.session.delete(person)
            db.session.commit()
            return "", 204
        else:
            return "", 404

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        person = db.session.query(models.Person).get(id)
        if person is not None:
            return person.as_dict()
        else:
            return "", 404

    def _person_kisse_exists(self, person: models.Person) -> bool:
        kisse = models.Kisse.query.filter_by(id=person.kisse_id).first()
        return kisse is not None

    def _person_is_unique_within_kisse(self, person: models.Person) -> bool:
        kisse = models.Kisse.query.filter_by(id=person.kisse_id).first()
        people = [p.name for p in kisse.people]
        return (kisse is not None) and (person.name not in people)


class ExpenseResource(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("description", required=True)
        parser.add_argument("amount", required=True)
        parser.add_argument("person_id", required=True)
        args = parser.parse_args()

        person_id = hashid.get_id_from_hashid(args["person_id"])
        expense = models.Expense(description=args["description"],
                                 amount=args["amount"],
                                 person_id=person_id)
        if not self._expense_person_exists(expense):
            return f"No Person with id {expense.person_hashid} exists.", 400
        else:
            db.session.add(expense)
            db.session.commit()

            return expense.as_dict(), 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("description")
        parser.add_argument("amount")
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        expense = db.session.query(models.Expense).get(id)
        if expense is not None:
            expense.description = args.get("description", expense.description)
            expense.amount = args.get("amount", expense.amount)
            db.session.commit()
            return "", 200
        else:
            return "", 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True)
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        expense = db.session.query(models.Expense).get(id)
        if expense is not None:
            db.session.delete(expense)
            db.session.commit()
            return "", 204
        else:
            return "", 404

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["id"])
        expense = db.session.query(models.Expense).get(id)
        if expense is not None:
            return expense.as_dict()
        else:
            return "", 404

    def _expense_person_exists(self, expense: models.Expense) -> bool:
        person = models.Person.query.get(expense.person_id)
        return person is not None


class KisseKlyvResource(flask_restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("kisse_id")
        args = parser.parse_args()

        id = hashid.get_id_from_hashid(args["kisse_id"])
        kisse = models.Kisse.query.get(id)
        if kisse is not None:
            return kisse.klyv()
        return "", 404


