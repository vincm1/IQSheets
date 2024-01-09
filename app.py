"""Module docstring """
# import the create app application factory
import os
from iqsheets_app import create_app

if __name__ == '__main__':
    app = create_app(os.getenv('ENV') or 'development')
    app.run()
