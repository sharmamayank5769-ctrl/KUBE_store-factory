from database import get_connection
from utils import generate_token, hash_password, check_password


class user_model():

    def user_getall_model(self):
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT id, username, created_at FROM users")
        result = cur.fetchall()
        con.close()
        users = [dict(row) for row in result]
        return users

    def user_addone_model(self, data):
        con = get_connection()
        cur = con.cursor()

        hashed_pwd = hash_password(data['password'])

        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data['username'], hashed_pwd)
        )
        con.commit()
        con.close()
        return {"message": "User added successfully"}

    def user_login_model(self, data):
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ?",
            (data['username'],)
        )
        result = cur.fetchone()
        con.close()

        if result and check_password(data['password'], result['password']):
            token = generate_token(data['username'])
            return {"status": "success", "message": "Login successful", "token": token}
        else:
            return {"status": "failed", "message": "Invalid credentials"}