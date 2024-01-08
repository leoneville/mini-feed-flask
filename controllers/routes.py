from controllers import user_controller, auth_controller


def initialize_routes(app):
    blueprints = [
        auth_controller,
        user_controller
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
