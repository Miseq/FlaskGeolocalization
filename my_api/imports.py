from flask import Flask, g, request
import markdown     # konwersja txt to html
import os
import shelve
from flask_restful import Resource, Api, reqparse
import geopy.distance
from my_api.LocationList import LocationList