@app.route("/addFoodIDs/<int:user_id>", methods=['PATCH'])
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
            views=food_id['views'],
            comment=food_id['comment'],
            shared=food_id['shared'],

        )
        user.food_ids.append(food_item)

    user.save()

    return make_response(jsonify(message="Food IDs added to the user"), 200)