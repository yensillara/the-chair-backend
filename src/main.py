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
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_current_user, get_jwt_identity
from models import db, Professional, Client, Project
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
#aquí cambiamos a super-secret
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app) #se agrega para evitar este error 'You must initialize a JWTManager with this flask application before using this method
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

#to get all professionals
@app.route('/professionals', methods=['GET'])
def handle_professional():
    professionals = Professional.query.all()
    response_body = []
    for professional in professionals:
        response_body.append(professional.serialize())
    return jsonify(response_body), 200

#to create a professional
@app.route('/professionals', methods=['POST'])
def add_new_professional():
    body = request.get_json()
    print (body)
    new_professional = Professional(
        full_name = body ["full_name"],
        password = body ["password"],
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
        return jsonify ("NOT CREATE PROFESSIONAL"), 500

#to update and get a specific professional 
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

#to delete a professional
@app.route('/professionals/<int:id>', methods=['DELETE'])
def remove_delete(id):
    professional = Professional.query.get(id)
    if professional is None:
        raise APIException('Professional not found', status_code=404)
    db.session.delete(professional)
    db.session.commit()
    return jsonify([]), 204

#----------Endpoinst clients 

#to get all clients
@app.route('/clients', methods=['GET'])
def handle_client():
    clients = Client.query.all()
    response_body=[]
    for client in clients: 
        response_body.append (client.serialize())
    return jsonify(response_body), 200

#to create a new client
@app.route('/clients', methods=['POST'])
@jwt_required
def add_new_client():
    body = request.get_json()
    print (body)
    current_email = get_jwt_identity()
    professional = Professional.query.filter_by(email=current_email).one_or_none()
    if professional is None:
        return jsonify ({"msg":"Not found"}), 404
    new_client = Client (
        full_name = body ['full_name'],
        professional_id = professional.id,
        email = body ['email'],
        phone = body ['phone'],
        location = body ['location'],
    )
    db.session.add(new_client)
    try:
        db.session.commit()
        print (new_client.serialize())
        return jsonify (new_client.serialize()), 201
    except Exception as error:
        print (error.args)
        return jsonify ("NOT CREATE CLIENT"), 500

#to delete a specific client
@app.route('/client/<int:id>', methods=['DELETE'])
def remove_client(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    return jsonify ([]), 204

@app.route('/client/<int:id>', methods=['GET', 'PATCH'])
def update_client(id):
    if request.method == ['GET']:
        client = Client.query.get(id)
        return jsonify (client.serialize()),200
    if request.method == ['PATCH']:
        client = Client.query.get(id)
        body = request.body_json()
        if 'email' in body:
            client_email = body ['email'],
        if 'phone' in body:
            client_phone = body ['phone'],
        if 'location' in body:
            client_location = body ['location'],
        db.session.commit()
        return jsonify (client.serialize()),200

#----------Endpoints projects

#to get all projects
@app.route('/projects', methods=['GET'])
def handle_project():
    projects = Project.query.all()
    response_body=[]
    for project in projects: 
        response_body.append (project.serialize())
    return jsonify(response_body), 200

#to create a new project
@app.route('/projects', methods=['POST'])
def create_new_project():
    body = request.get_json()
    print (body)
    new_project = Project (
        project_name = body ['project_name'],
        client_id = body ['client_id'],
        notes = body ['notes'],
        tipology = body ['tipology']
    )
    db.session.add(new_project)
    try:
        db.session.commit()
        print (new_project.serialize())
        return jsonify (new_project.serialize()), 201
    except Exception as error:
        print (error.args)
        return jsonify ("NOT CREATE PROJECT"), 500
    #return jsonify (add_notes.serialize()), 201
    #new_workspace = ProjectWorkSpace(
        #workspace_type_id = body ["workspace_type_id"], 
        #project_id = new_project.id  
    #)
    #db.session.add(new_workspace)
    #db.session.commit()
    #print (new_workspace.serialize())
    #return jsonify (new_workspace.serialize()), 201
    

@app.route('/projects/<int:id>', methods=['GET', 'PATCH'])
def update_project(id):
    if request.method == ['GET']:
        project = Project.query.get(id)
        return jsonify (project.serialize()), 200
    if request.method == ['PATCH']:
        project = Project.query.get(id)
        body = request.body_json()
        if 'project_name' in body:
            project_name = body ['project_name'],
        if 'notes' in body:
            project_notes = body ['notes'],
        db.session.commit()
        return jsonify (project.serialize()), 200

#to delete a specific project
@app.route('/projects/<int:id>', methods=['DELETE'])
def remove_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify ([]), 204

#----------Login
@app.route("/login", methods=["POST"])
def handle_login():
    """ 
        check password for user with email = body['email']
        and return token if match.
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    professional = Professional.query.filter_by(email=email).one_or_none()
    if not professional:
        return jsonify({"msg": "User does not exist"}), 404
    if professional.check_password(password):
        response = {'jwt': create_access_token (identity=professional.email)}
        return jsonify(response), 200
    else:
        return jsonify({"msg": "Bad credentials"}), 401
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401, 403
    # Identity can be any data that is json serializable

@app.route('/seguro')
@jwt_required
def handle_seguro():
    email = get_jwt_identity()
    #esto devuelve la identidad del token
    return jsonify ({"msg":f"Hello,{email}"})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



