import re
import time
import uuid
import threading

from app import app
from flask import request, jsonify
from model.user_model import user_model
from database import get_connection
from store_k8s import create_store, delete_store, store_status

obj = user_model()


# ---------------- User routes (pehle wale, waise hi) ----------------

@app.route('/user/addone', methods=['POST'])
def user_addone_controller():
    data = request.form
    return jsonify(obj.user_addone_model(data))


@app.route('/user/getall', methods=['GET'])
def user_getall_controller():
    result = obj.user_getall_model()
    return jsonify(result)


@app.route('/user/login', methods=['POST'])
def user_login_controller():
    data = request.form
    return jsonify(obj.user_login_model(data))


@app.route('/user/addtwo', methods=['POST'])
def user_addtwo_controller():
    data = request.form
    return jsonify(obj.user_addtwo_model(data))


