from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db
from flask_bcrypt import Bcrypt

from resources.User import User, UserList, user_ns, users_ns
from resources.Project import Project, ProjectList, projects_ns, project_ns
from resources.Auth import LoginApi, auth_ns
from resources.ProjectSupport import ProjectSupport, ProjectSupportList, UserProjectSupportList, CreateProjectSupport, project_support_ns, project_supports_ns
from marshmallow import ValidationError
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from models.User import UserModel
from schemas.User import UserSchema

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Project Flask-API Documentation')
app.register_blueprint(bluePrint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)


app.config.from_envvar('ENV_FILE_LOCATION')

api.add_namespace(project_ns)
api.add_namespace(projects_ns)
api.add_namespace(user_ns)
api.add_namespace(users_ns)
api.add_namespace(auth_ns)
api.add_namespace(project_support_ns)
api.add_namespace(project_supports_ns)

@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

project_ns.add_resource(Project, '/<int:id>')
projects_ns.add_resource(ProjectList, "")
user_ns.add_resource(User, '/<int:id>')
users_ns.add_resource(UserList, "")
auth_ns.add_resource(LoginApi, '/login')
project_support_ns.add_resource(ProjectSupport, '/<int:id>')
project_support_ns.add_resource(CreateProjectSupport, '')
project_supports_ns.add_resource(UserProjectSupportList, "/<int:user_id>")
project_supports_ns.add_resource(ProjectSupportList, "/project/<int:project_id>")


def createAdmin():
    with app.app_context():
        exists = UserModel.find_by_name('admin')
        if not exists:
            user = UserModel(
                name='admin',
                login='admin',
                email='admin@mail.com',
                cpf='78945612399',
                birthday='08/02/1995',
                password='admin@123',
                admin=True,
            )
            user.hash_password()
            user.save_to_db()

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    createAdmin()
    app.run(port=5000, debug=True)