# routes/items_data.py

from flask import Blueprint, jsonify, request
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from model.item_csv_model import ItemData


item_bp = Blueprint("items", __name__)


# --------------------------------------------------
# Helper: serialize SQLAlchemy object
# --------------------------------------------------
def serialize(item):
    return {
        column.name: getattr(item, column.name)
        for column in item.__table__.columns
    }


# --------------------------------------------------
# Pagination utility
# --------------------------------------------------
def paginate(query, page, limit):
    total = query.count()
    items = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total // limit) + (1 if total % limit else 0),
        "items": [serialize(item) for item in items],
    }


# --------------------------------------------------
# Complete Items API
# --------------------------------------------------
@item_bp.route("/complete", methods=["GET"])
def get_complete_items():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 1000))

        query = db.session.query(ItemData).filter(
            # name required
            ItemData.name.isnot(None),
            ItemData.name != "",

            # at least one phone required
            or_(
                and_(ItemData.phone_no_1.isnot(None), ItemData.phone_no_1 != ""),
                and_(ItemData.phone_no_2.isnot(None), ItemData.phone_no_2 != ""),
                and_(ItemData.phone_no_3.isnot(None), ItemData.phone_no_3 != ""),
                and_(ItemData.whatsapp_no.isnot(None), ItemData.whatsapp_no != ""),
                and_(ItemData.virtual_phone_no.isnot(None), ItemData.virtual_phone_no != ""),
            ),

            # category required
            ItemData.category.isnot(None),
            ItemData.category != "",

            # sub category required
            ItemData.sub_category.isnot(None),
            ItemData.sub_category != "",

            # area required
            ItemData.area.isnot(None),
            ItemData.area != "",

            # city required
            ItemData.city.isnot(None),
            ItemData.city != "",
        )

        return jsonify(paginate(query, page, limit)), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# Incomplete Items API
# --------------------------------------------------
@item_bp.route("/incomplete", methods=["GET"])
def get_incomplete_items():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 1000))

        query = db.session.query(ItemData).filter(
            or_(
                # name missing
                ItemData.name.is_(None),
                ItemData.name == "",

                # all phones missing
                and_(
                    or_(ItemData.phone_no_1.is_(None), ItemData.phone_no_1 == ""),
                    or_(ItemData.phone_no_2.is_(None), ItemData.phone_no_2 == ""),
                    or_(ItemData.phone_no_3.is_(None), ItemData.phone_no_3 == ""),
                    or_(ItemData.whatsapp_no.is_(None), ItemData.whatsapp_no == ""),
                    or_(ItemData.virtual_phone_no.is_(None), ItemData.virtual_phone_no == ""),
                ),

                # category missing
                ItemData.category.is_(None),
                ItemData.category == "",

                # sub category missing
                ItemData.sub_category.is_(None),
                ItemData.sub_category == "",

                # area missing
                ItemData.area.is_(None),
                ItemData.area == "",

                # city missing
                ItemData.city.is_(None),
                ItemData.city == "",
            )
        )

        return jsonify(paginate(query, page, limit)), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
