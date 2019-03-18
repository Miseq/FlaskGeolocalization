Skrócona dokumentacja zadnia:


********************************
Files
*******************************
    /main.py - It is responsible for client side
    /requirements.txt - output of <pip list> dropped into the file
    /test_locations.json - File which contains a short list of sample locations, ready to use.


    /my_api/_init_.py - Responsible for starting a server
    /my_api/app.py - Creating Flask object, starting connection with database, droping it, responsible for making paths
    /my_api/import.py - contains all the imports used in this subdirectory
    /my_api/Location.py - Single location entity,
    /my_api/LocationList.py - It allows to create, get, modyify and drop list(dict) of locations, here goes most of the requests
   /my_api/README - Describes way in which this Rest server works, for example how every response looks
   /my_api/SearchingClosestLocation.py - Using a geopy package, calculates the distance between the coordiantes from the database and the user data received in POST, and then returns the name(and coordiantes, and distance) of the nearest location,

   /db - Contains database build from shelve package. https://docs.python.org/3/library/shelve.html


**************************************
How it Works
**************************************

    1. Starting a serwer: ./my_api python __init__.py
    2. Showing arguments for client: ./python main,py --help
    3. Checking if database exists, returns all records: ./python main.py --locations
        3a) If database dosen't exist we can upload any .json file with correct structure by:
            ./python main.py --file path_to_file.json
            structure of file:
            [
                {
                    "name": "example"
                    "latitude": "42.00"
                    "longitude": "-42.00"
                },
                {
                ...
                }
            ]
        3b) If there are some records but we want to wipe them all: ./python main.py --delete
    4.Sending our localization.
        4a) Typing our own geo coordinates:
            ./python main.py --lat 42.00 --lon 42.00
        4b) Auto getting and sending our coordinates from IP address(precision may veary):
            ./python main.py --auto
        4c) By typing full or part of the addres we can get very precise coordinates, it uses OpenStreetMap https://www.openstreetmap.org
            Accepts polish letters('ąęćź....')
            ./python main.py -- input "Address"
    5. Getting response from server.


**************************************************************
Sample of sending address and gettting response from server:
******************************************************************

- (zadanie_servocode) D:\Programming\Python\Servocode>python main.py --input "Area 51"
- Algorythim, based on your input will search for closest location Air Force Flight Test Center (Detachment 3), 4th Street, Lincoln County,
 Nevada, USA
- Closest location: miejsce5, with coordinates: latitude 50.013, longitude 150.24,estimeted distance in km: 7205.231956837128




