from controllers import user_controller, auth_controller, post_controller


def initialize_routes(app):
    blueprints = [
        auth_controller,
        user_controller,
        post_controller
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
