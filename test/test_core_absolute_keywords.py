from keywords_service.core import absolute_keywords

test_weights = {"keyword0": 0.0001,
			   "keyword1" : 0.05, 
	 		   "keyword2": 0.04, 
	 		   "keyword3": 0.03,
	 		   "keyword4": 0.02,
	 		   "keyword5": 0.01}

def test_basic_minimal():
	result = absolute_keywords.extract_keywords("testing function")
	assert type(result) == type(dict())
	assert "testing" in result.keys() or "function" in result.keys()

def test_basic_minimal_wrong():
	result = absolute_keywords.extract_keywords("second test")
	assert not("testing" in result.keys() or "function") in result.keys()

def test_basic_too_short():
	result = absolute_keywords.extract_keywords("a b c")
	assert len(result) == 0

def test_user_config():
	user_config = { "mistake": "discarded",
					"min_token_length": 1,
					"min_tag_length": 1,
					"ngram_max": 1,
					"keyword_threshold": 1.0}

	result = absolute_keywords.extract_keywords("x r z v", 
		user_config=user_config)
	assert list(result.keys()) == ["x", "r", "z", "v"]
	assert list(result.values()) == [0.25, 0.25, 0.25, 0.25]

def test_apply_threshold():
	result = absolute_keywords.apply_threshold(test_weights, goal=0.05)
	assert(len(result) == 1)
	assert("keyword1" in result.keys())

	result = absolute_keywords.apply_threshold(test_weights, goal=0.07)
	assert(len(result) == 2)
	assert("keyword1" in result.keys())
	assert("keyword2" in result.keys())

	result = absolute_keywords.apply_threshold(test_weights, goal=1.0)
	assert(len(result) == len(test_weights))
	assert result.keys() == test_weights.keys()

	result = absolute_keywords.apply_threshold(test_weights, goal=0)
	assert(len(result) == 0)

def test_calculate_weights():
	counts = {"keyword1" : 5, "keyword2": 3, "keyword3": 1}
	total = sum(counts.values())
	result = absolute_keywords.calculate_weights(counts, total)
	assert result == counts
	assert result["keyword1"] == 5/total
	assert result["keyword2"] == 3/total
	assert result["keyword3"] == 1/total


def test_get_ngrams():
	tokens = ["keyword1", "keyword2", "keyword3"]
	result = absolute_keywords.get_ngrams(tokens, max_n=2)
	assert len(result) == 2
	assert "keyword1_keyword2" in result
	assert "keyword2_keyword3" in result

	result = absolute_keywords.get_ngrams(tokens, max_n=3)
	assert len(result) == 3
	assert "keyword1_keyword2" in result
	assert "keyword2_keyword3" in result
	assert "keyword1_keyword2_keyword3" in result 


def test_lemmatize():
	words = ["catacombs", "babies", "food"]

	result = list(absolute_keywords.lemmatize(words))
	assert len(result) == 3
	assert "catacomb" in result
	assert "baby" in result
	assert "food"

def test_length_threshold():
	words = ["a", "ab", "abc", "abcd", "abcde"]

	result = list(absolute_keywords.length_threshold(words, threshold=3))

	assert len(result) == 3
	assert "a" not in result
	assert "ab" not in result

	result = list(absolute_keywords.length_threshold(words, threshold=10))

	assert len(result) == 0

def test_strip_punct():
	string = "a' punctuated... str.ing"

	result = absolute_keywords.strip_punct(string)
	assert result == "a punctuated string"

def test_stopwords():
	string = "the"
	result = absolute_keywords.not_stopword(string)
	assert not result

	string = "automobile"
	result = absolute_keywords.not_stopword(string)
	assert result

def test_cleanup_text():
	string = "a short test. Therefore, all is well, tip top and ship-shape."

	result = list(absolute_keywords.cleanup_text(string, threshold=3))

	assert result == ["short", "test", "therefore", 
					  "well", "tip", "top", "shipshape"]
	


