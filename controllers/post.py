import math

from spectree import Response
from flask import Blueprint, request, json
from flask_jwt_extended import jwt_required, current_user

from models.post import Post, PostCreate
from factory import api, db
from utils.response import DefaultResponse

post_controller = Blueprint('post_controller', __name__, url_prefix='/posts')


@post_controller.post('')
@api.validate(json=PostCreate, resp=Response(
    HTTP_201=DefaultResponse
), tags=['posts'])
@jwt_required()
def create_post():
    '''
    Create an post
    '''
    try:
        payload = request.get_json()

        text = payload['text'].strip()

        post = Post(
            text=text,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        return {'msg': 'Post criado com sucesso.'}, 201

    except Exception as err:
        db.session.rollback()
        return {
            'msg': 'Ocorreu um erro ao tentar criar o post.',
            'type_error': str(type(err)),
            'msg_error': str(err)
        }, 500
