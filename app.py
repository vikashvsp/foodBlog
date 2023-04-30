from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_cors import cross_origin

from mongoengine import SequenceField
import config
password = config.mongopass
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
database_name = "foodBlog"
DB_URI = "mongodb+srv://vkvikashkumar987:{}@cluster0.ncpjepi.mongodb.net/{}?retryWrites=true&w=majority".format(
    password, database_name)
print(DB_URI)
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


class FoodItem(db.EmbeddedDocument):
    food_id = SequenceField(required=True)
    title = db.StringField(required=True)
    photo = db.StringField()
    recipe = db.StringField()
    ingredient = db.StringField()
    cuisineType = db.StringField()
    mealType = db.StringField()
    dietaryRestriction = db.StringField()
    views = db.StringField()
    like = db.StringField()
    comment = db.StringField()
    shared = db.StringField()

    def to_json(self):
        return {
            "food_id": self.food_id,
            "title": self.title,
            "photo": self.photo,
            "recipe": self.recipe,
            "ingredient": self.ingredient,
            "cuisineType": self.cuisineType,
            "mealType": self.mealType,
            "dietaryRestriction": self.dietaryRestriction,
            "views": self.views,
            "like": self.like,
            "comment": self.comment,
            "shared": self.shared
        }


class User(db.Document):
    user_id = db.IntField(required=True, unique=True)
    name = db.StringField(required=True)
    gender = db.StringField(required=True)
    food_ids = db.EmbeddedDocumentListField(FoodItem)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "gender": self.gender,
            "food_ids": [food_item.to_json() for food_item in self.food_ids]
        }


@app.route("/createUser", methods=['POST'])
def db_createUser():
    name = request.json.get("name")
    gender = request.json.get("gender")

    # Find the highest user_id in the database and increment it by 1
    highest_user = User.objects.order_by('-user_id').first()
    if highest_user is None:
        user_id = 1
    else:
        user_id = highest_user.user_id + 1

    user = User(user_id=user_id, name=name, gender=gender)
    user.save()

    return make_response(jsonify(message="User created", user_id=user_id), 201)


@app.route("/addFoodIDs/<int:user_id>", methods=['PATCH'])
# @cross_origin(supports_credentials=True)
def db_addFoodIDs(user_id):

    food_ids = request.json.get("food_ids")

    if not food_ids:
        return make_response(jsonify(message="No food_ids provided"), 400)
    user = User.objects(user_id=user_id).first()
    if not user:
        return make_response(jsonify(message="User not found"), 404)
    for food_id in food_ids:
        food_item = FoodItem(
            title=food_id['title'],
            photo=food_id['photo'],
            recipe=food_id['recipe'],
            ingredient=food_id['ingredient'],
            cuisineType=food_id['cuisineType'],
            mealType=food_id['mealType'],
            dietaryRestriction=food_id['dietaryRestriction'],


        )
        user.food_ids.append(food_item)

    user.save()

    return make_response(jsonify(message="Food IDs added to the user"), 200)


@app.route("/getAllFoodIDs", methods=['GET'])
def db_getAllFoodIDs():
    users = User.objects()
    food_data = []
    for user in users:
        for food_item in user.food_ids:
            food_data.append(food_item.to_json())
    return jsonify(food_data)


if __name__ == '__main__':
    app.run(debug=True)
