from flask import jsonify, Blueprint, request
from sqlalchemy.orm import Session
from connection import engine
from repository import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt


app = Blueprint('routes', __name__)


@app.route('/')
def index():
    return jsonify({"status": "Raising the server"}), 201


# -----------Auth--------------------

@app.route('/auth/sign-up')
def sign_up():
    pass


@app.route('/auth/sign-in')
def sign_in():
    pass


# ----------end Auth "Not done"------------------


# ------------MENU------------------------------
@app.route('/menu', methods=['POST'])
# @jwt_required
def menu_add_route():
    """
    correcting jwt_required
    """

    data = request.get_json()
    result = menu_add(data['title'], data['category'],
                      data['description'], data['status'], data['price'])
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
def menu_update_route():
    data = request.get_json()
    return menu_update(data)


@app.route("/menu/<int:_id>", methods=["DELETE"])
def menu_delete_route(_id):
    return menu_delete(_id)

# -------------end MENU not done---------------------------------


# -------------TABLES------------------------------

@app.route('/tables', methods=["POST"])
def table_create_route():
    data = request.get_json()
    print(data)
    table_number = data['table_number']
    result = table_add(table_number)
    if result is None:
        return jsonify({"status":"Successfully"}),201
    return result


@app.route("/tables", methods=["GET"])
def table_read_route():
    result = table_read()
    return jsonify({"result": result}), 201


@app.route('/tables/<int:id>', methods=["DELETE"])
def table_delete_route(id):
    return table_delete(id)


# ------------end TABLES------------------------
