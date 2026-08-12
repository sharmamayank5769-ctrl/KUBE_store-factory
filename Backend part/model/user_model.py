from database import get_connection

class user_model():
    def user_getall_model(self):
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        con.close()
        users = [dict(row) for row in result]
        return users

    def user_addone_model(self, data):
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data['username'], data['password'])
        )
        con.commit()
        con.close()
        return {"message": "User added successfully"}

    def user_login_model(self, data):
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (data['username'], data['password'])
        )
        result = cur.fetchone()
        con.close()

        if result:
            return {"status": "success", "message": "Login successful"}
        else:
            return {"status": "failed", "message": "Invalid username or password"}