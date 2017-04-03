import flask
from flask import jsonify


app = flask.Flask(__name__)


@app.route('/api/available', methods=['GET'])
def list_available():
    a = []
    return jsonify({'available': a})


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
