from flask import Flask, jsonify, request, g, make_response
from dotenv import load_dotenv
import os
import mysql.connector 
from project.user import user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"}), 200

@app.before_request
def before_request():
    try:
        load_dotenv()
        g.db = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
    except Exception as e:
        return jsonify({"error": f"{e}"}), 400

@app.after_request
def after_request(response):
    db = getattr(g, "db", None)
    if db is not None:
        try:
            db.close()
        except Exception as e:
            return make_response(jsonify({"error": f"{e}"}), 400)
    return response

app.register_blueprint(user_bp)