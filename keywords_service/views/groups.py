""" Defines the flask blueprint for document groups.
Group creation is intended to be done without user supervision or input.
However it may be helpful to implement an API for creating a specifically
defined group. In this case there needs to be a corresponding API for deleting
the manually created group. In ordinary operation the user does not need
to call these methods, but they are exposed for reference and transparency.

At present there are no genera guarantees for consistency of the groups as
documents are added, since by design they may change as the document set
changes. However manually created groups are static and endure until
specifically deleted. """

from flask import (
        Blueprint, request
    )

from keywords_service.auth import auth
from keywords_service.db import get_db

bp = Blueprint('groups', __name__, url_prefix="/api/groups")

@bp.route('/', methods=["GET", "POST"])
@auth.login_required
def groups(check_owner=True):
    """ Getting the groups involves clustering and/or community detection
    in the document graph. Posting to groups will involve the user specifying
    that some set of documents belong to a group, which will be created and
    populated with those documents alone."""
    response = None

    if request.method == "GET":
        pass
        # db, cur = get_db()

    elif request.method == "POST":
        pass


    if not response:
        response = {"message": "Not implemented."}

    return response



@bp.route('/<int:group_id>', methods=["GET", "DELETE"])
@auth.login_required
def group(group_id, check_owner=True):
    """ To retrieve just a single group by group id. Or to delete a group.
    The only groups that can be deleted are those that were manually
    created."""
    response = None

    if request.method == "GET":
        pass
        # db, cur = get_db()

    elif request.method == "DELETE":
        pass


    if not response:
        response = {"message": "Not implemented."}

    return response
