from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    #hashed.password = db.Column(db.String(8), nullable=False)
    #salt = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String (20), nullable=False)

    def __repr__(self):
        return '<Professional %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "profession": self.profession,
            "phone": self.phone,
            "location": self.location,
        }