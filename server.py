from flask import Flask, jsonify, request, make_response
import json
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'db.json')

def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return {}

def save_db(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/users/<username>/favorites', methods=['GET','POST','OPTIONS'])
def favorites(username):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    db = load_db()
    users = db.get('users', {})
    if request.method == 'GET':
        user = users.get(username, {})
        return jsonify({'favorites': user.get('favorites', [])})
    # POST: 保存收藏
    try:
        body = request.get_json(force=True)
        fav = body.get('favorites', []) if isinstance(body, dict) else []
    except:
        return jsonify({'error':'invalid body'}), 400
    users.setdefault(username, {})['favorites'] = fav
    db['users'] = users
    save_db(db)
    return jsonify({'ok': True})

@app.route('/api/ping')
def ping():
    return jsonify({'ok': True})

if __name__ == '__main__':
    import sys
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    app.run(host='0.0.0.0', port=port)
