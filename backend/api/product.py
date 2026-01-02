# backend/api/product.py

from flask import Blueprint, request
from services.product.upload_service import handle_product_upload

product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/api/products"
)


@product_bp.route("/<source>/upload", methods=["POST"])
def upload_product(source):
    """
    Generic product upload endpoint

    Examples:
    POST /api/products/amazon/upload
    POST /api/products/big-basket/upload
    POST /api/products/vivo/upload
    """
    return handle_product_upload(source, request)
