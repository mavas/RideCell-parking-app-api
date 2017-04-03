"""
REST API for listing and/or reserving parking spaces.
"""


import sqlite3, os

import flask
from flask import jsonify, request


__AUTHOR__ = "David Kilgore"


app = flask.Flask(__name__)
DATABASE = 'db.sqlite'
if not os.path.exists(DATABASE):
    print("Creating database.")
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE parking_spots (id, lng, lat, reserved, time)')
    c.execute('INSERT INTO parking_spots VALUES (0, 2, 4, 0, 0)')
    c.execute('INSERT INTO parking_spots VALUES (1, 6, 1, 0, 0)')
    conn.commit()
    conn.close()


@app.route('/api/available', methods=['GET'])
def available():
    """API endpoint for listing available parking spaces.

    curl -X GET
        http://localhost:8000/api/available
        --data "lng=4,lat=9"
    """
    r = []
    d = request.values.to_dict()
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    if 'lng' in d and 'lat' in d:
        lng = int(d['lng'])
        lat = int(d['lat'])
        q = 'SELECT * from parking_spots where lng=? and lat=? and reserved=0'
        c.execute(q, (lng, lat))
        conn.commit()
        for i in c.fetchall():
            r.append(i)

    elif 'lng' in d and not 'lat' in d:
        lng = int(d['lng'])
        q = 'SELECT * from parking_spots where lng=? and reserved=0'
        c.execute(q, (lng,))
        conn.commit()
        for i in c.fetchall():
            r.append(i)

    elif not 'lng' in d and 'lat' in d:
        lat = int(d['lat'])
        q = 'SELECT * from parking_spots where lat=? and reserved=0'
        c.execute(q, (lat,))
        conn.commit()
        for i in c.fetchall():
            r.append(i)

    return jsonify({'available': r})


@app.route('/api/reserve', methods=['POST'])
def reserve():
    """API endpoint for reserving a parking space.

    curl -X POST
        http://localhost:8000/api/reserve
        --data "parking_spot=1&time_range=10"
    """
    d = request.values.to_dict()
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    if 'parking_spot' in d and 'time_range' in d:
        parking_spot = int(d['parking_spot'])
        time_range = int(d['time_range'])
        q = 'UPDATE parking_spots SET reserved=1, time=? WHERE id=?'
        c.execute(q, (time_range, parking_spot))
        conn.commit()

    conn.commit()
    conn.close()
    return jsonify({'reserved': 'success'})


if __name__ == '__main__':
    # python server.py
    app.run(debug=True, port=8000)
