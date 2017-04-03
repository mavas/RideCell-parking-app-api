import sqlite3, os

import flask
from flask import jsonify, request


app = flask.Flask(__name__)
DATABASE = 'db.sqlite'
if not os.path.exists(DATABASE):
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
    if 'lng' in d and 'lat' in d:
        lng = d['lng']
        lat = d['lat']
        c = sqlite3.connect(DATABASE)
        c.execute('SELECT * from parking_spots where lng = ? and lat = ?', lng, lat)
        for i in c.fetchall():
            r.append(i)
    return jsonify({'available': r})


@app.route('/api/reserve', methods=['POST'])
def reserve():
    a = []
    return jsonify({'reserved': a})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
