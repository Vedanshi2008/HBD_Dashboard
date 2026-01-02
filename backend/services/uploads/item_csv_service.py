# backend/services/uploads/item_csv_service.py

from flask import jsonify
import pandas as pd
from io import StringIO
import numpy as np
import traceback
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from model.item_csv_model import ItemData


def upload_item_csv(request):
    try:
        # -----------------------------
        # File validation
        # -----------------------------
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if not file or file.filename.strip() == "":
            return jsonify({"error": "Empty file name"}), 400

        # -----------------------------
        # Read CSV
        # -----------------------------
        contents = file.read().decode("utf-8", errors="ignore")
        df = pd.read_csv(StringIO(contents))

        if df.empty:
            return jsonify({"error": "CSV file is empty"}), 400

        # Normalize NaN
        df = df.replace({np.nan: None, "nan": None, "NaN": None})

        # Convert numeric fields safely
        numeric_fields = [
            "ratings", "avg_spent", "cost_for_two",
            "pincode", "latitude", "longitude",
            "price", "quantity"
        ]

        for col in numeric_fields:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        def safe_str(val):
            if val is None:
                return None
            val = str(val).strip()
            return None if val.lower() in {"nan", "null", "none", ""} else val

        inserted = 0
        skipped = 0
        errors = []

        # -----------------------------
        # Insert rows
        # -----------------------------
        for index, row in df.iterrows():
            try:
                name = safe_str(row.get("name"))
                if not name:
                    skipped += 1
                    errors.append({
                        "row": index + 2,
                        "reason": "name is required"
                    })
                    continue

                record = ItemData(
                    name=name,
                    description=safe_str(row.get("description")),
                    category=safe_str(row.get("category")),
                    sub_category=safe_str(row.get("sub_category")),
                    city=safe_str(row.get("city")),
                    area=safe_str(row.get("area")),
                    address=safe_str(row.get("address")),
                    phone_no_1=safe_str(row.get("phone_no_1")),
                    phone_no_2=safe_str(row.get("phone_no_2")),
                    phone_no_3=safe_str(row.get("phone_no_3")),
                    whatsapp_no=safe_str(row.get("whatsapp_no")),
                    virtual_phone_no=safe_str(row.get("virtual_phone_no")),
                    email=safe_str(row.get("email")),
                    facebook_url=safe_str(row.get("facebook_url")),
                    linkedin_url=safe_str(row.get("linkedin_url")),
                    twitter_url=safe_str(row.get("twitter_url")),
                    source=safe_str(row.get("source")),
                    state=safe_str(row.get("state")),
                    country=safe_str(row.get("country")),
                    reviews=safe_str(row.get("reviews")),
                    ratings=row.get("ratings"),
                    avg_spent=row.get("avg_spent"),
                    cost_for_two=row.get("cost_for_two"),
                    pincode=row.get("pincode"),
                    latitude=row.get("latitude"),
                    longitude=row.get("longitude"),
                    price=row.get("price"),
                    quantity=row.get("quantity"),
                )

                db.session.add(record)
                inserted += 1

            except Exception as row_error:
                skipped += 1
                errors.append({
                    "row": index + 2,
                    "reason": str(row_error)
                })

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Item CSV processed successfully",
            "inserted_rows": inserted,
            "skipped_rows": skipped,
            "sample_errors": errors[:10]
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({
            "error": "Unexpected error occurred",
            "details": str(e)
        }), 500
