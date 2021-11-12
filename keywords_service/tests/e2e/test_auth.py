from conftest import test_users, make_header
from flask import g


def test_unauth_token(client):
	response = client.get('/api/auth/token', 
		headers=make_header(test_users[0]["username"], "wrong"))
	assert response.status_code == 401

def test_auth_token(client, app):
	response = client.get('/api/auth/token', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))
	assert response.status_code == 200

	try_again = client.get('/api/auth/token', 
		headers=make_header(response.json["token"], "unused"))

	assert try_again.status_code == 200


def test_bad_token(client, app):
	
	response = client.get('/api/auth/token', 
		headers=make_header("badtoken", "unused"))

	assert response.status_code == 401

def test_register(client):
	response = client.post('/api/auth/register', 
		json={"username": "testuser1", 
			  "password": "password"})

	assert response.status_code == 200
	assert "message" in response.json


def test_register_no_password(client):
	response = client.post('/api/auth/register', 
		json={"username": "testuser1"})

	assert response.status_code == 400
	assert "message" in response.json


def test_register_no_username(client):
	response = client.post('/api/auth/register', 
		json={"password": "password"})

	assert response.status_code == 400
	assert "message" in response.json


def test_duplicate_user_register(client):
	response = client.post('/api/auth/register', 
		json={"username": "testuser2", 
			  "password": "password"})

	assert response.status_code == 200

	response = client.post('/api/auth/register', 
		json={"username": "testuser2", 
			  "password": "password"})

	assert response.status_code == 400

