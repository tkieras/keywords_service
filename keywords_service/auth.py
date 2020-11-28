""" Holds functions necessary for authentication:
Within the blueprint:
    - route for registration of a new user.
    - route for obtaining a secure token.

Helper functions for:
    - username/password verification
    - generation/verification of token
"""

from flask import (
        Blueprint, g, request, make_response,
        current_app)

from flask_httpauth import HTTPBasicAuth

from werkzeug.security import check_password_hash, generate_password_hash

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from keywords_service.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth = HTTPBasicAuth()


@bp.route('/register', methods=["POST"])
def register():
    """ API for registration of a new user. """
    error_messages = {"username" : "Key 'username' is required.",
                      "password": "Key 'password' is required."}

    errors = []
    for key in error_messages:
        if key not in request.json:
            errors.append(error_messages[key])

    response = make_response({"message" : " ".join(errors)},
        400) if errors else None


    if not response:

        username = request.json['username']
        password = request.json['password']

        db, cur = get_db()

        cur.execute('SELECT id FROM users WHERE username = %s',
            (username,))

        user_exists = cur.fetchone()
        if user_exists:
            response = make_response({"message":
                "User {} is already registered.".format(username)},
            400)

    if not response:
        cur.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (username, generate_password_hash(password))
        )
        db.commit()

        cur.execute('SELECT max(id) FROM users')
        user_id = cur.fetchone()[0]

        response = make_response({"message" :
            "User {} created.".format(username),
            "id" : user_id})

    return response


@auth.verify_password
def verify_password(username_or_token, password):
    """ Verification function used by flask_httpauth. Expects either a
    username and password, or a token. The token is checked first, and
    username/password verification only proceeds if the token fails.
    If a valid token is provided the password variable is never used."""
    verification_result = False

    user = verify_auth_token(username_or_token)
    if user:
        verification_result = True
        g.user = user

    else:

        _, cur = get_db()

        cur.execute(
            'SELECT id, password FROM users WHERE username = %s',
            (username_or_token,)
            )
        user = cur.fetchone()


        if user and check_password_hash(user["password"], password):
            g.user = user["id"]
            verification_result = True

    return verification_result



@bp.route('/token', methods=["GET"])
@auth.login_required
def request_token():
    """ API for requesting a secure token."""
    return {"token" : generate_auth_token(g.user).decode('ascii')}


def generate_auth_token(user_id, expiration=600):
    """ Generates a secure token that expires after the specified time."""

    serializer = Serializer(current_app.config['SECRET_KEY'],
        expires_in=expiration)

    return serializer.dumps({"id" : user_id})

def verify_auth_token(token):
    """ Verifies a token. If verificiation succeeds, the return value is the
    user_id of the user that obtained the token."""
    serializer = Serializer(current_app.config['SECRET_KEY'])

    user_id = None

    try:
        data = serializer.loads(token)
        _, cur = get_db()

        cur.execute(
            'SELECT id FROM users WHERE id = %s',
            (data["id"],)
            )
        user_id = cur.fetchone()[0]

    except (SignatureExpired, BadSignature):
        pass

    return user_id
