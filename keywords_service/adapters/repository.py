import abc
from typing import Set, Optional, List

from keywords_service.domain.collection import CollectionGraph
from keywords_service.domain.document import DocumentNode



class AbstractRepository(abc.ABC):

	@abc.abstractmethod
	def getDocument(self, identifier: str) -> Optional[DocumentNode]:
		raise NotImplementedError

	@abc.abstractmethod
	def addDocument(self, doc: DocumentNode) -> bool:
		raise NotImplementedError

	@abc.abstractmethod
	def addDocumentEdge(self, edge: DocumentEdge) -> bool:
		raise NotImplementedError

	@abc.abstractmethod
	def addDocumentGroup(self, group: DocumentGroup) -> bool:
		raise NotImplementedError

	@abc.abstractmethod
	def listDocumentGroups(self) -> List[DocumentGroup]:
		raise NotImplementedError


class SqlAlchemyDocumentRepository(AbstractDocumentRepository):
	def __init__(self, session):
		self.session = session

	def get(self, identifier: str) -> Optional[DocumentNode]:

		return self.session.query(DocumentNode) \
						   .filter(DocumentNode.identifier == identifier) \
						   .first()

	def add(self, doc: DocumentNode) -> bool:

		exists = bool(self.session.query(DocumentNode) \
					   .filter(DocumentNode.identifier == doc.identifier) \
					   .count())

		if exists:
			return False

		self.session.add(doc)
		self.session.commit()

		return True

class SqlAlchemyCollectionRepository(AbstractCollectionRepository):
	def __init__(self, session, doc_repo):
		super().__init__(doc_repo)
		self.session = session

	def getCollection(self) -> Optional[CollectionGraph]:
		raise NotImplementedError

	def setCollection(self, update: CollectionGraph) -> bool:
		raise NotImplementedError

	def getDocumentRepository(self) -> AbstractDocumentRepository:
		return self.doc_repo