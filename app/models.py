from flask_sqlalchemy import SQLAlchemy
from config.local import config
import uuid
from datetime import datetime

db = SQLAlchemy()

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = config['DATABASE_URI'] if database_path is None else database_path
    db.app = app
    db.init_app(app)
    db.create_all()

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    department_id = db.Column(db.String(36), db.ForeignKey('departments.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))
    files = db.relationship('File', backref='employee', lazy=True)


    def __init__(self, firstname, lastname, age, department_id):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.is_active = True
        self.department_id = department_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Employee %r %r>' % (self.firstname, self.lastname)
    
    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'image': self.image,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }
    
class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(120), nullable=False)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String(120), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))
    employees = db.relationship('Employee', backref='department', lazy=True)


    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Department %r %r>' % (self.name, self.short_name)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }