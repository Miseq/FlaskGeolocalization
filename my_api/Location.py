from my_api.imports import *

class Location(Resource):

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = shelve.open('./db/locations.db')
        return db

    def get(self, id):
        db = self.get_db()
        if id in db:
            return {'message': 'Success', 'data': db[id]}, 200
        else:
            return {'message': 'Location not found', 'data': {}}, 404

    def delete(self, id):
        db = self.get_db()
        if id in db:
            del db[id]
            return {'message': 'Deleted', 'data': {}}, 202
        else:
            return {'message': 'Location not found', 'data': {}}, 404