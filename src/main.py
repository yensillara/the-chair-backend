"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from flask_jwt_extended import JWTManager, create_access_token
from models import db, Professional
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'paloma'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/professionals', methods=['GET'])
def handle_professional():
    professionals = Professional.query.all()
    response_body = []
    for professional in professionals:
        response_body.append(professional.serialize())
    return jsonify(response_body), 200

@app.route('/professionals', methods=['POST'])
def add_new_professional():
    body = request.get_json()
    print (body)
    new_professional = Professional(
        full_name = body ["full_name"],
        email = body ["email"],
        profession = body ["profession"],
        phone = body ["phone"],
        location = body ["location"],
    )
    db.session.add(new_professional)
    try:
        db.session.commit()
        print (new_professional.serialize())
        return jsonify (new_professional.serialize()), 201
    except Exception as error:
        print (error.args)
        return jsonify ("NOT CREATE"), 500

@app.route('/professionals/<int:id>', methods=['GET','PATCH'])
def update_professional(id):
    if request.method == 'GET':
        professional = Professional.query.get(id)
        return jsonify (professional.serialize()), 200
    if request.method == 'PATCH':
        professional = Professional.query.get(id)
        body = request.get_json()
        if "full_name" in body:
            professional.full_name = body ['full_name']
        if "email" in body:
            professional.email = body ['email']
        if "phone" in body:
            professional.phone = body ['phone']
        if "location" in body:
            professional.location = body ['location']
        db.session.commit()
        return jsonify (professional.serialize()),200

@app.route('/professionals/<int:id>', methods=['DELETE'])
def remove_delete(id):
    professional = Professional.query.get(id)
    if professional is None:
        raise APIException('Professional not found', status_code=404)
    db.session.delete(professional)
    db.session.commit()
    return jsonify([]), 204




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
