from flask import g, appcontext_pushed

import pytest
from contextlib import contextmanager

from werkzeug.security import generate_password_hash
from requests.auth import _basic_auth_str

import keywords_service
from keywords_service.db import get_db
from keywords_service.auth import auth

test_users = [{"username": "test", "password": "test"},
			  {"username" : "imposter", "password": "impostertest"}]


def make_header(username, password):
	return { 'Authorization': _basic_auth_str(username, password) }

@pytest.fixture
def app():
	app = keywords_service.create_app()
	app.config["TESTING"] = True

	with app.app_context():
		db, cur = get_db()
		cur.execute('DELETE from keyword')
		cur.execute('DELETE from document')
		cur.execute('DELETE from users')
		db.commit()
		
		for user in test_users:
			username = user["username"]
			password = user["password"]
			cur.execute(
				'INSERT INTO users (username, password) VALUES (%s, %s)', 
				(username, generate_password_hash(password))
			)
		db.commit()

	yield app

	# # Clean up the database between tests
	# with app.app_context():
	# 	db, cur = get_db()
		

@pytest.fixture
def client(app, monkeypatch):
	client = app.test_client()
	#monkeypatch.setattr(auth, 'verify_password', lambda x, y: True)
	return client


# @contextmanager
# def user_set(app, user):
# 	def handler(sender, **kwargs):
# 		g.user = user
# 	with appcontext_pushed.connected_to(handler, app):
# 		yield
