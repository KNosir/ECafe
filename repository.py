from flask import jsonify
from sqlalchemy.orm import Session
from models import *
from datetime import datetime
from connection import engine
from sqlalchemy import and_
from ServiceAndUtility import convert_to_hash

# --------------MENU--------------


def menu_add(_title: str, _category: str, _description: str, _status: str, _price: float):
    try:
        with Session(autoflush=False, bind=engine) as db:
            db.add(Menu(title=_title, category=_category, description=_description,
                        status=_status, price=_price))
            db.commit()
    except Exception as err:
        return err


def menu_result(_title, _description, _category, _id, _price, _status) -> list:
    with Session(bind=engine, autoflush=False) as db:
        result = db.query(Menu).filter(and_(Menu.is_deleted == False, Menu.title.ilike(f"%{_title}%"), Menu.description.ilike(
            f"%{_description}%"), Menu.category.ilike(f"%{_category}%"), Menu.id.ilike(f"%{_id}%"), Menu.price.ilike(f"%{_price}%"), Menu.status.ilike(f"%{_status}%"))).all()
        send_data = []
        try:
            for i in result:
                i = i.__dict__
                del i['_sa_instance_state']
                send_data.append(i)
        except Exception as e:
            return e
    return send_data


def menu_update(new_changes: dict):
    with Session(autoflush=False, bind=engine) as db:
        menu_id = db.query(Menu).filter(
            and_(Menu.id == new_changes["id"], Menu.is_deleted == False)).first()
        if menu_id is not None:
            del new_changes["id"]
            for k, m in new_changes.items():
                if hasattr(menu_id, k):
                    setattr(menu_id, k, m)
            db.commit()
            return jsonify({"status": "Done successfuly"}), 201
        else:
            return jsonify({"status": "Menu not found"}), 404

    return jsonify({"status": "Something went wrong"}), 500


def menu_delete(_id: int):
    with Session(autoflush=False, bind=engine) as db:
        deleted = db.query(Menu).filter(
            and_(Menu.id == _id, Menu.is_deleted == False)).first()
        if deleted is not None:
            deleted.is_deleted = True
            db.commit()
            return jsonify({"status": "Done successfully"}), 201
        else:
            return jsonify({"status": "Not found"}), 404


# ------------end Menu-------------


# ----------TABLES------------------

def table_add(_table_number: int, _author_id: int):
    try:
        with Session(autoflush=False, bind=engine) as db:
            db.add(TableManagement(
                table_number=_table_number, authod_id=_author_id))
            db.commit
    except Exception as err:
        return err


def table_read():
    with Session(autoflush=False, bind=engine) as db:
        result = db.query(TableManagement).filter(
            TableManagement.is_deleted == False).all()
        free_list = []
        for i in result:
            i = i.__dict__
            del i['_sa_instance_state']
            free_list.append(i)
    return free_list


def table_delete(_id):

    with Session(autoflush=False, bind=engine) as db:
        result = db.query(TableManagement).filter(
            and_(TableManagement.id == _id, TableManagement.is_deleted == False)).first()
        if result is not None:
            result.is_deleted = True
            db.commit()
            return jsonify({"status": "Successfully"}), 201
        return jsonify({'status': "Something went wrong "}), 404


# --------end TABLES----------------


# --------PERSONAL--------------------

def personal_add(personal):
    try:
        with Session(autoflush=False, bind=engine) as db:
            db.add(personal)
            db.commit()
    except Exception as err:
        db.rollback()
        return err


def personal_read(_id=""):
    try:
        with Session(autoflush=False, bind=engine) as db:
            result = db.query(Personal).filter(
                and_(Personal.id.ilike(f"%{_id}%"), Personal.is_deleted == False))
            free_list = []
        for i in result:
            i = i.__dict__
            del i['_sa_instance_state']
            free_list.append(i)
        return free_list

    except Exception as err:
        print(err)
        return None


def personal_update(_id: int, new_changes: dict):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = db.query(Personal).filter(
                and_(Personal.id == _id, Personal.is_deleted == False))
            for k, v in new_changes.items():
                if hasattr(user, k):
                    setattr(user, k, v)
            db.commit()
            return None
    except:
        db.rollback
        return jsonify({"status": "User not found or something went wrong"}), 400


def personal_delete(_id):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = db.query(Personal).filter(
                and_(Personal.id == _id, Personal.is_deleted == False)).first()
            user.is_deleted = True
            db.commit()
            return None

    except Exception as err:
        print(err)
        return jsonify({"status": "Something went wrong please check it "}), 400


def check_user(_user_name, _password):
    _password = convert_to_hash(_password)
    try:
        with Session(autoflush=False, bind=engine) as db:

            result = db.query(Personal).filter(and_(Personal.user_name ==
                                                    _user_name, Personal.password == _password)).first()
            return result.id, result.role
    except Exception as err:
        return None


# --------end PERSONAL------------------
