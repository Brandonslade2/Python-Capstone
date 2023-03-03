##Models for Jennie's Business Ledger##
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField 
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import UserMixin


db = SQLAlchemy()

##TABLES##

class HomePage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

class EditHomePageForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('submit')
    csrf_token = HiddenField(validators=[DataRequired()])





# class User(db.Model):
#     "A user to access the ledger"

#     __tablename__ = "users"

#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_name = db.Column(db.String, unique=True)
#     user_password = db.Column(db.String)
#     user_description = db.Column(db.String)


class Client(db.Model):
    "A client"

    __tablename__ = "clients"

    client_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    client_name = db.Column(db.String, unique=True)
    client_address = db.Column(db.String)
    client_phonenumber = db.Column(db.BigInteger)


class Service(db.Model):
    "A service offered"

    __tablename__ = "services"

    service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_name = db.Column(db.String, unique=True)
    service_description = db.Column(db.String)

class Pricing(db.Model):
    "A Price"

    __tablename__ = "pricing"

    pricing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pricing_name = db.Column(db.String, unique=True)
    pricing_location = db.Column(db.String)
    pricing_duration = db.Column(db.Integer)
    pricing_price = db.Column(db.Float)

class Enhancement(db.Model):
    "An enhancement that would add to price"

    __tablename__ = "enhancements"

    enhancement_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    enhancement_name = db.Column(db.String, unique=True)
    enhancement_price = db.Column(db.Float)
    enhancement_description = db.Column(db.String)


class History(db.Model):
    "Full Service History"

    __tablename__ = "history"

    history_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    client_name = db.Column(db.String, db.ForeignKey("clients.client_name"))
    service_name = db.Column(db.String, db.ForeignKey("services.service_name"))
    pricing_name = db.Column(db.String, db.ForeignKey("pricing.pricing_name"))
    enhancement_name = db.Column(db.String, db.ForeignKey("enhancements.enhancement_name"))
    history_date = db.Column(db.String)
    history_total_price = db.Column(db.Float)




##OPERATIONS##

#Create first user upon hard reset
def create_first_user(username, email, password_hash):
    user = User(username=username, email=email, password_hash=password_hash)
    return user



def get_user_by_username(username):
    return User.query.filter(User.user_name == username).first()


#Services page
def get_services():
    return Service.query.all()

def create_service(service_name, service_description):

    service = Service(
        service_name=service_name,
        service_description=service_description,
    )
    return service

#Pricing page
def get_pricing():
    return Pricing.query.all()

def create_pricing(pricing_name, pricing_location, pricing_duration, pricing_price):

    pricing = Pricing(
        pricing_name=pricing_name,
        pricing_location=pricing_location,
        pricing_duration=pricing_duration,
        pricing_price=pricing_price,
    )
    return pricing

#Enhancments page
def get_enhancements():
    return Enhancement.query.all()

def create_enhancement(enhancement_name, enhancement_price, enhancement_description):

    enhancement = Enhancement(
        enhancement_name=enhancement_name,
        enhancement_price=enhancement_price,
        enhancement_description=enhancement_description,
    )
    return enhancement

#Clients page
def get_clients():
    return Client.query.all()

def create_client(client_name, client_address, client_phonenumber):

    client = Client(
        client_name=client_name,
        client_address=client_address,
        client_phonenumber=client_phonenumber,
    )
    return client

#History page
def get_history():
    return History.query.all()

#Home page
def create_homepage(content):
    

    homepage = HomePage(
        content=content
    )
    return homepage




# def get_history():
#     history_records = db.session.query(
#     History.history_id,
#     History.history_date,
#     Client.client_name.label('client_name'),  # Use the "name" column of the Clients table
#     Service.service_name.label('service_name'),
#     Pricing.pricing_price.label('pricing_price'),
#     Enhancement.enhancement_name.label('enhancement_name'),
#     History.history_total_price
#     ).join(
#     Client, Service, Pricing, Enhancement
#     ).all()
#     return history_records


# def create_history(client_id, service_id, pricing_id, enhancements, history_date, history_total_price):
#     if not isinstance(enhancements, list):
#         raise TypeError("enhancements must be a list of Enhancement objects")

#     history = History(
#         client_id=client_id,
#         service_id=service_id,
#         pricing_id=pricing_id,
#         enhancements=enhancements,
#         history_date=history_date,
#         history_total_price=history_total_price
#     )
#     return history



#Connect to Database
def connect_to_db(flask_app, db_uri="postgresql://postgres:postgres@localhost:5432/jslmt", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    app.run(debug=True)
    connect_to_db(app)
    
