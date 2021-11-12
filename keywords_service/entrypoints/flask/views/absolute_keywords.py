""" Flask blueprint for the retrieval of absolute keywords. These keywords
are created when a document is added. The keywords may then be retrieved."""

from flask import (
        Blueprint, g, make_response
    )

from keywords_service.service_layer import services

bp = Blueprint('absolute_keywords', __name__, url_prefix="/api/documents")

@bp.route('/<int:doc_id>/absolute_keywords', methods=["GET"])
#@auth.login_required
def absolute_keywords(doc_id):
    """ Fetches the keywords for a document that were created when the
    document was added. Returns a dictionary / key-value set where
    the keys are keywords and values are weights. """

    response = None

    query = services.query_model(doc_id, uow)

    if query is None:
        response = make_response({"message":
            "Document with id {} doesn't exist.".format(doc_id)}, 400)
    else:
        response = query
   
    # if not response:
    #     if check_owner and doc_info['owner_id'] != g.user:
    #         response = make_response({"message" :
    #             "Insufficient privileges."}, 403)

    return response
