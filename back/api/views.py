from flask import Flask, request
from flask_cors import CORS, cross_origin

import mongoDB.manageDB as manager
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def helloWorld():
    return 'Hello from flask'


@app.route('/login', methods=['POST'])
def loginUser():
    userDetails = request.get_json()
    print(userDetails)
    if manager.verifyUser(userDetails):
        return 'User data', 200
    else:
        return 'Bad credentials', 401


@app.route('/getUserData', methods=['POST'])
def getData():
    getUserName = request.get_json()
    print(getUserName)
    data = manager.load_all_series(userName=getUserName['username'])
    return json.dumps(data)


if __name__ == '__main__':
    app.run()
