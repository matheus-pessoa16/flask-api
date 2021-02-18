from ma import ma
from models.User import UserModel
from models.Project import ProjectModel
from schemas.ProjectSupport import ProjectSupportSchema

class ProjectSchema(ma.SQLAlchemyAutoSchema):
  projectSupport = ma.Nested(ProjectSupportSchema, many = True)
  class Meta:
    model = ProjectModel
    load_instance = True
    load_only = ("user",)
    include_fk = True