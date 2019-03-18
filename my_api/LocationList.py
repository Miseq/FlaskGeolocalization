from my_api.imports import *
import json

class LocationList(Resource):
    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = shelve.open('locations.db')
        return db

    def get(self):
        db = self.get_db()
        locations = []

        keys = list(db.keys())
        for key in keys:
            locations.append(db[key])
        return {'message': 'Success', 'data': locations}, 200

    def post(self):
        data = request.get_json()
        db = self.get_db()
        for element in data:
            db[data['name']] = data

        return {'message': 'Success', 'data': data}, 201

    def delete(self):
        db = self.get_db()
        keys = list(db.keys())

        for key in keys:
            del db[key]
        return {'message': 'Destroyed', 'data': {}}, 200