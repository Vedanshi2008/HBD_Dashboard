# backend/services/items/duplicate_service.py

from flask import request, jsonify
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from model.item_csv_model import ItemData


# --------------------------------------------------
# Serializer
# --------------------------------------------------
def _serialize(item):
    return {
        column.name: getattr(item, column.name)
        for column in item.__table__.columns
    }


# --------------------------------------------------
# FETCH DUPLICATE ITEMS (PAGINATED)
# --------------------------------------------------
def get_duplicate_items():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit

        # -----------------------------
        # Step 1: Identify duplicate groups
        # -----------------------------
        duplicate_groups = (
            db.session.query(
                ItemData.name,
                ItemData.category,
                ItemData.sub_category,
                ItemData.email,
                ItemData.city,
                ItemData.area,
                ItemData.address,
                func.count(ItemData.id).label("count"),
            )
            .group_by(
                ItemData.name,
                ItemData.category,
                ItemData.sub_category,
                ItemData.email,
                ItemData.city,
                ItemData.area,
                ItemData.address,
            )
            .having(func.count(ItemData.id) > 1)
            .subquery()
        )

        # -----------------------------
        # Step 2: Join to get all duplicates
        # -----------------------------
        duplicates_query = (
            db.session.query(ItemData)
            .join(
                duplicate_groups,
                and_(
                    ItemData.name == duplicate_groups.c.name,
                    ItemData.category == duplicate_groups.c.category,
                    ItemData.sub_category == duplicate_groups.c.sub_category,
                    ItemData.email == duplicate_groups.c.email,
                    ItemData.city == duplicate_groups.c.city,
                    ItemData.area == duplicate_groups.c.area,
                    ItemData.address == duplicate_groups.c.address,
                ),
            )
            .order_by(ItemData.id)
        )

        # -----------------------------
        # Step 3: Remove first occurrence per group
        # -----------------------------
        seen = set()
        duplicates = []

        for item in duplicates_query.offset(offset).limit(limit).all():
            key = (
                item.name,
                item.category,
                item.sub_category,
                item.email,
                item.city,
                item.area,
                item.address,
            )
            if key in seen:
                duplicates.append(_serialize(item))
            else:
                seen.add(key)

        # -----------------------------
        # Step 4: Count total duplicates
        # -----------------------------
        total_duplicates = (
            db.session.query(func.sum(duplicate_groups.c.count - 1)).scalar()
        ) or 0

        return jsonify({
            "success": True,
            "page": page,
            "limit": limit,
            "total": total_duplicates,
            "total_pages": (total_duplicates + limit - 1) // limit,
            "items": duplicates,
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# DELETE SELECTED DUPLICATES
# --------------------------------------------------
def delete_duplicate_items():
    try:
        data = request.get_json(silent=True) or {}
        ids_to_delete = data.get("ids", [])

        if not ids_to_delete:
            return jsonify({
                "error": "No IDs provided"
            }), 400

        deleted_count = (
            db.session.query(ItemData)
            .filter(ItemData.id.in_(ids_to_delete))
            .delete(synchronize_session=False)
        )

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Selected duplicates deleted successfully",
            "deleted_count": deleted_count,
            "deleted_ids": ids_to_delete,
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
