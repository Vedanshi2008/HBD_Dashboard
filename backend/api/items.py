# backend/api/items.py

from flask import Blueprint
from flask_jwt_extended import jwt_required

from services.items.item_query_service import (
    get_complete_items,
    get_incomplete_items,
    download_incomplete_items_csv
)
from services.items.duplicate_service import (
    get_duplicate_items,
    delete_duplicate_items
)

items_bp = Blueprint(
    "items",
    __name__,
    url_prefix="/api/items"
)

# --------------------------------------------------
# ITEMS READ APIs
# --------------------------------------------------

@items_bp.route("/complete", methods=["GET"])
@jwt_required()
def complete_items():
    """
    Fetch paginated complete items
    """
    return get_complete_items()


@items_bp.route("/incomplete", methods=["GET"])
@jwt_required()
def incomplete_items():
    """
    Fetch paginated incomplete items
    """
    return get_incomplete_items()


# --------------------------------------------------
# CSV DOWNLOAD
# --------------------------------------------------

@items_bp.route("/incomplete/csv", methods=["GET"])
@jwt_required()
def download_incomplete_csv():
    """
    Download incomplete items as CSV (streamed)
    """
    return download_incomplete_items_csv()


# --------------------------------------------------
# DUPLICATES MANAGEMENT
# --------------------------------------------------

@items_bp.route("/duplicates", methods=["GET"])
@jwt_required()
def fetch_duplicates():
    """
    Fetch duplicate items (paginated)
    """
    return get_duplicate_items()


@items_bp.route("/duplicates", methods=["DELETE"])
@jwt_required()
def remove_duplicates():
    """
    Delete selected duplicate item IDs
    """
    return delete_duplicate_items()
