# backend/api/uploads.py

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.uploads.item_csv_service import upload_item_csv
from services.uploads.generic_csv_service import upload_generic_csv

uploads_bp = Blueprint(
    "uploads",
    __name__,
    url_prefix="/api/uploads"
)

# --------------------------------------------------
# ITEM CSV UPLOAD
# --------------------------------------------------
@uploads_bp.route("/items/csv", methods=["POST"])
@jwt_required()
def upload_items_csv():
    """
    Upload item CSV
    POST /api/uploads/items/csv
    """
    return upload_item_csv(request)


# --------------------------------------------------
# GENERIC CSV UPLOAD (CREATE TABLE FROM CSV)
# --------------------------------------------------
@uploads_bp.route("/generic/csv", methods=["POST"])
@jwt_required()
def upload_generic():
    """
    Upload any CSV and create table dynamically
    POST /api/uploads/generic/csv
    """
    return upload_generic_csv(request)
