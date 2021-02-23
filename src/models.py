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
    description = db.Column(db.String (1000), nullable=False)

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
        self.description = body ['description']
        
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
        return new_professional    

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "profession": self.profession,
            "phone": self.phone,
            "location": self.location,
            "descrition":self.description,
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
        return new_client

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
    RESIDENCTIAL = "Residential"
    OFFICE = "Office"
    COMERCIAL = "Comercial"

class WorkSpaces(enum.Enum):
    LIVINGROOM = "Living room"
    FAMILYROOM = "Family room"
    KITCHEN = "Kitchen"
    BATHROOM = "Bathroom"
    BEDROOM = "Bedroom"
    VESTIER = "Vestier"
    HOME_OFFICE = "Home Office"
    OFFICE = "Office"
    PLAYROOM = "Playroom"
    LAUNDRY = "Laundry"
    OUTDOOR = "Outdoor"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    tipology = db.Column(db.Enum(Tipologies), nullable=False, default="Residential")
    #project_data = db.Column(db.Integer, db.ForeignKey('ProjectData.id'), uselist=False)
    project_name = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.String(300), nullable=False)

    project_data = db.relationship ('ProjectData', backref="project", uselist=False)

    def __init__ (self, client_id, tipology, project_name, notes, workspace):
        self.client_id = client_id
        self.project_name = project_name
        self.notes = notes
        self.project_data = project_data
        self.tipology = Tipologies(tipology)

    def serialize(self):
        return{
            "id": self.id,
            "client_id": self.client_id,
            "client": self.client.serialize(),
            "tipology": self.tipology.value,
            "project_data": self.project_data.serialize(),
            "project_name": self.project_name,
            "notes": self.notes
        }

# Class ProjectData:

class ProjectData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    workspace = db.Column(db.Enum(WorkSpaces), nullable=False, default="Living room")
    design_style_id = db.Column(db.Integer, db.ForeignKey('design_style.id'), nullable=False)
    project_furniture_styles = db.relationship('ProjectFurnitureStyle', backref='project_data')
    project_accesories_styles = db.relationship('ProjectAccesoriesStyle', backref='project_data')
    color_palette_id = db.Column(db.Integer, db.ForeignKey('color_palette.id'), nullable=False)
    project_textures = db.relationship('ProjectTexture', backref='project_data')
    project_finishes = db.relationship('ProjectFinishes', backref='project_data')
    sketch_id = db.Column(db.Integer, db.ForeignKey('sketch.id'), nullable=False)


    def __init__ (self, workspace, project_id, design_style_id, color_palette_id, sketch_id): 
        self.workspace = workspace
        self.project_id = project_id
        self.design_style_id = design_style_id
        self.color_palette_id = color_palette_id
        self.sketch_id = sketch_id
        

    def serialize(self):
        return{
            "id": self.id,
            "workspace": self.workspace.value,
            "project_id": self.project_id,
            "design_style_id": self.design_style_id,
            "furniture_style": self.furniture_style,
            "accesories_style": self.accesories_style,
            "color_palette_id": self.color_palette_id,
            "texture": self.texture,
            "finishes": self.finishes,
            "sketch_id": self.sketch_id,
        }

#Class DesignStyle:
class DesignStyle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    design_style_name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(900), nullable=False)

    project_data=db.relationship ('ProjectData', backref='design_style')

    def serialize(self):
        return{
            "id": self.id,
            "design_style_name": self.designstyle_name,
            "image_url": self.image_url,
        }

# Class FurnitureStyle:
class FurnitureStyle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    furniture_style_name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(900), nullable=False)

    project_furniture_style = db.relationship ("ProjectFurnitureStyle", backref="furniture_style")
    
    def serialize(self):
        return{
            "id":self.id,
            "furniture_style_name":self.furniture_style_name,
            "image_url": self.image_url, 
        }

# Class ProjectFurnitureStyle:
class ProjectFurnitureStyle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Enum(WorkSpaces), nullable=False, default="Living room")
    furniture_style_id = db.Column(db.Integer, db.ForeignKey('furniture_style.id'), nullable=False)
    project_data_id = db.Column (db.Integer, db.ForeignKey('project_data.id'), nullable=False)
    
    def serialize(self):
        return{
            "id":self.id,
            "workspace": self.workspace.value,
            "furniture_style_id": self.furniture_style_id,
            "project_data_id": self.project_data_id,
        } 

# Class AccesoriesStyle:
class AccesoriesStyle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accesories_style_name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(900), nullable=False)

    project_accesories_style = db.relationship ("ProjectAccesoriesStyle", backref="accesories_style")

    def serialize(self):
        return{
            "id":self.id,
            "accesories_style_name": self.accesories_style_name,
            "image_url": self.image_url,
        }

# Class ProjectAccesoriesStyle:
class ProjectAccesoriesStyle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Enum(WorkSpaces), nullable=False, default="Living room")
    accesories_style_id = db.Column(db.Integer, db.ForeignKey('accesories_style.id'), nullable=False)
    project_data_id = db.Column (db.Integer, db.ForeignKey('project_data.id'), nullable=False)

    def serialize(self):
        return{
            "id":self.id,
            "workspace": self.workspace.value,
            "accesories_style_id": self.accesories_style_id,
            "project_data_id": self.project_data_id,
        }

#Class ColorPalette:
class ColorPalette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color_palette_name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(900), nullable=False)

    project_data=db.relationship ('ProjectData', backref='color_palette')

    def serialize(self):
        return{
            "id": self.id,
            "color_palette_name": self.color_palette_name,
            "image_url": self.image_url,
        }

#Class Texture:
class Texture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texture_name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(900), nullable=False)

    project_texture = db.relationship ("ProjectTexture", backref="texture")

    def serialize(self):
        return{
            "id": self.id,
            "texture_name": self.texture_name,
            "image_url": self.image_url,
        }

# Class ProjectTexture:
class ProjectTexture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Enum(WorkSpaces), nullable=False, default="Living room")
    texture_id = db.Column(db.Integer, db.ForeignKey('texture.id'), nullable=False)
    project_data_id = db.Column (db.Integer, db.ForeignKey('project_data.id'), nullable=False)

    def serialize(self):
        return{
            "id":self.id,
            "workspace": self.workspace,
            "texture_id": self.texture_id,
            "project_data_id": self.project_data_id,
        }

#Class Finishes:
class Finishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finishes_name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(900), nullable=False)

    project_finishes = db.relationship ("ProjectFinishes", backref="finishes")

    def serialize(self):
        return{
            "id": self.id,
            "finishes_name": self.finishes_name,
            "image_url": self.image_url,   
        }

# Class ProjectFinishes:
class ProjectFinishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace = db.Column(db.Enum(WorkSpaces), nullable=False, default="Living room")
    finishes_id = db.Column(db.Integer, db.ForeignKey('finishes.id'), nullable=False)
    project_data_id = db.Column (db.Integer, db.ForeignKey('project_data.id'), nullable=False)

    def serialize(self):
        return{
            "id":self.id,
            "workspace": self.workspace,
            "finishes_id": self.finished_id,
            "project_data_id": self.project_data_id,
        }

# Class Sketch:
class Sketch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sketch_name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(900), nullable=False)

    project_data=db.relationship ('ProjectData', backref='sketch')

    def serialize(self):
        return{
            "id": self.id,
            "sketch_name": self.sketch_name,
            "image": self.image,
        }