# backend/services/uploads/generic_csv_service.py

from flask import jsonify
import pandas as pd
import chardet
import os
from sqlalchemy import (
    create_engine, Table, Column,
    Integer, Text, MetaData, inspect
)
from sqlalchemy.exc import SQLAlchemyError


def upload_generic_csv(request):
    try:
        # -----------------------------
        # File validation
        # -----------------------------
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename.strip() == "":
            return jsonify({"error": "Empty filename"}), 400

        # Table name from filename
        table_name = (
            os.path.splitext(file.filename)[0]
            .strip()
            .replace(" ", "_")
            .replace("-", "_")
            .lower()
        )

        # -----------------------------
        # Detect encoding
        # -----------------------------
        rawdata = file.read()
        encoding = chardet.detect(rawdata).get("encoding") or "utf-8"
        file.seek(0)

        # -----------------------------
        # Read CSV
        # -----------------------------
        try:
            df = pd.read_csv(file, encoding=encoding, on_bad_lines="skip")
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin1", on_bad_lines="skip")

        if df.empty:
            return jsonify({"error": "CSV is empty or invalid"}), 400

        # -----------------------------
        # Database engine (same DB)
        # -----------------------------
        engine = create_engine(
            request.app.config["SQLALCHEMY_DATABASE_URI"]
        )
        metadata = MetaData()
        inspector = inspect(engine)

        if inspector.has_table(table_name):
            return jsonify({
                "message": f"Table '{table_name}' already exists",
                "table": table_name,
                "rows_inserted": 0
            }), 200

        # -----------------------------
        # Prepare table
        # -----------------------------
        df = df.fillna("").astype(str)

        columns = [
            Column(
                str(col).strip()
                .replace(" ", "_")
                .replace("-", "_")
                .lower(),
                Text()
            )
            for col in df.columns
        ]

        table = Table(
            table_name,
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            *columns
        )

        metadata.create_all(engine)

        # -----------------------------
        # Insert data in chunks
        # -----------------------------
        chunksize = 5000
        rows_inserted = 0

        for start in range(0, len(df), chunksize):
            df.iloc[start:start + chunksize].to_sql(
                table_name,
                engine,
                if_exists="append",
                index=False
            )
            rows_inserted += len(df.iloc[start:start + chunksize])

        return jsonify({
            "success": True,
            "message": f"Table '{table_name}' created successfully",
            "table": table_name,
            "columns": list(df.columns),
            "rows_inserted": rows_inserted
        }), 201

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Unexpected error occurred",
            "details": str(e)
        }), 500
