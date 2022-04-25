import datetime
import jwt
from pymongo import MongoClient
from bson.objectid import ObjectId


def connect(host="localhost", port=27017) -> dict:
    """
    Creates the connection to the database
    """
    try:
        conn = MongoClient(host, port)
        print("Connected successfully to MongoDB!")
        return conn
    except:
        raise Exception("Could not connect to MongoDB...")


def user_exists(db, email) -> bool:
    """
    Checks if a user already exists in the database
    :param db: The database instance.
    :param email: The email of the user.
    """
    query = {"email": email}
    res = db.users.find_one(query)

    if res:
        return True
    else:
        return False


def add_user(db, userData) -> int:
    """
    Adds a user to the database
    :param db: The database instance.
    :param userData: The informations about the user (email, username, password).
    """
    if not user_exists(db, userData["email"]):
        ts = datetime.datetime.now().timestamp()
        db.users.insert_one(
            {
                **userData,
                "created_at": ts,
                "data": {
                    "budget": 100,
                    "payments": {"recurrent": [], "single": []},
                },
            }
        )

        token = jwt.encode(
            {"email": userData["email"], "password": userData["password"]}, "Budget@101#SECRET", algorithm="HS256"
        )

        return {"status": 200, "token": token, "message": "Successfully added user to the database."}
    else:
        return {"status": 409, "message": "User already exists."}


def get_token(db, userData) -> dict:
    """
    Retrieves a user infos
    :param db: The database instance.
    :param userData: The informations about the user (email, username, password).
    """
    query = {"email": userData["email"], "password": userData["password"]}
    res = db.users.find_one(query)

    token = jwt.encode(
        {"email": userData["email"], "password": userData["password"]}, "Budget@101#SECRET", algorithm="HS256"
    )

    if res:
        return {"status": 200, "token": token}
    else:
        return {"status": 409, "message": "Either the user doesn't exist, or the credentials provided are not valid."}


def get_user(db, userData) -> dict:
    """
    Retrieves a user infos
    :param db: The database instance.
    :param userData: The informations about the user (email, username, password).
    """
    query = {"email": userData["email"]}
    res = db.users.find_one(query)

    if res:
        return {"status": 200, "data": res}
    else:
        return {"status": 409, "message": "The user does not exist."}


def update_user(db, userData) -> None:
    """
    Update guild infos in the database
    :param col: The database collection.
    :param userData: The informations about the user (email, username, password).
    """
    query = {"email": userData["email"]}

    if user_exists(db, userData["email"]):
        ts = datetime.datetime.now().timestamp()
        userData.pop("_id")
        updatedGuildData = {**userData, "updated_at": ts}
        db.users.replace_one(query, updatedGuildData)
        return {"status": 200, "message": "Successfully updated the user in the database."}
    else:
        return {"status": 409, "message": "The user does not exist."}
