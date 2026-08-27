from database import get_connection

class store_model():
    def store_getall_model(self):
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM stores")
        result = cur.fetchall()
        con.close()

        stores = [dict(row) for row in result]
        return stores

    def store_addone_model(self, data):
        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO stores (store_id, user_id, storage) VALUES (?, ?, ?)",
            (data['store_id'], data['user_id'], data['storage'])
        )
        con.commit()
        con.close()

        return {"message": "Store created successfully"}

    def store_delete_model(self, id):
        con = get_connection()
        cur = con.cursor()

        cur.execute("DELETE FROM stores WHERE id = ?", (id,))
        con.commit()
        con.close()

        return {"message": "Store deleted successfully"}