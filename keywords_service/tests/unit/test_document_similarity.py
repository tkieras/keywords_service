from keywords_service.domain import (
	document_similarity, document, weighted_keywords
)

def build_data(data_dict):
	return {k : weighted_keywords.WeightedKeyword(k, v) for k, v in data_dict.items()}

def test_compare():
	dummy_meta = document.DocumentMetadata("blah", "blah")

	doc_A = document.DocumentNode(dummy_meta, "very different words")
	doc_B = document.DocumentNode(dummy_meta, "content of doc b")
	doc_C = document.DocumentNode(dummy_meta, "content of doc b")


	assert(document_similarity.compare(doc_A, doc_B) < 
		   document_similarity.compare(doc_B, doc_C))

def test_jaccard():
	a = build_data({"1":1.0, "2":1.0, "3":1.0})
	b = build_data({"3":1.0, "4":1.0, "5":1.0})

	assert(document_similarity.jaccard(a, b) == (1/5))

def test_weighted_jaccard():
	a = build_data({"1":1.0, "2":1.0, "3":1.0})
	b = build_data({"3":1.0, "4":1.0, "5":1.0})

	assert(document_similarity.weighted_jaccard(a, b) == (1/5))

	a = build_data({"1":1.0, "2":1.0, "3":0.5})
	b = build_data({"3":0.5, "4":1.0, "5":1.0})

	assert(document_similarity.weighted_jaccard(a, b) == (1/9))

	a = build_data({"1":1.0, "2":1.0, "3":0.0})
	b = build_data({"3":0.0, "4":1.0, "5":1.0})

	assert(document_similarity.weighted_jaccard(a, b) == (0))


