#!/usr/bin/python3

from flask import Flask, request, jsonify, render_template, redirect, make_response, Response
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user,logout_user, login_required, current_user


app = Flask(__name__)

#project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = 'secretkey'
#database_file = "sqlite:///{}".format(os.path.join(project_dir,"test.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/bastien/Desktop/programacion/projecto_final/progrmacion_examen/test.db"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80))
	apellido = db.Column(db.String(80))
	cards = db.relationship('Card', backref='user')
	
class Card(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	numero = db.Column(db.Integer,unique = True)
	codseguridad = db.Column(db.Integer)
	vencimiento = db.Column(db.Integer)
	montoMaximo = db.Column(db.Float)
	user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
	ventas = db.relationship('Venta',backref='card')

class Venta(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
	card_id = db.Column(db.Integer,db.ForeignKey("card.id"))
	monto = db.Column(db.Integer)
	
	
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/login')
def index():
	user = User.query.filter_by(id=1).first()
	if user :	
		login_user(user)
		return "you are now logged in"
	else :
		return "jambon"
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return "you are logged out!"

@app.route("/who")
@login_required
def who():
	return "the current user is " + current_user.nombre


	

@app.route("/card", methods=["GET","POST"])
@login_required
def add_card():
	user = current_user
	if request.form.get("numero") and request.form.get("codseguridad") and request.form.get("vencimiento") and request.form.get("montoMaximo"):
		card = Card(numero=request.form.get("numero"),codseguridad=request.form.get("codseguridad"),vencimiento=request.form.get("vencimiento"),montoMaximo=request.form.get("montoMaximo"),user_id=user.id)
		db.session.add(card)
		db.session.commit()	
	books = Card.query.filter_by(user_id=user.id)
	return render_template("card.html",books=books)



	
@app.route("/card/update", methods=["POST"])
def update():
	newnumero = request.form.get("newnumero")
	oldnumero = request.form.get("oldnumero")
	card = Card.query.filter_by(numero=oldnumero).first()
	card.numero = newnumero
	newcodseguridad = request.form.get("newcodseguridad")
	oldcodseguridad = request.form.get("oldcodseguridad")
	card = Card.query.filter_by(codseguridad=oldcodseguridad).first()
	card.codseguridad = newcodseguridad
	newvencimiento = request.form.get("newvencimiento")
	oldvencimiento = request.form.get("oldvencimiento")
	card = Card.query.filter_by(vencimiento=oldvencimiento).first()
	card.vencimiento = newvencimiento
	newmontoMaximo = request.form.get("newmontoMaximo")
	oldmontoMaximo = request.form.get("oldmontoMaximo")
	card = Card.query.filter_by(montoMaximo=oldmontoMaximo).first()
	card.montoMaximo = newmontoMaximo
	db.session.commit()
	return redirect("/card")


@app.route("/card/delete", methods=["POST"])
def delete_card():
    numero = request.form.get("numero")
    card = Card.query.filter_by(numero=numero).first()
    db.session.delete(card)
    db.session.commit()
    return redirect("/card")

@app.route("/", methods=["GET","POST"])
def front():
	return render_template("front.html")

@app.route("/admin/user", methods=["GET","POST"])
def home():
	if request.form:
        	user = User(nombre=request.form.get("prenom"),apellido=request.form.get("nom"))
        	db.session.add(user)
        	db.session.commit()
	books = User.query.all()
	return render_template("test.html",books=books)




def check_auth(username, password):
	return username == 'admin' and password == 'admin'

def authenticate():
	return Response('Could not verify your access level for that URL.\n''You have to login with proper credentials', 401,{'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_admin(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated




@app.route("/venta", methods=["GET","POST"])
@requires_admin
def venta():
	return render_template("venta.html")

@app.route("/buy<id>", methods=["GET","POST"])
@login_required
def buy(id):
	card = Card.query.filter_by(id=int(id)).first()
	if not card :
		return jsonify({'message':'No card found'})
	return jsonify({'cliente':card.user_id,'numero':card.numero,'monto':1000})


if __name__ == '__main__':
	app.run(debug=True)
