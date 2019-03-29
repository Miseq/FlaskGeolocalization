from flask import g
import shelve
from flask_restful import Resource


class Location(Resource):

    @staticmethod
    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = shelve.open('./db/locations.db')
        return db

    def get(self, key):
        db = self.get_db(self)
        if key in db:
            return {'message': 'Success', 'data': db[key]}, 200
        else:
            return {'message': 'Location not found', 'data': {}}, 404

    def delete(self, key):
        db = self.get_db(self)
        if key in db:
            del db[key]
            return {'message': 'Deleted', 'data': {}}, 202
        else:
            return {'message': 'Location not found', 'data': {}}, 404
