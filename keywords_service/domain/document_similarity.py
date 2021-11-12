from keywords_service.domain import document

class DocumentEdge:
	def __init__(self, left: document.DocumentNode, right: document.DocumentNode):
		self.left = left
		self.right = right
		self.weight = compare(left, right)


def compare(left: document.DocumentNode, right: document.DocumentNode):
	return weighted_jaccard(left.content.data, right.content.data)


def jaccard(A: dict, B: dict):
    A = set(A.keys())
    B = set(B.keys())
    num = len(A.intersection(B))
    denom = len(A) + len(B) - num
    return num/denom

def weighted_jaccard(A: dict, B: dict):
	unpack = lambda v: 0 if v is None else v.weight

	all_keys = set(A.keys()).union(set(B.keys()))

	num = 0
	denom = 0
	for k in all_keys:
		a = unpack(A.get(k, None))
		b = unpack(B.get(k, None))
		num += min(a, b)
		denom += max(a, b)

	return num / denom