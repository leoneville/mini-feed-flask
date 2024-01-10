from datetime import datetime

from main import app
from factory import db
from models import User, Post


with app.app_context():
    user = User.query.filter_by(username='leoneville.dev').first()

    # post = Post(text="Hello World!", author_id=user.id)

    # db.session.add(post)

    # post_2 = Post(text="Neps is awesome!", author=user)

    # db.session.add(post_2)

    # db.session.commit()

    post = Post.query.first()

    # Imprime nome campo "username" do objeto "author"
    print(f'Author: {post.author.username}')
    # Imprime texto do objeto Post
    print(f'Text: {post.text}')
    # Imprime data de criação
    print(f'Created at: {post.created}')

    print(user.posts)

    print(user.posts.all())
