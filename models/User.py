
from models.Project import ProjectModel
from flask_restplus.fields import Boolean
from db import db
from typing import List
from flask_bcrypt import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    cpf = db.Column(db.String(13), nullable=False, unique=True)
    birthday = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    projects = db.relationship("ProjectModel",lazy="dynamic",primaryjoin="UserModel.id == ProjectModel.user_id", cascade="all, delete-orphan")


    def __init__(self, name, login, email, cpf, birthday, password, admin=False):
        self.name = name
        self.login = login
        self.email = email
        self.cpf = cpf
        self.birthday = birthday
        self.password = password
        self.admin = admin

    def json(self):
        return {'name': self.name, 
        'name': self.name,
        'login': self.login,
        'email': self.email,
        'cpf': self.cpf,
        'birthday': self.birthday,
        'admin': self.admin}

    @classmethod
    def find_by_name(cls, name) -> "UserModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_email(cls, email) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_cpf(cls, cpf) -> "UserModel":
        return cls.query.filter_by(cpf=cpf).first()

    @classmethod
    def find_by_login(cls, login) -> "UserModel":
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password) -> Boolean:
        return check_password_hash(self.password, password)
