import abc
from dataclasses import dataclass
import datetime
from typing import Set
import hashlib


from keywords_service.domain import (
	weighted_keywords
)


class DocumentMetadata:
	def __init__(self, loc: str, description: str):
		self.loc = loc
		self.date_added = datetime.datetime.now()
		self.description = description


class DocumentNode:
	def __init__(self, meta: DocumentMetadata,
					   content: str,
					   config = None):
		self.meta = meta
		self.identifier = create_md5_document_identifier(content)
		self.content = WeightedKeywordDocumentContent(content, config)


class AbstractDocumentContent(abc.ABC):
	@abc.abstractmethod
	def __init__(self, document_text: str):
		pass


class WeightedKeywordDocumentContent(AbstractDocumentContent):
	def __init__(self, document_text: str, config=None):
		self.data = weighted_keywords.extract(document_text, config)


def create_md5_document_identifier(content: str) -> str:
	return hashlib.md5(content.encode('utf-8')).hexdigest()