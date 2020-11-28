""" Flask blueprint for the retrieval of absolute keywords. These keywords
are created when a document is added. The keywords may then be retrieved."""

from flask import (
        Blueprint, g, make_response
    )

#from flask_httpauth import HTTPBasicAuth

from keywords_service.auth import auth
from keywords_service.db import get_db


bp = Blueprint('absolute_keywords', __name__, url_prefix="/api/documents")

@bp.route('/<int:doc_id>/absolute_keywords', methods=["GET"])
@auth.login_required
def absolute_keywords(doc_id, check_owner=True):
    """ Fetches the keywords for a document that were created when the
    document was added. Returns a dictionary / key-value set where
    the keys are keywords and values are weights. """

    response = None

    _, cur = get_db()

    cur.execute(
            'SELECT d.created, d.uri, d.owner_id'
            ' FROM document d'
            ' WHERE d.id = %s', (doc_id,)
        )
    doc_info = cur.fetchone()

    if doc_info is None:
        response = make_response({"message":
            "Document with id {} doesn't exist.".format(doc_id)},
            400)

    if not response:
        if check_owner and doc_info['owner_id'] != g.user:
            response = make_response({"message" :
                "Insufficient privileges."}, 403)

    if not response:
        cur.execute(
            'SELECT keyword_text, keyword_weight'
            ' FROM keyword'
            ' WHERE document_id = %s'
            ' ORDER BY keyword_weight DESC', (doc_id,)
        )
        response = dict(cur.fetchall())

    return response
