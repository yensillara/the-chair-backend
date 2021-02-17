from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode


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
  
    # def __repr__(self):
    #     return '<Professional %r>' % self.username

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

    def __init__(self,**body):
        #con esta recibimos lo que nos envía la función constructora
        self.full_name = body ['full_name']
        self.email = body ['email']
        self.professional_id = professional_id
        self.phone = body ['phone']
        self.location = body ['location']

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

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    # tipology = db.Column(db.Integer, db.ForeingKey('tipology.id'), nullable=False)
    # remodeling_type_id = db.Column(db.Integer, db.Foreignkey('remodeling.id'), nullable=False)
    # workspace_type_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nuallable=False)
    project_name = db.Column(db.String(120), nullable=False)
    final_notes = db.Column(db.String(300), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "client_id": self.client_id,
            # "tipology": self.tipology,
            # "remodeling_type_id": self.remodeling_type.id,
            # "workspace_type_id": self.workspace_type_id,
            "project_name": self.project_name,
            "final_notes": self.final_notes
        }

