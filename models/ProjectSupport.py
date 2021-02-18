from db import db
from typing import List
from sqlalchemy.orm import backref

class ProjectSupportModel(db.Model):
  __tablename__ = "project_support"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
  project_id = db.Column(db.Integer,db.ForeignKey('project.id'),nullable=False)

  def __init__(self, user_id, project_id):
    self.user_id = user_id
    self.project_id = project_id

  def json(self):
    return {
    'user': self.user,
    'project': self.project }

  @classmethod
  def find_by_id(cls, _id) -> "ProjectSupportModel":
    return cls.query.filter_by(id=_id).first()
  
  @classmethod
  def find_by_user_id_project_id(cls, user_id, project_id) -> "ProjectSupportModel":
    return cls.query.filter_by(user_id=user_id, project_id = project_id).first()

  @classmethod
  def find_all_by_user_id(cls, user_id) -> List["ProjectSupportModel"]:
    return cls.query.filter_by(user_id = user_id)

  @classmethod
  def find_all_by_project_id(cls, project_id) -> List["ProjectSupportModel"]:
    return cls.query.filter_by(project_id = project_id)

  def save_to_db(self) -> None:
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self) -> None:
    db.session.delete(self)
    db.session.commit()