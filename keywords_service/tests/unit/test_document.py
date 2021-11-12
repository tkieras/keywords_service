
from keywords_service.domain import document

def test_basic():
	md = document.DocumentMetadata("/usr/lib", "test doc")

	doc = document.DocumentNode(md, "test content")

	assert "content" in doc.content.data or "test" in doc.content.data

	