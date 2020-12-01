""" Flask blueprint for core methods on documents. A document may be added
or deleted. Once added it becomes by default a member of the working set
from which groups are extracted. """

import hashlib

from flask import (
        Blueprint, g, request, url_for, make_response
    )

#from flask_httpauth import HTTPBasicAuth

from keywords_service.auth import auth
from keywords_service.db import get_db
from keywords_service.core.absolute_keywords import extract_keywords


bp = Blueprint('documents', __name__, url_prefix="/api/documents")

@bp.route('/', methods=["POST"])
@auth.login_required
def create_absolute_keywords():
    """ Post a document to add it to the working set.

    When a document is added the content is not stored in the database. Rather,
    the 'absolute keywords' are extracted along with their weights, and these
    are stored until the document is deleted. """

    error_messages = {"name" : "Key 'name' is required.",
                      "content": "Key 'content' is required.",
                      "empty" : "No data provided."}

    errors = []
    if not request.json:
        errors.append(error_messages["empty"])
    else:
        for key in ("name", "content"):
            if key not in request.json.keys():
                errors.append(error_messages[key])

    response = make_response({"message" : " ".join(errors)},
        400) if errors else None

    if not response:

        content = request.json["content"]
        checksum = hashlib.md5(content.encode('utf-8')).hexdigest()

        db, cur = get_db()

        cur.execute(
            'SELECT name, id, created FROM document'
            ' WHERE checksum = %s', (checksum,)
            )
        prior_creation = cur.fetchone()

        if prior_creation:
            response = make_response({"message":
                "Content was added at a prior time ({}).".format(
                    prior_creation["created"])},
                302)
            response.headers["Location"] = url_for(
                'absolute_keywords.absolute_keywords',
                doc_id=prior_creation["id"])

    if not response:

        name = request.json["name"]

        cur.execute(
                'INSERT INTO document (name, checksum, owner_id)'
                ' VALUES (%s, %s, %s)',
                (name, checksum, g.user)
            )

        db.commit()
        cur.execute('SELECT max(id) FROM document')
        doc_id = cur.fetchone()[0]

        keyword_data = extract_keywords(content)

        records = [(doc_id, keyword_text, keyword_weight)
            for keyword_text, keyword_weight in keyword_data.items()]

        for record in records:
            cur.execute(
                'INSERT INTO keyword'
                ' (document_id, keyword_text, keyword_weight)'
                ' VALUES (%s, %s, %s)',
                (record)
                )
        db.commit()

        response = make_response({"message":"Keywords created.", 
                                  "id":doc_id}, 201)
        response.headers["Location"] = url_for(
            'absolute_keywords.absolute_keywords', doc_id=doc_id)

    return response


@bp.route('/<int:doc_id>', methods=["DELETE"])
@auth.login_required
def delete(doc_id):
    """ Deletes a document and the keywords associated with it. May only be
    performed by the user that added the document. """
    response = None

    db, cur = get_db()
    cur.execute(
            'SELECT d.created, d.name, d.owner_id'
            ' FROM document d'
            ' WHERE d.id = %s', (doc_id,)
        )
    doc_info = cur.fetchone()

    if doc_info is None:
        response = make_response({"message":
            "Document with id {} doesn't exist.".format(doc_id)},
            400)

    if not response:
        if doc_info["owner_id"] != g.user:
            response = make_response({"message" :
                "Insufficient privileges."}, 403)

    if not response:

        cur.execute('DELETE FROM keyword WHERE document_id = %s', (doc_id,))
        cur.execute('DELETE FROM document WHERE id = %s', (doc_id,))
        db.commit()

        response = make_response({"message":
            "Document {} and its keywords deleted.".format(doc_id)})

    return response
