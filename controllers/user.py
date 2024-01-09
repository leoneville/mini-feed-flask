from datetime import date

from spectree import Response
from flask import Blueprint, request, json
from flask_jwt_extended import jwt_required, current_user

from factory import db, api
from utils.response import DefaultResponse
from models.user import User, UserCreate, UserResponse, UserResponseList, UserEdit

user_controller = Blueprint('user_controller', __name__, url_prefix='/users')

USUARIO_NAO_ENCONTRADO = 'Usuário não encontrado.'


@user_controller.get('/<int:user_id>')
@api.validate(resp=Response(
    HTTP_200=UserResponse,
    HTTP_404=DefaultResponse
), tags=['users'], path_parameter_descriptions={"user_id": "ID do usuário"})
@jwt_required()
def get_user(user_id: int):
    '''
    Get a specified user
    '''
    user = db.session.get(User, user_id)
    if user is None:
        return {'msg': USUARIO_NAO_ENCONTRADO}, 404

    response = UserResponse.from_orm(user).json()

    return json.loads(response), 200


@user_controller.get('')
@api.validate(resp=Response(
    HTTP_200=UserResponseList
), tags=['users'])
@jwt_required()
def get_users():
    '''
    Get all users
    '''
    users = User.query.all()

    response = UserResponseList(
        __root__=[UserResponse.from_orm(user).dict() for user in users]
    ).json()

    return json.loads(response), 200


@user_controller.post('')
@api.validate(json=UserCreate, resp=Response(
    HTTP_201=DefaultResponse,
    HTTP_409=DefaultResponse
), tags=['users'])
@jwt_required()
def post_user():
    '''
    Create an user
    '''
    try:
        payload = request.get_json()

        username = payload['username']
        email = payload['email']
        birthdate = payload.get('birthdate')
        password = payload['password']

        if User.query.filter_by(username=username).first():
            return {'msg': 'Username não disponível.'}, 409

        if User.query.filter_by(email=email).first():
            return {'msg': 'Email já cadastrado.'}, 409

        if birthdate:
            birthdate = date.fromisoformat(birthdate)

        user = User(
            username=username,
            email=email,
            birthdate=birthdate,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return {'msg': 'Usuário criado com sucesso.'}, 201

    except Exception as err:
        db.session.rollback()
        return {
            "msg": "Ocorreu um erro ao criar o usuário.",
            "type_error": str(type(err)),
            "msg_error": str(err)
        }, 500


@user_controller.put('')
@api.validate(json=UserEdit, resp=Response(
    HTTP_200=DefaultResponse,
    HTTP_404=DefaultResponse,
    HTTP_409=DefaultResponse
), tags=['users'])
@jwt_required()
def put_user():
    '''
    Update a user
    '''
    payload = request.get_json()

    username = payload['username']
    email = payload['email']
    birthdate = payload.get('birthdate')

    user = current_user

    if User.query.filter_by(username=username).first() and username != user.username:
        return {'msg': 'Username não disponível.'}, 409

    if User.query.filter_by(email=email).first() and email != user.email:
        return {'msg': 'Email já cadastrado.'}, 409

    if birthdate:
        birthdate = date.fromisoformat(birthdate)

    user.username = username
    user.email = email
    user.birthdate = birthdate

    db.session.commit()

    return {'msg': 'Usuário atualizado com sucesso.'}, 200


@user_controller.delete('/<int:user_id>')
@api.validate(resp=Response(
    HTTP_200=DefaultResponse,
    HTTP_404=DefaultResponse
), tags=['users'], path_parameter_descriptions={"user_id": "ID do usuário"})
@jwt_required()
def delete_user(user_id: int):
    '''
    Delete a user
    '''
    user = db.session.get(User, user_id)
    if user is None:
        return {'msg': USUARIO_NAO_ENCONTRADO}, 404

    db.session.delete(user)
    db.session.commit()

    return {'msg': 'Usuário deletado com sucesso.'}, 200
