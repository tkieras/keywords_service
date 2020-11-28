from conftest import test_users, make_header

test_input = {"uri" : "test", "content": "This is a test."}


def test_get_groups_normal(client):
	response = client.get('/api/groups', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200



def test_post_groups_normal(client):
	response = client.post('/api/groups', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200

def test_get_group_normal(client):
	response = client.get('/api/groups/0', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200


def test_delete_group_normal(client):
	response = client.delete('/api/groups/0', 
		headers=make_header(test_users[0]["username"], 
			test_users[0]["password"]))

	assert response.status_code == 200