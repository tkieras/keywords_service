from dataclasses import dataclass


@dataclass
class GroupDocumentEntry:
	group_id: int
	similarity_threshold: float
	document: str


@dataclass
class GroupKeywordEntry:
	group_id: int
	keyword: str

