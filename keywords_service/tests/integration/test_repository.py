from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from keywords_service.adapters import repository, orm
from keywords_service.domain import (
	document, collection
)


def test_repository_can_add_retrieve(session):
	md = document.DocumentMetadata("/usr/lib", "test doc")

	doc = document.DocumentNode(md, "test content")

	repo = repository.SqlAlchemyDocumentRepository(session)

	repo.add(doc)

	retrieved = repo.get(doc.identifier)

	assert(retrieved is not None)


def test_repository_handles_request_failure(session):

	repo = repository.SqlAlchemyDocumentRepository(session)

	bad = repo.get("test")

	assert(bad is None)

	

def test_collection_can_add_retrieve(session):
	md = document.DocumentMetadata("/usr/lib", "test doc")

	doc = document.DocumentNode(md, "test content")

	doc_repo = repository.SqlAlchemyDocumentRepository(session)

	doc_repo.add(doc)

	repo = repository.SqlAlchemyCollectionRepository(session, doc_repo)

	repo.setCollection(collection.CollectionGraph())

	retrieved = repo.getCollection()

	assert(retrieved is not None)

	assert(repo.getDocumentRepository() == doc_repo)

	assert(repo.getDocumentRepository().get(doc.identifier) == doc)


def test_sqlalchemy_document(session):
	md = document.DocumentMetadata("/usr/lib", "test doc")

	doc = document.DocumentNode(md, "test content")

	repo = repository.SqlAlchemyDocumentRepository(session)

	repo.add(doc)

	retrieved = repo.get(doc.identifier)

	assert(retrieved is doc)

	# test that adding duplicate doc fails
	assert(not repo.add(doc))
	
	# test that getting returns None if doc by identifer doesn't exist
	bad = repo.get("this shouldn't exist")

	assert(bad is None)