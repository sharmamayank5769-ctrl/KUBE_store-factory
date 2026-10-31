import re
import time
import threading

from app import app
from flask import request, jsonify
from model.store_model import store_model
from utils import token_required
from database import get_connection
from store_k8s import create_store, delete_store, store_status

obj = store_model()


def _set_status(store_id, status):
    con = get_connection()
    con.execute("UPDATE stores SET status=? WHERE store_id=?", (status, store_id))
    con.commit()
    con.close()


def _provision(store_id, storage):
    """Background mein store banata hai aur ready hone par status update karta hai."""
    try:
        create_store(store_id, storage)
        for _ in range(60):                      # lagbhag 5 minute tak intezaar
            if store_status(store_id) == "ready":
                _set_status(store_id, "ready")
                return
            time.sleep(5)
        _set_status(store_id, "failed")
    except Exception as e:
        print("provision error:", e)
        _set_status(store_id, "failed")


@app.route('/store/getall', methods=['GET'])
@token_required
def store_getall_controller():
    result = obj.store_getall_model()
    return jsonify(result)


@app.route('/store/addone', methods=['POST'])
@token_required
def store_addone_controller():
    data = request.form
    store_id = data.get('store_id', '')
    storage = data.get('storage', '2Gi')

    # store_id namespace ka naam banta hai, isliye sirf chhote akshar + ank allow
    if not re.fullmatch(r"[a-z0-9]{3,20}", store_id):
        return jsonify({"message": "invalid store id"}), 400
    if not re.fullmatch(r"\d{1,3}Gi", storage):
        return jsonify({"message": "invalid storage"}), 400

    result = obj.store_addone_model(data)
    threading.Thread(target=_provision, args=(store_id, storage), daemon=True).start()
    return jsonify(result)


@app.route('/store/delete/<id>', methods=['DELETE'])
@token_required
def store_delete_controller(id):
    # Dashboard row ka id bhejta hai, namespace ke liye store_id chahiye
    con = get_connection()
    row = con.execute("SELECT store_id FROM stores WHERE id=?", (id,)).fetchone()
    con.close()

    if row is not None:
        try:
            delete_store(row["store_id"])
        except Exception as e:
            print("delete error:", e)
            return jsonify({"message": "Kubernetes delete failed: " + str(e)}), 500

    return jsonify(obj.store_delete_model(id))