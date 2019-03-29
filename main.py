import argparse
import json
import requests
from flask import request
import pprint
import geocoder
from arguments import *

def load_from_file(file='test_locations.json'):
    try:
        with open(file) as json_file:
            data = json.load(json_file)
        return data
    except:
        print("Can't load data from file")
        exit(404)


# Function which  formats given arguments into json dict and sends it for calculating
def check_closest_location(latitude, longitude):
    flag, messege = coordinates_correctnes(latitude, longitude)
    if flag == 0:
        lat = str(latitude)
        lon = str(longitude)
        coordinates_json = {}
        coordinates_json['latitude'] = lat
        coordinates_json['longitude'] = lon
        response = requests.post('http://127.0.0.1:8000/search', json=coordinates_json)
        return response.json()['data']
    else:
        print(messege)
        exit()


# Checks if given arguments are correct
def coordinates_correctnes(latitude, longitude):
    lat = float(latitude)
    lon = float(longitude)
    if lat < -90.0 or lat > 90.0:
        return 1, "Wrong value of latitude!"
    elif lon < -180.0 or lon > 180.0:
        return 2, "Wrong value of longitude!"
    else:
        return 0, "Coordinates are correct"


def main(*args, **kwargs):
    server_response = argument_parsing(*args, **kwargs)
    print(server_response)


if __name__ == '__main__':
    main()