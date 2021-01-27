
from flask import request, Response
from flask_restplus import Resource, fields, Namespace

from models.User import UserModel
from schemas.User import UserSchema

from flask_jwt_extended import create_access_token
import datetime

auth_ns = Namespace('auth', description='auth related operations')

userJWT = auth_ns.model('UserJWT', {
  'login': fields.String('Username to access'),
  'password': fields.String('User password'),
})


class LoginApi(Resource):
    @auth_ns.doc('Login with user')
    @auth_ns.expect(userJWT)
    def post(self):
      body = request.get_json()
      user = UserModel.find_by_login(login=body.get('login'))
      user_schema = UserSchema()
      authorized = user.check_password(body.get('password'))
      if not authorized:
        return {'error': 'Login or password invalid'}, 401
    
      expires = datetime.timedelta(days=7)
      access_token = create_access_token(identity=str(user.id), expires_delta=expires)
      return {'token': access_token, 'user': user_schema.dump(user)}, 200