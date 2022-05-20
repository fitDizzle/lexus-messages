from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import os
import re

app = Flask(__name__)

ENV = 'dev'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ConnorClark123!!@localhost/lexus'
else:
    uri = os.getenv('postgres://efhunvhahuwfuw:9899b7fca3b499f0d411bb12ddfe935fb99302c58a517e4ba0867f9e180c031c@ec2-3-209-124-113.compute-1.amazonaws.com:5432/d5r1bqpu2acqio')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200), unique=False)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments        
    

@app.route('/')
def index():
    return render_template('index.html')

# Routes
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        
        print(customer, dealer, rating, comments)
        
        if customer == '' or dealer == '':
            return render_template('index.html', message="Please enter required fields")
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message="You have already submitted feedback")


if __name__ == '__main__':
    app.run()
    
