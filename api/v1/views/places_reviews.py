@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    required_fields = ['user_id', 'text']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return make_response(jsonify({'error': f"Missing fields: {', '.join(missing_fields)}"}), 400)

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)
