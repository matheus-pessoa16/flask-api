from flask import request
from flask_restplus import Resource, fields, Namespace

from models.ProjectSupport import ProjectSupportModel
from schemas.ProjectSupport import ProjectSupportSchema

from models.Project import ProjectModel

from flask_jwt_extended import jwt_required

PROJECT_SUPPORT_NOT_FOUD = "Project support not found."
PROJECT_ALREADY_SUPPORTED = "Project already supported"

project_support_ns = Namespace('support', description='supports related operations')
project_supports_ns = Namespace('supports', description='supports related operations')


project_support_schema = ProjectSupportSchema()
project_support_list_schema = ProjectSupportSchema(many=True)

#Model required by flask_restplus for expect
project_support = project_support_ns.model('ProjectSupport', {
    'project_id': fields.Integer,
    'user_id': fields.Integer
})


class ProjectSupport(Resource):

  @jwt_required
  def get(self, id):
      project_support_data = ProjectSupportModel.find_by_id(id)
      if project_support_data:
          return project_support_schema.dump(project_support_data)
      return {'message': PROJECT_SUPPORT_NOT_FOUD}, 404

  @jwt_required
  def delete(self,id):
      item_data = ProjectSupportModel.find_by_id(id)
      if item_data:
          item_data.delete_from_db()
          return {'message': "Support removed successfully"}, 200
      return {'message': PROJECT_SUPPORT_NOT_FOUD}, 404

class CreateProjectSupport(Resource):
  @project_support_ns.expect(project_support)
  @project_support_ns.doc('Add support to a project')
  def post(self):
      
      support_json = request.get_json()
      
      project_id = support_json['project_id']
      user_id = support_json['user_id']

      support_data = ProjectSupportModel.find_by_user_id_project_id(user_id=user_id, project_id=project_id)

      if support_data:
          return {'message': PROJECT_ALREADY_SUPPORTED}, 400
      
      support_data = project_support_schema.load(support_json)
      
      support_data.save_to_db()

      project_data = ProjectModel.find_by_id(project_id)

      project_data.supports = ProjectSupportModel.find_all_by_project_id(project_id).count()

      project_data.save_to_db()

      return '', 201

class ProjectSupportList(Resource):
  
  @project_supports_ns.doc('Get all supports by project')
  @jwt_required
  def get(self, project_id):
      return project_support_list_schema.dump(ProjectSupportModel.find_all_by_project_id(project_id)), 200

class UserProjectSupportList(Resource):

  @project_supports_ns.doc('Get all projects supported by a user')
  @jwt_required
  def get(self, user_id):
      return project_support_list_schema.dump(ProjectSupportModel.find_all_by_user_id(user_id)), 200