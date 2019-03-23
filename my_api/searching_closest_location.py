from flask import g, request
import shelve
from flask_restful import Resource
import geopy.distance


class SearchingClosestLocation(Resource):
    @staticmethod
    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = shelve.open('./db/locations.db')
        return db

    def post(self):
        db = self.get_db()
        locations = list(db.keys())
        closest_location = None
        closest_place = ""
        user_data = request.get_json()

        latitude_user = float(user_data['latitude'])
        longitude_user = float(user_data['longitude'])

        for key in locations:
            location = db[key]

            distance = self.calculate(latitude_user, longitude_user, location.get('latitude'), location.get('longitude'))

            if not closest_location or distance < closest_location:
                closest_location = distance
                closest_place = location
                closest_latitude = closest_place['latitude']
                closest_name = closest_place['name']
                closest_longitude = closest_place['longitude']
        response = "Closest location: {0}, with coordinates: latitude {1}, longitude {2},estimeted distance in km: {3}"
        response.format(closest_name, closest_latitude, closest_longitude, str(distance))   # TODO make it less ugly

        if closest_place is not "":
            return {'message': 'Success', 'data': response}, 201
        else:
            return {'message': 'Failed', 'data': {}}, 404

    @staticmethod
    def calculate(self, lat_u, lon_u, lat_l , lon_l):
        coordinates_user = (float(lat_u), float(lon_u))
        coordinates_location = (float(lat_l), float(lon_l))

        return geopy.distance.distance(coordinates_user, coordinates_location).km

