from Location import Location
from SearchingClosestLocation import SearchingClosestLocation
from imports import *
from LocationList import LocationList

app = Flask(__name__)
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open('./db/locations.db')
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