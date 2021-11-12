
from keywords_service.domain import document


def test_in_memory_basic(session):
	
	md = document.DocumentMetadata("/usr/lib", "a test")

	doc = document.DocumentNode(md, "test content")

	assert(any([k in doc.content.data for k in ["test", "content"]]))

	session.add(doc)

	session.commit()

	retr = session.query(document.DocumentNode).first()

	assert(retr is doc)

	assert(retr.meta.loc == "/usr/lib")

	assert(any([k in retr.content.data for k in ["test", "content"]]))

