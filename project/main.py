from flask import Blueprint, render_template, request
from . import db
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    token_str = request.args.get('token')

    if not ObjectId.is_valid(token_str):
        return render_template('error.html')

    token = db.Token.find_one({"_id": ObjectId(token_str)})
    
    if token == None:
        return render_template('error.html')

    token['count'] += 1
    db.Token.update_one({"_id": token['_id']},{
    '$set': {
        'count': token['count']
    }})

    return render_template('profile.html', name = db.User.find_one({"_id": token['userID']})['name'], count = token['count'])  

@main.route("/test")
def test():
    db.User.insert_one({"name": "John"})
    return "Connected to the data base!"