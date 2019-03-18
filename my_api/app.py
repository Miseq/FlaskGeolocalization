from my_api.Location import Location
from my_api.SearchingClosestLocation import SearchingClosestLocation
from my_api.imports import *
from my_api.LocationList import LocationList

app = Flask(__name__)
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open('locations.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/my_api/README', 'r') as index_file:
        content = index_file.read()
        return markdown.markdown(content)


api.add_resource(LocationList , '/locations')
api.add_resource(Location, '/locations/<string:name>')
api.add_resource(SearchingClosestLocation, '/search')