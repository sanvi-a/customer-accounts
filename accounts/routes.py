"""REST API routes for the Accounts service."""
from flask import Blueprint, jsonify, make_response, request, url_for

from accounts.models import Account, DataValidationError

bp = Blueprint("accounts", __name__)

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415


@bp.route("/")
def index():
    """Root URL response."""
    paths = url_for("accounts.list_accounts", _external=True)
    return jsonify(name="Account REST API Service", version="1.0", paths=paths), HTTP_200_OK


@bp.route("/health")
def health():
    """Health check used by Kubernetes probes."""
    return jsonify(status="OK"), HTTP_200_OK


@bp.route("/accounts", methods=["POST"])
def create_accounts():
    """Create an Account."""
    if not request.is_json:
        return make_response(jsonify(error="Content-Type must be application/json"), HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    try:
        account = Account().deserialize(request.get_json())
    except DataValidationError as error:
        return make_response(jsonify(error=str(error)), HTTP_400_BAD_REQUEST)
    account.create()
    location_url = url_for("accounts.read_accounts", account_id=account.id, _external=True)
    return make_response(jsonify(account.serialize()), HTTP_201_CREATED, {"Location": location_url})


@bp.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts."""
    return make_response(jsonify([account.serialize() for account in Account.all()]), HTTP_200_OK)


@bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    """Read a single Account."""
    account = Account.find(account_id)
    if not account:
        return make_response(jsonify(error=f"Account {account_id} not found"), HTTP_404_NOT_FOUND)
    return make_response(jsonify(account.serialize()), HTTP_200_OK)


@bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an Account."""
    account = Account.find(account_id)
    if not account:
        return make_response(jsonify(error=f"Account {account_id} not found"), HTTP_404_NOT_FOUND)
    if not request.is_json:
        return make_response(jsonify(error="Content-Type must be application/json"), HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    try:
        account.deserialize(request.get_json())
    except DataValidationError as error:
        return make_response(jsonify(error=str(error)), HTTP_400_BAD_REQUEST)
    account.update()
    return make_response(jsonify(account.serialize()), HTTP_200_OK)


@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account."""
    account = Account.find(account_id)
    if account:
        account.delete()
    return make_response("", HTTP_204_NO_CONTENT)
