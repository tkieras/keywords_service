from conftest import test_users, make_header

test_input = {"name" : "test", "content": "This is a test."}


def test_get_normal(client):
	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 201
	location = response.headers["Location"]

	response = client.get(location,
		headers=make_header(test_users[0]["username"],
			test_users[0]["password"]))

	assert response.status_code == 200
	assert len(response.json) > 0
	assert "test" in response.json.keys() or "this" in response.json.keys()
	assert not "a" in response.json.keys()


def test_get_not_exist(client):

	response = client.get("/api/documents/32/absolute_keywords",
		headers=make_header(test_users[0]["username"],
			test_users[0]["password"]))

	assert response.status_code == 400
	assert "message" in response.json

def test_get_wrong_user(client):
	response = client.post('/api/documents', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]),
		json=test_input)

	assert response.status_code == 201
	location = response.headers["Location"]

	response = client.get(location,
		headers=make_header(test_users[1]["username"],
			test_users[1]["password"]))

	assert response.status_code == 403