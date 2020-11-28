""" Implementation of core function for extract_keywords. This function
takes a string containing a body of text and returns a dictionary of
keywords and weights, where keywords with higher weights are more
important to the text. Default configuration values are explained here, but
may be overridden by passing a dictionary to extract_keywords.
    min_tag_length: Keywords shorter than min_tag_length are discarded
    min_token_length: Before constructing ngrams and possible keywords,
        tokens less than this length are discarded. This is useful
        to remove single characters, digits or roman numerals.
    ngram_max: Ngram construction iterates through the values from 1 to
        ngram_max, so that the set of possible keywords to choose from
        includes ngrams constructed at each value of n. If set to 1,
        no ngrams are used.
    keyword_threshold: Should be a float between 0 and 1.0, representing
        the fraction of the total set of possible keywords that will be
        returned from the function. Currently, the weights are simple
        fractions, such that the sum of all keyword weights will be the minimum
        number necessary to be equal or greater than the keyword_threshold.
"""

import re
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

DEFAULT_CONFIG = {
	"min_tag_length" : 3,
	"min_token_length" : 2,
	"ngram_max" : 2,
	"keyword_threshold" : 0.20,
}

stopwords = set(stopwords.words('english'))
punct = re.compile(r'[^\w\d\s]+')
lemmatizer = WordNetLemmatizer()


def extract_keywords(text, user_config=None):
    """ Main function for extracting a set of keywords from a text string. If
    a user_config dictionary is passed, containing keys are added/overwritten
    in the default config. Returns a dictionary keywords and weights."""
    config = DEFAULT_CONFIG
    if user_config:
        for key, value in user_config.items():
            config[key] = value

    text = cleanup_text(text, config["min_token_length"])
    tokens = list(lemmatize(text))
    tokens.extend(get_ngrams(tokens, config["ngram_max"]))
    tokens = length_threshold(tokens, config["min_tag_length"])


    counts, total = count_tokens(tokens)
    weights = calculate_weights(counts, total)

    keywords = apply_threshold(weights, config["keyword_threshold"])

    return keywords

def strip_punct(word):
    """ Removes punctuation from the word."""
    return re.sub(punct, '', word)

def lower(word):
    """ Lower case, necessary before WordNet Lemmatizer"""
    return word.lower()

def not_stopword(word):
    """ Checks against the previously loaded set of stopwords."""
    return word not in stopwords

def is_alpha(word):
    """ Excludes tokens that have numbers or other non-alpha characters."""
    return word.isalpha()

def min_length(word, thresh):
    """ Predicate for the length of a word """
    return len(word) >= thresh

def cleanup_text(text, threshold):
    """ Combines many simple functions to clean up the text. Takes a string.
    Returns an iterable."""
    pred_comb = lambda w: min_length(w, threshold) and \
                          not_stopword(w) and \
                          is_alpha(w)

    text = text.split()
    result = filter(pred_comb,
             map(strip_punct,
             map(lower, text)))

    return result

def length_threshold(text, threshold):
    """ Filters an iterable with a length threshold predicate."""
    return filter(lambda w: len(w) >= threshold, text)


def lemmatize(text):
    """ Maps a word to its lemma using the WordNet Lemmatizer."""
    return map(lambda w: lemmatizer.lemmatize(w), text)

def get_ngrams(tokens, max_n):
    """ Returns a list of ngrams from the range 2 up to and including max_n.
    This list will not include the original tokens, and so should be combined
    with the tokens by the caller if ngrams of n=1 are needed."""
    ngrams = []
    for ngram_size in range(2, max_n+1):
        ngrams_n = nltk.ngrams(tokens, ngram_size)
        ngrams.extend(["_".join(ngram) for ngram in ngrams_n])

    return ngrams

def count_tokens(tokens):
    """ Simple counter, returning counts and the total """
    counts = Counter(tokens)
    return counts, sum(counts.values())


def calculate_weights(counts, total):
    """ Modifies the counts dictionary in place to produce fractional weights.
    Each weight is the ratio of this keyword to the total size of the body
    of keywords. """
    for k in counts.keys():
        counts[k] /= total
    return counts


def apply_threshold(weights, goal):
    """ Returns a set of keywords such that the set is of minimal size,
    but the goal is met. The goal should be a float from 0 to 1.0 representing
    the fraction of the total body of keywords that should be represented
    by the keyword set. Currently weights are a simple fraction, so keywords
    are added until the sum of the added keyword weights meets or exceeds
    the goal."""
    all_keys = iter(sorted(weights.keys(), key=lambda k: weights[k],
        reverse=True))

    result = {}
    current = 0

    while current < goal:
        key = next(all_keys, None)
        if not key:
            break
        current += weights[key]
        result[key] = weights[key]

    return result
