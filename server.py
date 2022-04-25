import repackage

from db.api import add_user, connect, get_user, update_user, get_token
from utils.parser import parse_json

repackage.up()

import jwt

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

conn = connect(host="localhost")
db = conn.budget101


@app.route("/", methods=["GET"])
def index() -> str:
    return "Backend is running!"


@app.route("/login", methods=["POST"])
def login() -> dict:
    data = request.get_json()

    res = get_token(db, data)

    return res


@app.route("/register", methods=["POST"])
def register() -> dict:
    data = request.get_json()

    res = add_user(db, data)

    return res


@app.route("/getUser", methods=["POST"])
def getUser() -> dict:
    data = request.get_json()

    try:
        decodedToken = jwt.decode(data["token"].replace('"', ""), "Budget@101#SECRET", algorithms=["HS256"])
        userData = get_user(db, decodedToken)

        if userData["status"] == 200:
            return {"status": 200, "data": parse_json(userData["data"]), "message": "Token successfully decoded."}
        else:
            return {
                "status": 409,
                "message": "Token was successfully decoded but user cannot be found in the database.",
            }
    except Exception:
        return {"status": 409, "message": "Token couldn't be decoded."}


@app.route("/updateUserInfos", methods=["POST"])
def updateUserInfos() -> dict:
    data = request.get_json()

    res = update_user(db, data)

    return res


if __name__ == "__main__":
    app.run(debug=True)
