import os
from factory import create_app

config_class = os.environ.get("CONFIG_CLASS", "config.DevelopmentConfig")
print(config_class)

app = create_app(config_class)

if __name__ == '__main__':
    app.run()
