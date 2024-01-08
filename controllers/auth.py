from flask import Blueprint, request
from spectree import Response

from pydantic.v1 import BaseModel, SecretStr

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from models import User
from utils.response import DefaultResponse
from factory import api


class Auth(BaseModel):
    username: str
    password: SecretStr


class LoginResponse(BaseModel):
    type: str
    access_token: str
    refresh_token: str


auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')


@auth_controller.post('/login')
@api.validate(json=Auth, resp=Response(
    HTTP_200=LoginResponse,
    HTTP_401=DefaultResponse
), security={}, tags=['authentication'])
def login():
    '''
    Authenticate an user
    '''
    payload = request.get_json()

    username = payload['username']
    password = payload['password']

    if (user := User.query.filter_by(username=username).first()) and user.verify_password(password):
        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'type': 'Bearer',
            'access_token': token,
            'refresh_token': refresh_token
        }, 200

    return {'msg': 'Usuário ou senha incorretos.'}, 401


@auth_controller.post('/logout')
@api.validate(resp=Response(
    HTTP_200=DefaultResponse
), tags=['authentication'])
@jwt_required()
def logout():
    '''
    Logout an user
    '''
    return {'msg': 'Deslogado com sucesso'}, 200
