# backend/services/product/product_csv_service.py

import json
import traceback
from io import StringIO

import chardet
import numpy as np
import pandas as pd
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from model.amazon_product_model import AmazonProduct


def handle_product_csv_upload(request):
    try:
        # -----------------------------
        # File validation
        # -----------------------------
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if not file.filename.strip():
            return jsonify({"error": "Empty file name"}), 400

        # -----------------------------
        # Detect encoding & read CSV
        # -----------------------------
        raw_data = file.read()
        detected = chardet.detect(raw_data)
        encoding = detected.get("encoding") or "utf-8"

        try:
            csv_data = StringIO(raw_data.decode(encoding, errors="ignore"))
            df = pd.read_csv(csv_data)
        except Exception:
            return jsonify({
                "error": "Failed to read CSV file. Check encoding or format."
            }), 400

        # -----------------------------
        # Normalize NaN / None values
        # -----------------------------
        df = df.replace({np.nan: None, "nan": None, "NaN": None})

        def safe_str(value):
            if value is None:
                return None
            value = str(value).strip()
            if value.lower() in {"nan", "none", "null", ""}:
                return None
            return value

        inserted_count = 0
        skipped_count = 0

        # -----------------------------
        # Insert rows
        # -----------------------------
        for _, row in df.iterrows():
            try:
                product = AmazonProduct(
                    asin=safe_str(row.get("ASIN")),
                    product_name=safe_str(row.get("Product_name")),
                    price=safe_str(row.get("price")),
                    rating=float(row.get("rating"))
                    if str(row.get("rating")).replace(".", "", 1).isdigit()
                    else None,
                    number_of_ratings=int(row.get("Number_of_ratings"))
                    if str(row.get("Number_of_ratings")).isdigit()
                    else None,
                    brand=safe_str(row.get("Brand")),
                    seller=safe_str(row.get("Seller")),
                    category=safe_str(row.get("category")),
                    subcategory=safe_str(row.get("subcategory")),
                    sub_sub_category=safe_str(row.get("sub_sub_category")),
                    category_sub_sub_sub=safe_str(row.get("category_sub_sub_sub")),
                    colour=safe_str(row.get("colour")),
                    size_options=safe_str(row.get("size_options")),
                    description=safe_str(row.get("description")),
                    link=safe_str(row.get("link")),
                    image_urls=safe_str(row.get("Image_URLs")),
                    about_the_items_bullet=safe_str(
                        row.get("About_the_items_bullet")
                    ),
                    product_details=(
                        json.loads(row.get("Product_details"))
                        if isinstance(row.get("Product_details"), str)
                        and row.get("Product_details").strip().startswith("{")
                        else {}
                    ),
                    additional_details=(
                        json.loads(row.get("Additional_Details"))
                        if isinstance(row.get("Additional_Details"), str)
                        and row.get("Additional_Details").strip().startswith("{")
                        else {}
                    ),
                    manufacturer_name=safe_str(
                        row.get("Manufacturer_Name")
                    ),
                )

                db.session.add(product)
                inserted_count += 1

            except Exception as row_error:
                skipped_count += 1
                print("Row skipped:", row_error)
                continue

        # -----------------------------
        # Commit once
        # -----------------------------
        db.session.commit()

        return jsonify({
            "message": "Amazon product CSV uploaded successfully",
            "inserted_rows": inserted_count,
            "skipped_rows": skipped_count
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
        return jsonify({"error": str(e)}), 500
