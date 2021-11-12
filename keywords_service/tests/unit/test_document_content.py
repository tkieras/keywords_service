from keywords_service.domain import document

def test_basic_minimal():
	doc_content = document.WeightedKeywordDocumentContent("testing function")
	assert isinstance(doc_content, document.AbstractDocumentContent)

	assert "testing" in doc_content.data or "function" in doc_content.data