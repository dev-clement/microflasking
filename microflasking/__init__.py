import uuid
import os
from flask import Flask, jsonify
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .db import db
from .routes.users import blp as UserBlueprint
from .models import UserModel
from .blocklist import BLOCKLIST

def create_app(db_url = None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'th1s1s3cr3t'
    app.config['API_TITLE'] = 'Rest API with sqlalchemy and Flask'
    app.config['API_VERSION'] = '1.0.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['PROPAGATE_EXCEPTION'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///daabase.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['JWT_SECRET_KEY'] = uuid.uuid4().hex
    app.config['FLASK_DEBUG'] = 1
    app.config['FLASK_ENV'] = 'development'
    db.init_app(app=app)
    api = Api(app)
    jwt = JWTManager(app=app)
    migrate = Migrate(app=app, db=db)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        return {'id_admin': True if identity == 1 else False}
    
    @jwt.expired_token_loader
    def expired_token_loader(error):
        return jsonify({'message': 'The token has expired...', 'error': 'token_expired'}), status.HTTP_401_UNAUTHORIZED

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'message': 'Signature verification has failed...', 'error': 'invalid_token'}), status.HTTP_401_UNAUTHORIZED
    
    @jwt.unauthorized_loader
    def missing_token(error):
        return jsonify({'message': 'Request does not contains an access token...', 'error': 'authorization_required'}), status.HTTP_401_UNAUTHORIZED
    
    @jwt.revoked_token_loader
    def revoked_token_loader(jwt_header, jwt_payload):
        return jsonify({'message': 'The token has been revoked', 'error': 'token_revoked'}), status.HTTP_401_UNAUTHORIZED
    
    @jwt.needs_fresh_token_loader
    def token_need_fresh(jst_header, jwt_payload):
        return jsonify({'message': 'Token needs some refreshing...', 'error': 'fresh_token_expired'}), status.HTTP_401_UNAUTHORIZED
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_check(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    with app.app_context() as ctx:
        db.create_all()

    api.register_blueprint(UserBlueprint)
    return app
