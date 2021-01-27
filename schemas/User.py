from ma import ma
from models.User import UserModel
from models.Project import ProjectModel
from schemas.Project import ProjectSchema
from schemas.ProjectSupport import ProjectSupportSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
  projects = ma.Nested(ProjectSchema, many=True)
  projectSupport = ma.Nested(ProjectSupportSchema, many = True)
  class Meta:
    model = UserModel
    load_instance = True
    include_fk = True