from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

users = []
user_id_counter = 1

class UserList(Resource):
    def get(self):
        return users

    def post(self):
        global user_id_counter
        data = request.get_json()
        user = {"id": user_id_counter, "name": data["name"], "email": data["email"]}
        users.append(user)
        user_id_counter += 1
        return user, 201

class User(Resource):
    def get(self, id):
        for user in users:
            if user["id"] == id:
                return user
        return {"message": "User not found"}, 404

    def put(self, id):
        data = request.get_json()
        for user in users:
            if user["id"] == id:
                user["name"] = data["name"]
                user["email"] = data["email"]
                return user
        return {"message": "User not found"}, 404

    def delete(self, id):
        global users
        users = [user for user in users if user["id"] != id]
        return {"message": "User deleted"}

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")

if __name__ == "__main__":
    app.run()