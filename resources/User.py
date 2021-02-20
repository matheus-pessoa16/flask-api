
from flask import request
from flask_restplus import Resource, fields, Namespace

from models.User import UserModel
from schemas.User import UserSchema

from flask_jwt_extended import jwt_required

USER_NOT_FOUND = "User not found."
EMAIL_ALREADY_EXISTS = "Email '{}' already exists."
CPF_ALREADY_EXISTS = "CPF '{}' already exists."
LOGIN_ALREADY_EXISTS = "Login '{}' already exists."


user_ns = Namespace('user', description='user related operations')
users_ns = Namespace('users', description='users related operations')

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

#Model required by flask_restplus for expect
user = user_ns.model('User', {
    'name': fields.String('Name of the user'),
    'login': fields.String('Username to access'),
    'email': fields.String('Email of the user'),
    'cpf': fields.String('Document of the user'),
    'birthday': fields.Date,
    'password': fields.String('User password'),
})


class User(Resource):

    @jwt_required()
    def get(self, id):
        user_data = UserModel.find_by_id(id)
        if user_data:
            return user_schema.dump(user_data)
        return {'message':USER_NOT_FOUND}, 404

    @jwt_required()
    def delete(self,id):
        item_data = UserModel.find_by_id(id)
        if item_data:
            item_data.delete_from_db()
            return {'message': "Item Deleted successfully"}, 200
        return {'message':USER_NOT_FOUND}, 404

    @jwt_required()
    @user_ns.expect(user)
    def put(self, id):
        user_data = UserModel.find_by_id(id)
        user_json = request.get_json();

        if user_data:
            user_data.name = user_json['name']
            user_data.login = user_json['login']
            user_data.email = user_json['email']
            user_data.cpf = user_json['cpf']
            user_data.birthday = user_json['birthday']
        else:
            user_data = user_schema.load(user_json)

        user_data.save_to_db()
        return user_schema.dump(user_data), 200


class UserList(Resource):
    @users_ns.doc('Get all users')
    @jwt_required()
    def get(self):
        return user_list_schema.dump(UserModel.find_all()), 200

    @users_ns.expect(user)
    @users_ns.doc('Create an User')
    def post(self):
        
        user_json = request.get_json()
        
        email = user_json['email']
        cpf = user_json['cpf']
        login = user_json['login']

        if UserModel.find_by_email(email):
            return {'message': EMAIL_ALREADY_EXISTS.format(email)}, 400
        
        if UserModel.find_by_cpf(cpf):
            return {'message': CPF_ALREADY_EXISTS.format(cpf)}, 400

        if UserModel.find_by_login(login):
            return {'message': LOGIN_ALREADY_EXISTS.format(login)}, 400
        
        user_data = user_schema.load(user_json)
        user_data.hash_password()
        user_data.save_to_db()

        return user_schema.dump(user_data), 201

