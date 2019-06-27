#!/usr/bin/python3

from flask import Flask, request, jsonify, render_template, redirect, make_response, Response
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user,logout_user, login_required, current_user
import datetime, time
from test import User, Card

app = Flask(__name__)

#project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = 'secretkey'
#database_file = "sqlite:///{}".format(os.path.join(project_dir,"test.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/bastien/Desktop/programacion/projecto_final/progrmacion_examen/test.db"

db = SQLAlchemy(app)

def compare_date(year1,month1,year2,month2):
	

@app.route("/tarjeta", methods = ["GET","POST"] )
def tarjeta():
	value = request.json["tarjeta"]
	card = Card.query.filter_by(id = value).first()
	if not card :
		return jsonify({'error':"pas de carte"})
	return jsonify({'vencimiento':card.vencimiento})
	card_year = card.vencimiento[:4]
	card_month = card.vencimiento[4:]
	date = datetime.date.today()	
	if card :
		return jsonify({'vencimiento':card.vencimiento})
	return value


if __name__ == '__main__':
	app.run(debug=True)

