
from db import db
from typing import List
from sqlalchemy.orm import backref


class ProjectModel(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000))
    supports = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    user = db.relationship("UserModel", backref=backref("user", cascade="all, delete-orphan"))

    project_supports = db.relationship("ProjectSupportModel", lazy="dynamic",primaryjoin="ProjectModel.id == ProjectSupportModel.project_id", cascade="all, delete-orphan")
    
    def __init__(self, title, description, supports, user_id):
        self.title = title
        self.description = description
        self.supports = supports
        self.user_id = user_id

    def json(self):
        return {
        'title': self.title,
        'description': self.description,
        'supports': self.supports }

    @classmethod
    def find_by_title(cls, title) -> "ProjectModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_user_id_and_id(cls,user_id, _id) -> "ProjectModel":
        return cls.query.filter_by(id=_id, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, _id) -> "ProjectModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ProjectModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()