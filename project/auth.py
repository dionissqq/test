from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, mail, Message

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    user_email = request.form.get('email')
    user = db.User.find_one({"email": user_email})
    print('here')
    print(user)
    if user == None:
        print('there')
        flash('email is not registrated')
        return redirect(url_for('auth.login'))

    newToken = db.Token.insert_one({'userID':user['_id'], 'count' : 0})
    print(newToken)
    msg = Message('magic', sender = 'sometest232422@gmail.com', recipients = [user_email])
    msg.body = "link - " + request.url_root + 'profile?token=' + str(newToken.inserted_id)
    mail.send(msg)

    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    user_email = request.form.get('email')
    name = request.form.get('name')

    user = db.User.find_one({"email": user_email}) # if this returns a user, then the email already exists in database
    print(user)
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    db.User.insert_one({"name": name, "email": user_email})

    return redirect(url_for('auth.login'))
@auth.route('/logout')
def logout():
    return 'Logout'