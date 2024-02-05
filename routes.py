from flask import jsonify, Blueprint, request
from sqlalchemy.orm import Session
from connection import engine
from repository import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from ServiceAndUtility import *
from datetime import datetime

app = Blueprint('routes', __name__)


@app.route('/')
def index():
    return jsonify({"status": "Raising the server"}), 201


# -----------Auth--------------------

@app.route('/auth/sign-up', methods=["POST"])
def sign_up():
    data = request.get_json()
    data['password'] = convert_to_hash(data["password"])
    user = Personal(user_name=data['user_name'], password=data['password'], role=data['role'], salary=data['salary'],
                    first_name=data['first_name'], last_name=data['last_name'], age=data['age'], created_at=datetime.utcnow())
    result = personal_add(user)
    if result is None:
        return jsonify({"status": "Success "}), 201
    return result


@app.route('/auth/sign-in', methods=["POST"])
def sign_in():
    data = request.get_json()
    user_name = data['user_name']
    password = data['password']
    user = check_user(user_name, password)

    if user is None:
        return jsonify({"status": "Incorrect username or password "}), 400

    user_id, claim = user
    claim = {"role": claim}

    token = create_access_token(identity=user_id, additional_claims=claim)

    return jsonify(access_token=token), 200


# ----------end Auth "Not done"------------------


# ------------MENU------------------------------
@app.route('/menu', methods=['POST'])
@jwt_required()
def menu_add_route():
    """
    correcting jwt_required
    """
    user_id = get_jwt_identity()
    role = get_jwt()['role']

    if role not in ['admin', 'manager']:
        return jsonify({"status": "You don't have acces to this page"}), 404

    data = request.get_json()
    result = menu_add(data['title'], data['category'],
                      data['description'], data['status'], data['price'], author_id=user_id)
    if result is not None:
        return jsonify({"status": "Some problems in data"}), 404

    return jsonify({"status": "Successfully done"}), 201


@app.route("/menu", methods=['GET'])
def menu_get_route():
    names_dict = {
        "title": "",
        "description": "",
        "category": "",
        "id": "",
        "price": "",
        "status": ""
    }
    for i in ["title", "description", "category", "id", "price", "status"]:
        if request.args.get(i) is not None:
            names_dict[i] = request.args.get(i)

    result = menu_result(names_dict["title"], names_dict["description"],
                         names_dict["category"], names_dict["id"], names_dict["price"], names_dict["status"])
    if type(result) is not list:
        return jsonify({"status": "while querying something went wrong please correctly check"}), 404

    return jsonify({"result": result}), 201


@app.route("/menu", methods=["PUT"])
@jwt_required()
def menu_update_route():
    role = get_jwt()['role']
    if role not in ['admin', 'manager']:
        return jsonify({"status": "You don't have acces to this page"}), 404

    data = request.get_json()
    return menu_update(data)


@app.route("/menu/<int:_id>", methods=["DELETE"])
@jwt_required()
def menu_delete_route(_id):
    role = get_jwt()['role']
    if role not in ['admin', 'manager']:
        return jsonify({"status": "You don't have acces to this page"}), 404
    return menu_delete(_id)

# -------------end MENU not done---------------------------------


# -------------TABLES------------------------------

@app.route('/tables', methods=["POST"])
@jwt_required()
def table_create_route():

    user_id = get_jwt_identity()
    role = get_jwt()['role']
    if role not in ['admin', 'manager']:
        return jsonify({"status": "You don't have acces to this page"}), 404

    data = request.get_json()
    table_number = data['table_number']
    result = table_add(table_number, author_id=user_id)
    if result is None:
        return jsonify({"status": "Successfully"}), 201
    return result


@app.route("/tables", methods=["GET"])
def table_read_route():
    result = table_read()
    return jsonify({"result": result}), 201


@app.route('/tables/<int:id>', methods=["DELETE"])
@jwt_required()
def table_delete_route(id):
    role = get_jwt()['role']
    if role not in ['admin', 'manager']:
        return jsonify({"status": "You don't have acces to this page"}), 404
    return table_delete(id)


# ------------end TABLES------------------------


# ------------PERSONAL--------------------------

@app.route("/personal/<int:id>/info", methods=["GET"])
def personal_read_by_id_route(id):
    return jsonify(result=personal_read(id))


@app.route("/personal", methods=["GET"])
def personal_read_route():
    return jsonify(result=personal_read())


@app.route("/personal/<int:id>", methods=["PUT"])
@jwt_required()
def personal_update_route(id):
    role = get_jwt()
    if role not in ['admin', 'manager']:
        return jsonify({'status': "You don't have access to update"}), 400
    data = request.get_json()
    changes = personal_update(id, data)
    if changes is None:
        return jsonify({"status": "Success"}), 201
    return changes


@app.route("/personal", methods=['DELETE'])
@jwt_required()
def personal_delete_route():
    id = request.get_json()['id']
    role = get_jwt()['role']
    if role not in ['admin', 'manager']:
        return jsonify({"status": "You don't have access to delete"}), 400
    is_deleted = personal_delete(id)
    if is_deleted is None:
        return jsonify({"status": "Success"}), 201
    return is_deleted

# ------------end PERSONAL--------------------------




