
# Relative Keywords Service

![build](https://github.com/tkieras/keywords_service/workflows/build/badge.svg)

Implementation of a document content tagging service, using Flask and NLTK and available through a REST API. A user or client may retrieve the keywords provided by this service and assign them as tags in a file system, in browser bookmarks, or other databases. Most document content is discarded by the server after initial processing, though at this time for security and privacy reasons this service should not be used with sensitive data.

## Purpose: Tagging Documents Intelligently

Sometimes the best way to access a document is not by a single name, but by one of several possible keywords or tags that each represent the document's content in some way. When we force a document to have a single name, we must decide which of several names to choose, a decision that may or may not discard a lot of complexity and nuance. With tags we can have many tags and so allow more complexity to get captured.

However, a major drawback of tagging documents is that the number of tags can increase rapidly, with each tag representing only one or two documents. Navigating the tag set then becomes its own problem. To avoid this, the tagging process should consider not only the individual documents in isolation from each other, but also the entire set of documents that are being tagged. This will allow tags to be chosen so that the number of tags is reduced while retaining a high quality for individual tags.

## Usage

### Authentication

#### 1. Authentication methods:
All interactions except registration of a new user must be authenticated using HTTP Basic Authentication. Note that the server that presents this service to users should be configured with HTTPS. Two methods are supported:

* username/password
* auth_token

#### 2. Register a new user:
POST "/api/auth/register"
* { "username" : "your username"
  "password" : "your password" }

#### 3. Retrieve an authentication token:
GET "/api/auth/token"

### Documents

#### Add a document:
POST "/api/documents"
* {"name" : "name of your choosing",
  "content" : "text content here"}

Adding a document involves sending the text of the document to the server along with a name. The name may be any value, though it is suggested to use a URL or filepath.

When a document is added, the text content is processed, yielding a set of keywords called 'absolute keywords'. These are stored in the database for future use, while the raw text content is discarded. 

The document id is returned in the response body, and the path to the resource is in the Location header.

#### Delete a document
DELETE "/api/documents/<id>"

When a document is deleted, the keywords are no longer available for retrieval.

### Keywords

#### Retrieve absolute keywords
GET "/api/documents/<id>/absolute_keywords"

Basic keywords may be retrieved for a document. These represent document content independent of any other documents (absolute, as opposed to relative).

#### Retrieve relative keywords for a document

* Under construction

GET "/api/documents/<id>/relative_keywords"

Retrieving relative keywords are the primary use case for the API. After a document is added, the relative keywords may be retrieved. The algorithm for determining relative keywords is described elsewhere in this document.

#### Retrieve relative keywords for a group

* Under construction

GET "/api/group/<id>/relative_keywords"

The relative keywords of a document are the sum of the relative keywords that are attached to each group that the document belongs to. It may be useful to directly retrieve the relative keywords that belong to a specific group.

### Groups

#### Retrieve all groups

* Under construction

GET "/api/groups"

It may be useful to retrieve the groupings discovered in the document set. This method will return a dictionary where the key is the group id and the value is the list of document ids that belong to the group. Note that a single document may belong to several groups, depending on configuration options.

#### Retrieve the members of a single group

* Under construction

GET "/api/group/<id>"

It may be useful to retrieve the members of a particular group. This may be accomplished by this method.


## Algorithm Description

The process used here has several steps:

1. Preprocess the document contents to extract a small set of possible keywords.
2. Detect communities in the document set, where a user-defined threshold is used to indicate the similarity required for two documents to be adjacent.
3. For each detected community, assign a set of tags that represents the community. The tags are found by solving a max flow problem. Depending on user-defined parameters, the resulting tags will skew towards representing the commonalities, or toward representing the diversity of keywords found in the documents.

## Caveats

A feature of this approach is that the resulting tags for a given document will change depending on what other documents are also being tagged. In other words, the tags for a document are context dependent. As more documents are added, communities will evolve and the chosen tags for each community will reflect these changes.

As noted above, because tags are chosen at a group level, it is part of the intended behavior of this application that some tags to a document will not be keywords strictly found in the document itself. Depending on user-defined parameters, this will be more or less common. In such a case, the tag in question reflects keywords that are highly important to the group to which the document belongs. Therefore, the tag is assigned to the document because the document belongs to the group, and the tag reflects the group.

The inspiration for the algorithm comes from Wittgenstein's theory of family resemblance. In short, the notion is that common terms (i.e., 'dog', 'cat', 'game') do not need to reflect a conceptual 'least common denominator' or a definition that all members in the group share. Rather, membership in the group is assigned based on resemblance to other instances, and it may be impossible to discover a definition that all members in the group have in common. For the purpose of file tagging, the application of this theory is that not all documents in a cluster need to have a strictly shared topic, but rather they must all be related sufficiently closely to produce a family. Rather than give the family a single name (like 'cat', 'dog', 'game'), the family is named based on a heterogeneous set of keywords that, in general, captures what documents in the cluster are about. [Read more about Wittgenstein.](https://plato.stanford.edu/entries/wittgenstein/#LangGameFamiRese)


## Notes

The service requires several environment variables to be set:
	
* FLASK_SECRET_KEY
	* Per usual Flask.
* NLTK_DATA 
	* Must point to the folder `nltk_data` in this repository.
* POSTGRES_{USER, PASSWORD, HOST, PORT, DB}
		

