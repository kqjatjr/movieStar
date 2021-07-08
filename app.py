from pymongo import MongoClient, DESCENDING
from flask import Flask, render_template, jsonify, request
from flask.json import JSONEncoder
from bson import ObjectId


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


app = Flask(__name__)
app.json_encoder = MongoJSONEncoder

client = MongoClient('localhost', 27017)
db = client.movieStar


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/star/<id>/like', methods=['PUT'])
def postStarLike(id):
    star = db.mystar.find_one({'_id': ObjectId(id)})
    likeUp = star['like'] + 1
    db.mystar.update_one({'_id': ObjectId(id)}, {'$set': {'like': likeUp}})
    return jsonify({'success': True})


@app.route('/api/star/<id>', methods=['DELETE'])
def postStarDelete(id):
    db.mystar.delete_one({'_id': ObjectId(id)})
    return jsonify({'success': True})


@app.route('/api/star/list', methods=['GET'])
def getStarList():
    stars = list(db.mystar.find({}).sort(
        "like", DESCENDING))
    return jsonify({"Star": stars})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
