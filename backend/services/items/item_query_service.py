# backend/services/items/item_query_service.py

from flask import request, jsonify, Response, stream_with_context
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
import csv
from io import StringIO

from extensions import db
from model.item_csv_model import ItemData


# --------------------------------------------------
# Serializer
# --------------------------------------------------
def _serialize(item: ItemData) -> dict:
    return {
        column.name: getattr(item, column.name)
        for column in item.__table__.columns
    }


# --------------------------------------------------
# Pagination helper
# --------------------------------------------------
def _paginate(query, page: int, limit: int) -> dict:
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
        "items": [_serialize(item) for item in items],
    }


# --------------------------------------------------
# COMPLETE ITEMS
# --------------------------------------------------
def get_complete_items():
    """
    Returns paginated complete items
    """
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = max(int(request.args.get("limit", 100)), 1)

        query = db.session.query(ItemData).filter(
            ItemData.name.isnot(None),
            ItemData.name != "",

            or_(
                and_(ItemData.phone_no_1.isnot(None), ItemData.phone_no_1 != ""),
                and_(ItemData.phone_no_2.isnot(None), ItemData.phone_no_2 != ""),
                and_(ItemData.phone_no_3.isnot(None), ItemData.phone_no_3 != ""),
                and_(ItemData.whatsapp_no.isnot(None), ItemData.whatsapp_no != ""),
                and_(ItemData.virtual_phone_no.isnot(None), ItemData.virtual_phone_no != ""),
            ),

            ItemData.category.isnot(None),
            ItemData.category != "",

            ItemData.sub_category.isnot(None),
            ItemData.sub_category != "",

            ItemData.area.isnot(None),
            ItemData.area != "",

            ItemData.city.isnot(None),
            ItemData.city != "",
        )

        return jsonify(_paginate(query, page, limit)), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500


# --------------------------------------------------
# INCOMPLETE ITEMS
# --------------------------------------------------
def get_incomplete_items():
    """
    Returns paginated incomplete items
    """
    try:
        page = max(int(request.args.get("page", 1)), 1)
        limit = max(int(request.args.get("limit", 100)), 1)

        query = db.session.query(ItemData).filter(
            or_(
                ItemData.name.is_(None),
                ItemData.name == "",

                and_(
                    or_(ItemData.phone_no_1.is_(None), ItemData.phone_no_1 == ""),
                    or_(ItemData.phone_no_2.is_(None), ItemData.phone_no_2 == ""),
                    or_(ItemData.phone_no_3.is_(None), ItemData.phone_no_3 == ""),
                    or_(ItemData.whatsapp_no.is_(None), ItemData.whatsapp_no == ""),
                    or_(ItemData.virtual_phone_no.is_(None), ItemData.virtual_phone_no == ""),
                ),

                ItemData.category.is_(None),
                ItemData.category == "",

                ItemData.sub_category.is_(None),
                ItemData.sub_category == "",

                ItemData.area.is_(None),
                ItemData.area == "",

                ItemData.city.is_(None),
                ItemData.city == "",
            )
        )

        return jsonify(_paginate(query, page, limit)), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500


# --------------------------------------------------
# DOWNLOAD INCOMPLETE ITEMS AS CSV (STREAMED)
# --------------------------------------------------
def download_incomplete_items_csv():
    """
    Stream CSV of incomplete items
    """

    def generate():
        try:
            query = (
                db.session.query(ItemData)
                .filter(
                    or_(
                        ItemData.name.is_(None),
                        ItemData.name == "",

                        and_(
                            or_(ItemData.phone_no_1.is_(None), ItemData.phone_no_1 == ""),
                            or_(ItemData.phone_no_2.is_(None), ItemData.phone_no_2 == ""),
                            or_(ItemData.phone_no_3.is_(None), ItemData.phone_no_3 == ""),
                            or_(ItemData.whatsapp_no.is_(None), ItemData.whatsapp_no == ""),
                            or_(ItemData.virtual_phone_no.is_(None), ItemData.virtual_phone_no == ""),
                        ),

                        ItemData.category.is_(None),
                        ItemData.category == "",

                        ItemData.sub_category.is_(None),
                        ItemData.sub_category == "",

                        or_(
                            and_(ItemData.address.is_(None), ItemData.area.is_(None)),
                            and_(ItemData.address == "", ItemData.area == ""),
                        ),

                        ItemData.city.is_(None),
                        ItemData.city == "",
                    )
                )
                .yield_per(100000)
            )

            buffer = StringIO()
            writer = csv.writer(buffer)

            # Header
            writer.writerow([c.name for c in ItemData.__table__.columns])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

            count = 0
            for row in query:
                writer.writerow(
                    [getattr(row, c.name) for c in ItemData.__table__.columns]
                )
                count += 1

                if count % 100000 == 0:
                    yield buffer.getvalue()
                    buffer.seek(0)
                    buffer.truncate(0)

            if buffer.tell() > 0:
                yield buffer.getvalue()

        finally:
            db.session.remove()

    headers = {
        "Content-Disposition": "attachment; filename=incomplete_items.csv"
    }

    return Response(
        stream_with_context(generate()),
        mimetype="text/csv",
        headers=headers,
    )
