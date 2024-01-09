"""Module docstring """
import os
# import the create app application factory
from iqsheets_app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    app.run()
