from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #Minuto 11
ma = Marshmallow(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, unique = True,primary_key = True) #ID del Usuario
    code = db.Column(db.String(100), nullable = False) #Codigo Alfanumerico
    name = db.Column(db.String(100), nullable = False) #Nombre
    surname = db.Column(db.String(100), nullable = False) #Apellido
    gender = db.Column(db.String(100), nullable = False)   # Genero
    phone = db.Column(db.Integer, nullable = True) #Numero
    email = db.Column(db.String(100), nullable = False) #Email
    password = db.Column(db.String(100), nullable = False) #Contraseña
    pic_url = db.Column(db.String(10000), nullable = False) # Foto de Perfil
    admin = db.Column(db.Boolean, nullable = False)     #Si es administrador
    prof = db.Column(db.Boolean, nullable = False)      #Por si es un profesor

    def __init__(self, id, code, name, surname, gender, phone, email, password, pic_url, admin, prof):
        self.id = id
        self.code = code
        self.name = name
        self.surname = surname
        self.gender = gender
        self.phone = phone
        self.email = email
        self.password = password
        self.pic_url = pic_url
        self.admin = admin
        self.prof = prof

engine = create_engine('postgresql://localhost/mydb')
NEW_DB_NAME = 'db.sqlite'

with engine.connect() as conn:
    conn.execute('commit')
    conn.execute(f"CREATE DATABASE {NEW_DB_NAME}")

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', "code", "name", "surname", "gender", "phone", "email", "password", "pic_url", "admin", "prof")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/User', methods=['POST'])
def add_user():
    codigo = request.json['code']
    name = request.json['name']
    surname = request.json['surname']
    gender = request.json['gender']
    phone = request.json['phone']
    email = request.json['email']
    password = request.json['password']
    pic_url = request.json['pic_url']
    admin = request.json['admin']
    prof = request.json['prof']

    new_user = Usuario(codigo, name, surname, gender, phone, email, password, pic_url, admin, prof)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/product', methods=['GET'])
def get_products():
    all_users = Usuario.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    user = Usuario.query.get(id)

    codigo = request.json['code']
    name = request.json['name']
    surname = request.json['surname']
    gender = request.json['gender']
    phone = request.json['phone']
    email = request.json['email']
    password = request.json['password']
    pic_url = request.json['pic_url']
    admin = request.json['admin']
    prof = request.json['prof']

    user.name = name
    user.surname = surname
    user.gender = gender
    user.password = password
    user.pic_url = pic_url

    db.session.commit()

    return UserSchema.jsonify(user)

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    user = Usuario.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return UserSchema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)