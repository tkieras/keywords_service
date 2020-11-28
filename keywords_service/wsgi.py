""" Exposes flask app for wsgi interface """

from keywords_service import create_app

app = create_app()
