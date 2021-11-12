""" Flask blueprint for core methods on documents. A document may be added
or deleted. Once added it becomes by default a member of the working set
from which groups are extracted. """


from flask import (
        Blueprint, g, request, url_for, make_response
    )

#from flask_httpauth import HTTPBasicAuth

from keywords_service.service_layer import services

bp = Blueprint('documents', __name__, url_prefix="/api/documents")

@bp.route('/', methods=["POST"])
#@auth.login_required
def create_absolute_keywords():
    """ Post a document to add it to the working set.

    When a document is added the content is not stored in the database. Rather,
    the 'absolute keywords' are extracted along with their weights, and these
    are stored until the document is deleted. """

    error_messages = {"name" : "Key 'name' is required.",
                      "content": "Key 'content' is required.",
                      "empty" : "No data provided."}

    errors = []
    response = None

    if not request.json:
        errors.append(error_messages["empty"])
    else:
        for key in ("name", "content"):
            if key not in request.json.keys():
                errors.append(error_messages[key])

    if errors:
        response = make_response({"message" : " ".join(errors)}, 400)

    else:
        meta = services.create_document_metadata(request.get("name"), 
            request.get("description", None))

        status, identifier = services.update_model(meta, 
            request.get("content"), uow)

        if status == False:
            response = make_response({"message":
                "Content was already added."}, 302)
            response.headers["Location"] = url_for(
                'absolute_keywords.absolute_keywords',
                doc_id=identifier)

        else:
            response = make_response({"message":"Keywords created.", 
                                  "id": identifier}, 201)
            response.headers["Location"] = url_for(
            'absolute_keywords.absolute_keywords', doc_id=identifier)

    return response


@bp.route('/<int:doc_id>', methods=["DELETE"])
@auth.login_required
def delete(doc_id):
    """ Deletes a document and the keywords associated with it. May only be
    performed by the user that added the document. """
    response = None

    # if doc_info is None:
    #     response = make_response({"message":
    #         "Document with id {} doesn't exist.".format(doc_id)},
    #         400)

    # if not response:
    #     if doc_info["owner_id"] != g.user:
    #         response = make_response({"message" :
    #             "Insufficient privileges."}, 403)

    # if not response:

    #     response = make_response({"message":
    #         "Document {} and its keywords deleted.".format(doc_id)})

    if not response:
        response = {"message": "Not implemented."}

    return response
