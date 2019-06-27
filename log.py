#!/usr/bin/python3

from flask import Flask, request, jsonify, render_template, redirect, make_response, Response
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user,logout_user, login_required, current_user
import datetime, time
from test import User, Card, Venta

app = Flask(__name__)

#project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = 'secretkey'
#database_file = "sqlite:///{}".format(os.path.join(project_dir,"test.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/bastien/Desktop/programacion/projecto_final/progrmacion_examen/test.db"

db = SQLAlchemy(app)

def compare_date(year1,month1,year2,month2):
	if year1 < year2 :
		return True
	elif year1 == year2 :
		if month1 <= month2 :
			return True
		else :
			return False
	else :
		return False

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	idVenta = db.Column(db.Integer)
	paso = db.Column(db.String(80))
	resultado = db.Column(db.String(80))
	explicacion = db.Column(db.String(80))



def tarjeta(card_id):
	card = Card.query.filter_by(id = card_id).first()
	if not card :
		return jsonify({"codError":"20","error":"No existe la tarjeta"}), 403
	card_date = str(card.vencimiento)
	card_year = int(card_date[:4])
	card_month = int(card_date[4:])
	date = datetime.date.today()
	#if compare_date(2022,date.month,card_year,card_month) == True :
	if compare_date(date.year,date.month,card_year,card_month) == True :
		return True, 201
	else :
		return jsonify({"codError":"21","error":"Tarjeta expirada"}), 403	
		

@app.route("/monto", methods=["GET","POST"])
def monto(card_id , amount ):
	if card_id != None and amount != None :
		value = card_id
		monto = amount
	else :
		value = request.json["tarjeta"]
		monto = float(request.json["monto"])
	card = Card.query.filter_by(id = value).first()
	if not card :
		return jsonify({"codError":"20","error":"No existe la tarjeta"}), 403
	if card.montoMaximo < monto :
		return jsonify({"codError":"30","error":"Monto maximo de venta superado"}), 403
	else :
		return True, 201
	

@app.route("/registro", methods=["GET","POST"])
def log():	
	log = Log(idVenta=request.json["idVenta"],paso=request.json["paso"],resultado=request.json["resultado"])
	venta = Venta.query.filter_by(id = log.idVenta).first()
	card = Card.query.filter_by(id = venta.card_id).first()
	db.session.add(log)
	db.session.commit()
	if log.paso == "verification" and log.resultado == "INFO":
		if not card :
			log.resultado = "FALLO"
			db.session.add(log)
			db.session.commit()
			return jsonify({"codError":"20","error":"No existe la tarjeta"}), 403
		else :
			log.resultado = "OK"
			db.session.add(log)
			db.session.commit()
	return ""
							
		
	
if __name__ == '__main__':
	app.run(debug=True)

