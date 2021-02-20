from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import backref

db = SQLAlchemy()

class Professional(db.Model):
    #esta es la función constructura de la clase
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(25), unique=True, nullable=False)
    location = db.Column(db.String (50), nullable=False)
    clients = db.relationship("Client", backref="professional")

    def __init__(self,**body):
        #con esta recibimos lo que nos envía la función constructora
        self.full_name = body ['full_name']
        self.salt = b64encode(os.urandom(4)).decode('utf-8')
        self.hashed_password = self.set_password(body['password'])
        self.email = body ['email']
        self.profession = body ['profession']
        self.phone = body ['phone']
        self.location = body ['location']
        
    def set_password(self, password):
        return generate_password_hash(
            f"{password}{self.salt}"
    ) 

    def check_password(self, password):
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.salt}"
        )

    @classmethod
    def create (cls,**kwargs):
        new_professional=cls(kwargs)
        db.session.add(new_professional)
        db.session.commit()
        return add_new_professional    

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "profession": self.profession,
            "phone": self.phone,
            "location": self.location,
        }

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey ('professional.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    projects = db.relationship("Project", backref="client")

    @classmethod
    def create (cls, **body):
        new_client=cls(body)
        return add_new_cliente  

    def serialize(self):
        return{
            "id": self.id,
            "professional_id":self.professional_id,
            "full_name":self.full_name,
            "email":self.email,
            "phone":self.phone,
            "location":self.location,
        }

class Tipologies(enum.Enum):
    UNIFAMILIAR = "Unifamiliar"
    MULTIFAMILIAR = "Multifamiliar"
    OFICINA = "Oficina"
    LOCAL_COMERCIAL = "Local Comercial"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    #tipology_id = db.Column(db.Integer, db.ForeignKey('tipology.id'), nullable=False)
    tipology = db.Column(db.Enum(Tipologies), nullable=False, default="Unifamiliar")
    #workspace_type_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=True)
    project_name = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.String(300), nullable=False)

    def __init__ (self, client_id, tipology, project_name, notes):
        self.client_id = client_id
        self.project_name = project_name
        self.notes = notes
        self.tipology = Tipologies(tipology)

    def serialize(self):
        return{
            "id": self.id,
            "client_id": self.client_id,
            "tipology": self.tipology.value,
            #"workspace_type_id": self.workspace_type_id,
            "project_name": self.project_name,
            "notes": self.notes
        }



# class Tipology(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.Enum(Tipologies), nullable=False, default=1)
#     projects = db.relationship("Project", backref="tipology")

#     def serialize(self):
#         return{
#             "id":self.id,
#             "project_id":self.project_id,
#             "category":self.category, 
#         }


#Class WorkSpace:

class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipology = db.Column(db.Enum(Tipologies), nullable=False, default="Unifamiliar")
    workspace_name = db.Column(db.String(120), nullable=False)
    projectworkspaces = db.relationship("ProjectWorkSpace", backref = "workspace")

def serialize(self):
        return{
            "id":self.id,
            "tipology": self.tipology.value,
            "workspace_name":self.workspace_name, 
        }  

