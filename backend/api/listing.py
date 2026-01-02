# backend/api/listing.py

from flask import Blueprint, request, jsonify
from services.listing.upload_service import handle_listing_upload

listing_bp = Blueprint(
    "listing",
    __name__,
    url_prefix="/api/listings"
)

@listing_bp.route("/<source>/upload", methods=["POST"])
def upload_listing(source):
    """
    Generic upload endpoint for all listing sources.
    Examples:
    POST /api/listings/atm/upload
    POST /api/listings/bank/upload
    POST /api/listings/asklaila/upload
    """
    return handle_listing_upload(source, request)
