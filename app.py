from pymongo import MongoClient, DESCENDING
from flask import Flask, render_template, jsonify, request
from flask.json import JSONEncoder
from bson import ObjectId


# ObjectId 부분을 기본 문자열로 바꿔 줍니다
class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


app = Flask(__name__)
app.json_encoder = MongoJSONEncoder

client = MongoClient('localhost', 27017,
                     username='test',
                     password='test',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-1'
                     )
db = client.movieStar

# method :
# 1. GET : 검색
# 2. POST : 추가
# 3. DELETE : 삭제
# 4. PUT : 수정


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
    return jsonify({"stars": stars})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
