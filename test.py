#!/usr/bin/python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

#project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = 'secretkey'
#database_file = "sqlite:///{}".format(os.path.join(project_dir,"test.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/bastien/Desktop/programacion/projecto_final/progrmacion_examen/test.db"

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50),unique=True)
	name = db.Column(db.String(50))
	password = db.Column(db.String(80))
	admin = db.Column(db.Boolean)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(50))
	complete = db.Column(db.Boolean)
	user_id = db.Column(db.Integer)


if __name__ == '__main__':
	app.run(debug=True)
