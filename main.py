from flask import Flask, render_template, flash, request, redirect ,url_for
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	contact=db.Column(db.String(12), nullable=False, unique=True)

	def __init__(self,name,email,contact):
		self.name=name
		self.email=email
		self.contact=contact

@app.route('/')
def Index():
    all_data = Users.query.all()
 
    return render_template("index.html", contact = all_data)


	
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
 
 
        my_data = Users(name, email, contact)
        db.session.add(my_data)
        db.session.commit()
 
        flash("User Inserted Successfully")
 
        return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Users.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.contact = request.form['contact']
 
        db.session.commit()
        flash("Updated Successfully")
 
        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Users.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Deleted Successfully")
 
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)