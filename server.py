import sqlite3, os

import flask
from flask import jsonify, request


app = flask.Flask(__name__)
DATABASE = 'db.sqlite'
if not os.path.exists(DATABASE):
    print("Creating database.")
    c = sqlite3.connect('db.sqlite')
    c.execute('CREATE TABLE parking_spots (lng, lat, reserved)')
    c.execute('INSERT INTO parking_spots VALUES (2, 4, 0)')
    c.execute('INSERT INTO parking_spots VALUES (6, 1, 0)')
    c.commit()
    c.close()


@app.route('/api/available', methods=['GET'])
def list_available():
    r = []
    d = request.values.to_dict()
    c = sqlite3.connect(DATABASE).cursor()

    if 'lng' in d and 'lat' in d:
        lng = int(d['lng'])
        lat = int(d['lat'])
        q = 'SELECT * from parking_spots where lng = ? and lat = ?'
        c.execute(q, (lng, lat))
        for i in c.fetchall():
            r.append(i)

    elif 'lng' in d and not 'lat' in d:
        lng = int(d['lng'])
        q = 'SELECT * from parking_spots where lng = ?'
        c.execute(q, (lng,))
        for i in c.fetchall():
            r.append(i)

    elif not 'lng' in d and 'lat' in d:
        lat = int(d['lat'])
        q = 'SELECT * from parking_spots where lat = ?'
        c.execute(q, (lat,))
        for i in c.fetchall():
            r.append(i)

    c.close()
    return jsonify({'available': r})


@app.route('/api/reserve', methods=['POST'])
def reserve():
    a = []
    return jsonify({'reserved': a})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
