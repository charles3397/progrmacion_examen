#!/usr/bin/python3

from flask import Flask, request, jsonify, render_template
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
	nombre = db.Column(db.String(80))
	apellido = db.Column(db.String(80))
	cards = db.relationship('Card', backref='owner')
	
class Card(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	numero = db.Column(db.Integer,unique = True)
	codseguridad = db.Column(db.Integer)
	vencimiento = db.Column(db.Integer)
	montoMaximo = db.Column(db.Float)
	user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

#class Venta(db.Model):
	

@app.route("/", methods=["GET","POST"])
def home():
	if request.form:
        	user = User(nombre=request.form.get("prenom"),apellido=request.form.get("nom"))
        	db.session.add(user)
        	db.session.commit()
	books = User.query.all()
	return render_template("test.html",books=books)

@app.route("/venta", methods=["GET","POST"])
def venta():
	return render_template("venta.html")


if __name__ == '__main__':
	app.run(debug=True)
