from ma import ma
from models.User import UserModel
from models.Project import ProjectModel


class ProjectSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = ProjectModel
    load_instance = True
    load_only = ("user",)
    include_fk = True