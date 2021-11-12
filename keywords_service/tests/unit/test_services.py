from typing import Optional

from keywords_service.adapters import repository
from keywords_service.service_layer import (
	services, unit_of_work
)

from keywords_service.domain import (
	document, collection
)

class FakeCollectionRepository(repository.AbstractCollectionRepository):
	def __init__(self):
		self.data = collection.CollectionGraph()

	def getCollection(self) -> Optional[collection.CollectionGraph]:
		return self.data
		
	def setCollection(self, update: collection.CollectionGraph) -> bool:
		self.data = update
		return True


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
	
	def __init__(self):
		self.collection = FakeCollectionRepository()
		self.committed = False

	def __enter__(self):
		pass

	def commit(self):
		self.committed = True

	def rollback(self):
		pass



def test_add_document():
	uow = FakeUnitOfWork()

	assert(len(uow.collection.getDocumentRepository().data) == 0)

	md = services.create_document_metadata("/usr/lib", "test doc")

	status, identifier = services.update_model(md,"test content", uow)
	
	assert(len(uow.collection.getDocumentRepository().data) == 1)

	retr = uow.collection.getDocumentRepository().get(identifier)

	assert(retr is not None)

	assert(retr.meta.loc == "/usr/lib")


def test_retrieve_absolute_keywords():
	uow = FakeUnitOfWork()

	md = services.create_document_metadata("/usr/lib", "test doc")

	status, identifier = services.update_model(md,"test content", uow)
	
	keywords = services.query_for_absolute_keywords(identifier, uow)

	assert(keywords is not None)

	assert "content" in keywords or "test" in keywords