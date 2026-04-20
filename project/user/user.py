from flask import Blueprint,g

user_bp =  Blueprint('user', __name__)

@user_bp.get('/users')
def get_users():
    try:
        cursor = g.db.cursor(dictionary=True)
        cursor.execute("SELECT id, user_name FROM tbl_user")
        users = cursor.fetchall()
        return {"users": users}, 200
    except Exception as e:
        return {"error": f"{e}"}, 400