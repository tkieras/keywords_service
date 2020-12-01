from conftest import test_users, make_header

test_input = {"name" : "test", "content": "This is a test."}


def test_get_normal_document(client):
	response = client.get('/api/documents/0/relative_keywords', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200

def test_get_normal_group(client):
	response = client.get('/api/groups/0/relative_keywords', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200
