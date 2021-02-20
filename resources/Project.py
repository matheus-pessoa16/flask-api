from flask import request
from flask_restplus import Resource, fields, Namespace

from models.Project import ProjectModel
from schemas.Project import ProjectSchema
from models.User import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity

PROJECT_NOT_FOUND = "Project not found."


project_ns = Namespace('project', description='Project related operations')
projects_ns = Namespace('projects', description='Projects related operations')

project_schema = ProjectSchema()
project_list_schema = ProjectSchema(many=True)

#Model required by flask_restplus for expect
project = projects_ns.model('Project', {
    'title': fields.String('Title of the Project'),
    'description': fields.String('Description of the Project'),
    'supports': fields.Integer,
    'user_id': fields.Integer,
})


class Project(Resource):

    @jwt_required()
    def get(self, id):
        project_data = ProjectModel.find_by_id(id)
        if project_data:
            return project_schema.dump(project_data)
        return {'message': PROJECT_NOT_FOUND}, 404

    @jwt_required
    def delete(self,id):
        user_id = get_jwt_identity()

        user = UserModel.find_by_id(user_id)
        
        project_data = None

        if user.admin:
            project_data = ProjectModel.find_by_id(id)
        else:
            project_data = ProjectModel.find_by_user_id_and_id(user_id, id)

        if project_data:
            project_data.delete_from_db()
            return {'message': "Project Deleted successfully"}, 200
        return {'message': PROJECT_NOT_FOUND}, 404

    @project_ns.expect(project)
    @jwt_required
    def put(self, id):
        project_data = ProjectModel.find_by_id(id)
        project_json = request.get_json();

        if project_data:
            project_data.title = project_json['title']
            project_data.description = project_json['description']
            project_data.supports = project_json['supports']
        else:
            project_data = project_schema.load(project_json)

        project_data.save_to_db()
        return project_schema.dump(project_data), 200


class ProjectList(Resource):
    @projects_ns.doc('Get all Projects')
    def get(self):
        return project_list_schema.dump(ProjectModel.find_all()), 200

    @projects_ns.expect(project)
    @projects_ns.doc('Create a Project')
    @jwt_required()
    def post(self):
        project_json = request.get_json()
        project_data = project_schema.load(project_json)
        project_data.save_to_db()

        return project_schema.dump(project_data), 201