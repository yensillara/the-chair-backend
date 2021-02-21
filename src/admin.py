import os
from flask_admin import Admin
from models import db, Professional, Client, Workspace, ProjectWorkSpace, DesignStyle, FurnitureStyle, ProjectFurnitureStyle, AccesoriesStyle, ProjectAccesoriesStyle, ColorPalette, Texture, ProjectTexture, Finishes, ProjectFinishes 
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Professional, db.session))
    admin.add_view(ModelView(Client, db.session))
    admin.add_view(ModelView(Workspace, db.session))
    admin.add_view(ModelView(ProjectWorkSpace, db.session))
    admin.add_view(ModelView(DesignStyle, db.session))
    admin.add_view(ModelView(FurnitureStyle, db.session))
    admin.add_view(ModelView(ProjectFurnitureStyle, db.session))
    admin.add_view(ModelView(AccesoriesStyle, db.session)) 
    admin.add_view(ModelView(ProjectAccesoriesStyle, db.session))
    admin.add_view(ModelView(ColorPalette, db.session))
    admin.add_view(ModelView(Texture, db.session))
    admin.add_view(ModelView(ProjectTexture, db.session))
    admin.add_view(ModelView(Finishes, db.session)) 
    admin.add_view(ModelView(ProjectFinishes, db.session))     

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))