from spectree import Response
from flask import Blueprint, request

from pydantic.v1 import BaseModel, SecretStr

from flask_jwt_extended import (
        create_access_token, create_refresh_token, jwt_required, get_jwt,
        get_jwt_identity
    )

from factory import api, jwt_redis_blocklist
from models import User
from config import ACCESS_EXPIRES
from utils.response import DefaultResponse


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
    HTTP_200=DefaultResponse,
    HTTP_401=None
), tags=['authentication'])
@jwt_required()
def logout():
    '''
    Logout an user
    '''

    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    return {'msg': 'Deslogado com sucesso'}, 200


@auth_controller.post('/refresh_token')
@api.validate(resp=Response(
    HTTP_200=None,
    HTTP_401=None
), tags=['authentication'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Generates a new authentication token
    """
    identity = get_jwt_identity()

    return {"access_token": create_access_token(identity=identity)}, 200