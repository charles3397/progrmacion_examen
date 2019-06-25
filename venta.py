#!/usr/bin/python3

import os

from flask import Flask , render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Error(db.Model):
	id = db.Column(db.Integer, primary_key=True,)
	title = db.Column(db.String(80), unique=True, nullable=False)

	def get_codError(self):
	    	return format(self.codError)
	
	def get_error(self):
		return format(self.title)
	
	def ErrorJSON(self):
		buf = '{' + '"codError":' +'"'+format(self.codError)+ '","error:"' + '"' + format(self.error) + '"}'  


@app.route("/", methods=["GET","POST"])
def Add():
	if request.form:
        	error = Error(title=request.form.get("title"))
        	db.session.add(error)
        	db.session.commit()
	errors = Error.query.all()
	return render_template("venta.html",errors=errors)

cul = '''

@app.route("/update", methods=["POST"])
def update():
	newtitle = request.form.get("newtitle")
	oldtitle = request.form.get("oldtitle")
	book = Book.query.filter_by(title=oldtitle).first()
	book.title = newtitle
	db.session.commit()
	return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

'''

if __name__ == "__main__":
	app.run(debug=True)


