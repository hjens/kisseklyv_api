import flask_restful
from flask_restful import reqparse
from kisseklyv import app
from kisseklyv import models
from kisseklyv import db


class KisseResource(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("description")
        args = parser.parse_args()

        kisse = models.Kisse(description=args["description"])
        db.session.add(kisse)
        db.session.commit()

        return {"message": "Kisse created",
                "data": kisse.as_dict()}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("kisse_id", required=True)
        parser.add_argument("description", required=True)
        args = parser.parse_args()

        kisse = db.session.query(models.Kisse).get(args["kisse_id"])
        if kisse is not None:
            kisse.description = args["description"]
            db.session.commit()
            return "", 200
        else:
            return "", 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("kisse_id", required=True)
        args = parser.parse_args()

        kisse = db.session.query(models.Kisse).get(args["kisse_id"])
        if kisse is not None:
            db.session.delete(kisse)
            db.session.commit()
            return "", 204
        else:
            return "", 404


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("kisse_id", required=True)
        args = parser.parse_args()

        kisse = db.session.query(models.Kisse).get(args["kisse_id"])
        if kisse is not None:
            return {"message": "Get Kisse",
                    "data": kisse.as_dict()}
        else:
            return "", 404


class PersonResource(flask_restful.Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class ExpenseResource(flask_restful.Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class KisseKlyv(flask_restful.Resource):
    def get(self):
        pass


