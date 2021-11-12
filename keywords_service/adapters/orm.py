from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, Float,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from keywords_service.domain import (
	document,
	weighted_keywords
)

metadata = MetaData()

tbl_document_metadata = Table(
	'document_metadata', metadata, 
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('loc', String(255)),
	Column('date_added', Date),
	Column('description', String(255)),
	Column('doc_id', Integer, ForeignKey('document_node.id'))
)

# tbl_document_identifier = Table(
# 	'document_identifier', metadata,
# 	Column('id', Integer, primary_key=True, autoincrement=True),
# 	Column('digest', String(255)),
# 	Column('doc_id', Integer, ForeignKey('document_node.id'))
# )

# tbl_weighted_keywords = Table(
# 	'weighted_keywords', metadata,
# 	Column('id', Integer, primary_key=True, autoincrement=True),
# 	Column('keyword', String(255)),
# 	Column('weight', Float),
# 	Column('doc_content_id', Integer, ForeignKey('document_content.id'))
# )

# tbl_document_content = Table(
# 	'document_content', metadata,
# 	Column('id', Integer, primary_key=True, autoincrement=True),
# 	Column('doc_id', Integer, ForeignKey('document_node.id')))


tbl_document_node = Table(
	'document_node', metadata, 
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('identifier', String(255))
)




def start_mappers():
	mapper(document.DocumentMetadata, tbl_document_metadata)
	
	#mapper(document_identifier.Md5DigestDocumentIdentifier, tbl_document_identifier)

	#mapper(weighted_keywords.WeightedKeyword, tbl_weighted_keywords)

	# mapper(document_content.WeightedKeywordDocumentContent, tbl_document_content,
	# 	properties={
	# 		'data' : relationship(weighted_keywords.WeightedKeyword,
	# 			backref='tbl_document_content',
	# 			collection_class=attribute_mapped_collection("keyword"))
	# 	})

	mapper(document.DocumentNode, tbl_document_node, 
		properties={
			'meta' : relationship(document.DocumentMetadata, 
						backref='tbl_document_node',
						uselist=False),
			# 'identifier' : relationship(document_identifier.Md5DigestDocumentIdentifier,
			# 			backref='tbl_document_node',
			# 			uselist=False),
		})