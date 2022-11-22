from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

app = Flask(__name__)

#TODO: MYSQL CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abhijit@localhost:3306/test'
db = SQLAlchemy(app)

#TODO: THE DATABASE TABLE MODEL
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(20))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,firstName,lastName,email,password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '' % self.id

db.create_all()

#TODO: THE ORM for flask -> Marshmello-sqlAlchemy
class UserSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = User
        load_instance = True
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

#TODO: THE CRUD MAPPINGS

@app.route('/')
def hello():
    return "Hello"

#GET ALL USERS
@app.route('/users', methods = ['GET'])
def getUsers():
    getUsers = User.query.all()
    userSchema = UserSchema(many=True)
    users = userSchema.dump(getUsers)
    return make_response(jsonify({"user": users}))

#GET User by id
@app.route('/user/<id>', methods = ['GET'])
def getUserById(id):
    getUser = User.query.get(id)
    userSchema = UserSchema()
    user = userSchema.dump(getUser)
    return make_response(jsonify({"user": user}))

#POST User
@app.route('/createUser', methods = ['POST'])
def createUser():
    data = request.get_json() 
    userSchema = UserSchema()
    user = userSchema.load(data)
    result = userSchema.dump(user)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({"user": result}))

#PUT/EDIT user
@app.route('/updateUser/<id>', methods = ['PUT'])
def updateUser(id):
    data = request.get_json()
    getUser = User.query.get(id)

    if data.get('firstName'):
        getUser.firstName = data['firstName']
    if data.get('lastName'):
        getUser.lastName = data['lastName']
    if data.get('email'):
        getUser.email = data['email']
    if data.get('password'):
        getUser.password= data['password']    

    db.session.add(getUser)
    db.session.commit()

    userSchema = UserSchema(only=['id', 'firstName', 'lastName','email','password'])
    user = userSchema.dump(getUser)
    return make_response(jsonify({"user": user}))

#Delete User
@app.route('/deleteUser/<id>', methods = ['DELETE'])
def deleteUser(id):
    getUser = User.query.get(id)
    db.session.delete(getUser)
    db.session.commit()
    return make_response("Success",204)

if __name__ == "__main__":
    app.run(debug=True)
