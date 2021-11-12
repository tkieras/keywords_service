import datetime

from keywords_service.domain import document

def test_basic():
	md = document.DocumentMetadata("/usr/lib", "a test")

	assert(md.loc == "/usr/lib")
	assert(md.date_added < datetime.datetime.now())
	assert(md.description == "a test")
