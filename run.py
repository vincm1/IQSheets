# import the create app application factory
from formelwizzard_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()