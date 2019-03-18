import argparse
import json
import requests
from flask import request
import pprint
import geocoder


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
        return 1,"Wrong value of latitude!"
    elif lon < -180.0 or lon > 180.0:
        return 2,"Wrong value of longitude!"
    else:
        return 0,"Coordinates are correct"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',dest='path_to_file', required=False)
    parser.add_argument('--locations', action='store_true',  required=False)
    parser.add_argument('--delete', action='store_true', required=False)
    parser.add_argument('--lat', dest='user_lat', required=False)
    parser.add_argument('--lon', dest='user_lon', required=False)
    parser.add_argument('--ip', action='store_true',required=False)
    parser.add_argument('--input', dest='address_input', type=str,required=False)

    args = parser.parse_args()

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

    if args.locations:
        resp = requests.get('http://127.0.0.1:8000/locations').content
        response = str(resp.decode('utf-8'))


    if args.delete:
        resp = requests.delete('http://127.0.0.1:8000/locations').content
        response = str(resp.decode('utf-8'))

    if args.user_lat and args.user_lon:
        response = check_closest_location(args.user_lat, args.user_lon)

    if args.ip:
        print("Attention! This method uses IP addres which may give inacurate location!")
        g = geocoder.ip('me')
        print("Program detected your location as {0}, {1} \nNow it will serach closest location".format(g.city, g.state))
        response = check_closest_location(g.latlng[0], g.latlng[1])

    if args.address_input:
        raw_geo = geocoder.osm(args.address_input)
        location = raw_geo.geojson['features'][0]['properties']     # OMG! it's hard to get here
        print('Algorythim, based on your input will search for closest location {0}'.format(location['address']))
        response = check_closest_location(location['lat'], location['lng'])

    if args is None:
        response = "No argument was choosen, please try again. Type python main.py --help for manual"

    print(response)


if __name__ == '__main__':
    main()