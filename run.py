# import the create app application factory
from formelwizzard_app import create_app

# import the application config classes
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = create_app()

if __name__ == '__main__':
    app.run()