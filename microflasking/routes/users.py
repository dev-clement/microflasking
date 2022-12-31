from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required
)
from flask_api import status
from passlib.hash import pbkdf2_sha256
from microflasking import db
from microflasking.models import UserModel
from microflasking.schema import UserSchema
from microflasking.blocklist import BLOCKLIST

blp = Blueprint('Users', 'users', description='Operation on users...')

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'Logged-out successfully !'}, status.HTTP_200_OK

@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            abort(http_status_code=409, message='A user with that email already exists...')
        user = UserModel(email=user_data['email'], password=pbkdf2_sha256.hash(user_data['password']))
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created...'}, status.HTTP_201_CREATED

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, status.HTTP_200_OK
        abort(http_status_code=status.HTTP_400_BAD_REQUEST, message='Invalid credentials...')

