""" Flask blueprint for retrieving relative keywords. There are two ways
that relative keywords may be accessed:
    - for a particular document
    - for all documents in a group

The relative keyword API will invoke the group API if needed to determine
the groups from which to extract relative keywords. """

from flask import (
        Blueprint, request
    )


bp = Blueprint('relative_keywords', __name__, url_prefix="/api")

@bp.route('/documents/<int:doc_id>/relative_keywords', methods=["GET"])
#@auth.login_required
def document_relative_keywords(doc_id, check_owner=True):
    """ Retrieves the relative keywords for the specified document. """
    response = None

    if request.method == "GET":
        pass


    if not response:
        response = {"message": "Not implemented."}

    return response


@bp.route('/groups/<int:group_id>/relative_keywords', methods=["GET"])
#@auth.login_required
def group(group_id, check_owner=True):
    """ Retrieves the relative keywords associated with this particular group.
    Note that the group keywords are only those that are chosen for this
    group. In theory a document in group A may belong also to group B and
    so its keywords are the union of the keywords of A and of B. """
    response = None

    if request.method == "GET":
        pass
       

    if not response:
        response = {"message": "Not implemented."}

    return response
