from app import app
from flask import request, jsonify
from model.store_model import store_model

obj = store_model()

@app.route('/store/getall', methods=['GET'])
def store_getall_controller():
    result = obj.store_getall_model()
    return jsonify(result)

@app.route('/store/addone', methods=['POST'])
def store_addone_controller():
    data = request.form
    return jsonify(obj.store_addone_model(data))

@app.route('/store/delete/<id>', methods=['DELETE'])
def store_delete_controller(id):
    return jsonify(obj.store_delete_model(id))