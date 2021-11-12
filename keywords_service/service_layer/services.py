from typing import Tuple, Dict, Optional

from keywords_service.domain import (
	document, collection, document_similarity
)

from keywords_service.service_layer.unit_of_work import AbstractUnitOfWork


# public
def create_document_metadata(loc: str, description: str) -> document.DocumentMetadata:
	return document.DocumentMetadata(loc, description)


def update_model(meta: document.DocumentMetadata, contents: str, uow: AbstractUnitOfWork) -> Tuple[bool, str]:
	with uow:
		doc = create_document_node(meta, contents)
		if uow.collection.getDocumentRepository().add(doc):
			uow.collection.getCollection().add(doc)
			uow.commit()
			return True, doc.identifier
		else:
			return False, doc.identifier


'''
def query_model(identifier: str, uow: AbstractUnitOfWork) -> Set[str]:

'''
def query_for_absolute_keywords(identifier: str, uow: AbstractUnitOfWork) -> Optional[Dict[str, float]]:
	keywords = None
	
	with uow:
		doc = uow.collection.getDocumentRepository().get(identifier)

		if doc is not None:
			keywords = { k.keyword: k.weight for k in doc.content.data.values()}

	return keywords

	

'''
explore_model(uow: AbstractUnitOfWork) -> ModelSummary:

find_identifier(query: str, uow: AbstractUnitOfWork) -> Optional[List[str]]:
'''
## private


def create_document_node(meta: document.DocumentMetadata, contents: str) -> document.DocumentNode:
	return document.DocumentNode(meta, contents)

'''
create_document_edge(left: DocumentNode, right: DocumentNode) -> DocumentEdge:

create_collection_subgraph(base: CollectionGraph, thresh: float): -> CollectionSubgraph:

create_document_group(nodes: Set[DocumentNode]) -> DocumentGroup:

collect_keywords(identifier: AbstractDocumentIdentifier, source: CollectionSubgraph) -> Set[Keyword]:

'''