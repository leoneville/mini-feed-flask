import os
import csv
from datetime import datetime
from textwrap import dedent

from factory import db
from main import app
from models import Post, User, Role

URL = "http://127.0.0.1:5000"
basedir = os.path.abspath(os.path.dirname(__file__))


class Error(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return dedent(
            f"""
            {self.message}.
            Sorry, something is wrong!
            Please let me know by emailing the error above to leoneville_@hotmail.com or sending on discord.
            """
        )


def create_roles(roles):
    try:
        for role in roles:
            new_role = Role(
                name=role["name"],
                can_access_sensitive_information=True if role[
                    "can_access_sensitive_information"] == "True" else False,
                can_manage_users=True if role["can_manage_users"] == "True" else False,
                can_manage_posts=True if role["can_manage_posts"] == "True" else False
            )

            db.session.add(new_role)

        db.session.commit()
    except Exception as e:
        print(e)
        raise Error("Error on creating roles.")


def create_users(users):
    try:
        for user in users:
            new_user = User(
                username=user["username"],
                password=user["password"],
                email=user["email"],
                role=Role.query.filter_by(name=user["role"]).first(),
                birthdate=datetime.fromisoformat(user["birthdate"]),
            )
            db.session.add(new_user)

        db.session.commit()
    except Exception as e:
        print(e)
        raise Error("Error on creating users.")


def create_posts(posts):
    try:
        for post in posts:
            new_post = Post(text=post["text"], author_id=post["author_id"])
            db.session.add(new_post)

        db.session.commit()
    except Exception as e:
        print(e)
        raise Error("Error on creating posts.")


def main():
    resources_dir = os.path.join(basedir, "resources")

    with open(os.path.join(resources_dir, "roles.csv"), "r") as roles_file, open(
        os.path.join(resources_dir, "users.csv"), "r"
    ) as users_file, open(
        os.path.join(resources_dir, "posts.csv"), "r"
    ) as posts_file, app.app_context():

        roles = csv.DictReader(roles_file)
        users = csv.DictReader(users_file)
        posts = csv.DictReader(posts_file)

        create_roles(roles)
        create_users(users)
        create_posts(posts)


if __name__ == "__main__":
    main()
