import math

from spectree import Response
from flask import Blueprint, request, jsonify, json
from flask_jwt_extended import jwt_required, current_user

from factory import api, db
from models.post import (Post, PostCreate, PostResponse,
                         PostResponseList, SearchModel)

from utils.response import DefaultResponse, DefaultErrorResponse

post_controller = Blueprint('post_controller', __name__, url_prefix='/posts')

POST_NAO_ENCONTRADO = 'Post não encontrado.'


@post_controller.post('')
@api.validate(json=PostCreate, resp=Response(
    HTTP_201=DefaultResponse,
    HTTP_500=DefaultErrorResponse
), tags=['posts'])
@jwt_required()
def create_post():
    '''
    Create post
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


@post_controller.put('/<int:post_id>')
@api.validate(json=PostCreate, resp=Response(
    HTTP_200=DefaultResponse,
    HTTP_403=DefaultResponse,
    HTTP_404=DefaultResponse,
    HTTP_500=DefaultErrorResponse
), tags=['posts'])
@jwt_required()
def update_post(post_id: int):
    '''
    Update post
    '''
    try:
        if (post := db.session.get(Post, post_id)) is None:
            return {'msg': POST_NAO_ENCONTRADO}, 404

        if post.author_id != current_user.id:
            return {'msg': 'Você não tem autorização para atualizar este post.'}, 403

        payload = request.get_json()
        text = payload['text']

        post.text = text

        db.session.commit()

        return {'msg': 'Post atualizado com sucesso.'}, 200

    except Exception as err:
        db.session.rollback()
        return {
            'msg': 'Ocorreu um erro ao tentar atualizar o post.',
            'type_error': str(type(err)),
            'msg_error': str(err)
        }, 500


@post_controller.delete('/<int:post_id>')
@api.validate(resp=Response(
    HTTP_200=DefaultResponse,
    HTTP_403=DefaultResponse,
    HTTP_404=DefaultResponse,
    HTTP_500=DefaultErrorResponse
), tags=['posts'])
@jwt_required()
def delete_post(post_id: int):
    '''
    Delete post
    '''
    try:
        if (post := db.session.get(Post, post_id)) is None:
            return {'msg': POST_NAO_ENCONTRADO}, 404

        if post.author_id != current_user.id:
            return {'msg': 'Você não tem permissão para deletar este post.'}, 403

        db.session.delete(post)

        db.session.commit()

        return {'msg': 'Post deletado com sucesso.'}, 200

    except Exception as err:
        db.session.rollback()
        return {
            'msg': 'Ocorreu um erro ao tentar deletar o post.',
            'type_error': str(type(err)),
            'msg_error': str(err)
        }, 500


@post_controller.get('/<int:post_id>')
@api.validate(resp=Response(
    HTTP_200=PostResponse,
    HTTP_404=DefaultResponse,
    HTTP_500=DefaultErrorResponse
), tags=['posts'])
@jwt_required()
def get_one(post_id: int):
    '''
    Get post by id
    '''
    try:
        if (post := db.session.get(Post, post_id)) is None:
            return {'msg': POST_NAO_ENCONTRADO}, 404

        response = PostResponse.from_orm(post).json()

        return jsonify(json.loads(response)), 200

    except Exception as err:
        return {
            'msg': 'Ocorreu um erro ao buscar as informações do post.',
            'type_error': str(type(err)),
            'msg_error': str(err)
        }, 500


@post_controller.get('')
@api.validate(query=SearchModel, resp=Response(
    HTTP_200=PostResponseList,
    HTTP_500=DefaultErrorResponse
), tags=['posts'])
@jwt_required()
def get_all():
    '''
    Get all posts
    '''
    try:
        search = request.args.get('search', "", type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        reverse = True if request.args.get(
            'reversed', 'false') == 'true' else False

        posts_query = Post.query.filter(Post.text.ilike(f"%{search}%"))

        if reverse:
            posts_query = posts_query.order_by(Post.created.desc())

        posts_paginate = posts_query.paginate(page=page, per_page=per_page)

        posts, total = posts_paginate.items, posts_paginate.total

        response = PostResponseList(
            page=page,
            pages=math.ceil(total / per_page),
            total=total,
            posts=[PostResponse.from_orm(post).dict() for post in posts]
        ).json()

        return jsonify(json.loads(response)), 200

    except Exception as err:
        return {
            'msg': 'Ocorreu um erro ao buscar as informações do post.',
            'type_error': str(type(err)),
            'msg_error': str(err)
        }, 500
