import argparse
import json
import requests
from flask import request
import pprint
import geocoder
from main import coordinates_correctnes,load_from_file,check_closest_location


def argument_parsing():
    argument_used = False;
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='path_to_file', required=False)
    parser.add_argument('--locations', action='store_true', required=False)
    parser.add_argument('--delete', action='store_true', required=False)
    parser.add_argument('--lat', dest='user_lat', required=False)
    parser.add_argument('--lon', dest='user_lon', required=False)
    parser.add_argument('--ip', action='store_true', required=False)
    parser.add_argument('--input', dest='address_input', type=str, required=False)

    args = parser.parse_args()

    if args.delete:
        resp = requests.delete('http://127.0.0.1:8000/locations').content
        response = str(resp.decode('utf-8'))
        argument_used = True;

    if args.path_to_file:
        uncheked_data = load_from_file(args.path_to_file)
        number_of_locations = 0;
        correct_data = {}
        for location in uncheked_data:
            flag, messeage = coordinates_correctnes(location['latitude'], location['longitude'])
            if flag == 0:
                correct_data["name"] = location["name"]
                correct_data["latitude"] = location["latitude"]
                correct_data["longitude"] = location["longitude"]
                r = requests.post('http://127.0.0.1:8000/locations', json=correct_data)
                number_of_locations += 1
            else:
                print("{0} - {1}, going to another record".format(location['name'], messeage))
        response = "Added {0} locations to list".format(number_of_locations)
        argument_used = True;

    if args.locations:
        resp = requests.get('http://127.0.0.1:8000/locations').content
        response = str(resp.decode('utf-8'))
        argument_used = True;

    if args.user_lat and args.user_lon:
        response = check_closest_location(args.user_lat, args.user_lon)
        argument_used = True;

    if args.ip:
        print("Attention! This method uses IP addres which may give inacurate location!")
        g = geocoder.ip('me')
        print("Program detected your location as {0}, {1}\nNow it will serach closest location".format(g.city, g.state))
        response = check_closest_location(g.latlng[0], g.latlng[1])
        argument_used = True;

    if args.address_input:
        raw_geo = geocoder.osm(args.address_input)
        location = raw_geo.geojson['features'][0]['properties']  # OMG! it's hard to get here
        print('Algorythim, based on your input will search for closest location {0}'.format(location['address']))
        response = check_closest_location(location['lat'], location['lng'])
        argument_used = True;

    if not argument_used:
        response = "No argument was choosen, please try again. Type python main.py --help for manual"

    return response