from flask import Flask, jsonify
from users import users
from test import name


app = Flask(__name__)


@app.route('/')
def greeting():
    return "Hello World!"

@app.route('/hello')
def greeting_hello():
    return "Hi How are you"

@app.route('/greet')
def greeting_greet():
    return "Good Morning"

@app.route('/users', methods=["GET"])
def get_users():
    return jsonify(users)

@app.route('/users/<_id>', methods=["GET"])
def get_user_by_id(_id):
    user = {}
    for user in users:
        if user["id"] == _id:
            return jsonify(user)
    return jsonify({"msg": "user not found"})
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)