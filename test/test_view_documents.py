from conftest import test_users, make_header

test_input = {"uri" : "test", "content": "This is a test."}

def test_post_empty(client):

	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=None)

	assert response.status_code == 400
	assert "message" in response.json

def test_post_no_content(client):

	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json={"uri": "test"})

	assert response.status_code == 400
	assert "message" in response.json


def test_post_no_uri(client):

	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json={"content": "This is a test."})

	assert response.status_code == 400
	assert "message" in response.json

def test_post_normal(client):
	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 201
	assert "Location" in response.headers
	assert "message" in response.json


def test_post_repeat(client):
	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 201
	assert "message" in response.json


	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 302
	assert "message" in response.json


def test_post_normal_no_auth(client):
	response = client.post('/api/documents',
		json=test_input)

	assert response.status_code == 401

def test_delete_normal(client):
	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 201
	assert "Location" in response.headers
	assert "message" in response.json

	location = response.headers["Location"].split("/")
	id = None
	
	for w in location:
		try:
			id = int(w)
		except ValueError:
			pass

	assert id is not None
	response = client.delete('/api/documents/' + str(id),
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200
	assert "message" in response.json

	response = client.delete('/api/documents/' + str(id),
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 400
	assert "message" in response.json

def test_delete_wrong_user(client):
	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 201
	assert "Location" in response.headers
	assert "message" in response.json

	location = response.headers["Location"].split("/")
	id = None
	
	for w in location:
		try:
			id = int(w)
		except ValueError:
			pass

	assert id is not None
	response = client.delete('/api/documents/' + str(id),
		headers=make_header(test_users[1]["username"], 
			test_users[1]["password"]))

	assert response.status_code == 403
	assert "message" in response.json

	response = client.delete('/api/documents/' + str(id),
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200
	assert "message" in response.json