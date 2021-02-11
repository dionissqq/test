from flask import Flask
import pymongo
import dns
from flask_mail import Mail, Message
# init SQLAlchemy so we can use it later in our models

CONNECTION_STRING = 'mongodb+srv://user:mytestpass@cluster0.n5wao.mongodb.net/test?retryWrites=true&w=majority'

app = Flask(__name__)
mail= Mail(app)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sometest232422@gmail.com'
app.config['MAIL_PASSWORD'] = 'mynewpasstest'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('test')

# db.init_app(app)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
