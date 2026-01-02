# routes/amazon_product.py

from flask import Blueprint, jsonify
from sqlalchemy import not_
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from model.amazon_product_model import AmazonProduct


amazon_products_bp = Blueprint("products", __name__)


# --------------------------------------------------
# Helper: filter complete products
# --------------------------------------------------
def is_complete_query(query):
    return query.filter(
        AmazonProduct.product_name.isnot(None),
        AmazonProduct.product_name != "",
        AmazonProduct.category.isnot(None),
        AmazonProduct.category != "",
        AmazonProduct.subcategory.isnot(None),
        AmazonProduct.subcategory != "",
        AmazonProduct.description.isnot(None),
        AmazonProduct.description != "",
    )


# --------------------------------------------------
# Get complete products
# --------------------------------------------------
@amazon_products_bp.route("/products/complete", methods=["GET"])
def get_complete_products():
    try:
        query = db.session.query(AmazonProduct)
        products = is_complete_query(query).all()

        result = [
            {column.name: getattr(p, column.name) for column in p.__table__.columns}
            for p in products
        ]

        return jsonify({
            "count": len(result),
            "data": result
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# Get incomplete products
# --------------------------------------------------
@amazon_products_bp.route("/products/incomplete", methods=["GET"])
def get_incomplete_products():
    try:
        complete_ids = [
            p.id
            for p in is_complete_query(db.session.query(AmazonProduct)).all()
        ]

        query = db.session.query(AmazonProduct)

        if complete_ids:
            products = query.filter(
                not_(AmazonProduct.id.in_(complete_ids))
            ).all()
        else:
            products = query.all()

        result = [
            {column.name: getattr(p, column.name) for column in p.__table__.columns}
            for p in products
        ]

        return jsonify({
            "count": len(result),
            "data": result
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
