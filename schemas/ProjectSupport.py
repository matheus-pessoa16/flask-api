from ma import ma
from models.User import UserModel
from models.Project import ProjectModel
from models.ProjectSupport import ProjectSupportModel

class ProjectSupportSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = ProjectSupportModel
    load_instance = True
    load_only = ("user","project")
    include_fk = True