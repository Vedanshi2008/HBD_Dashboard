# services/items/duplicate_service.py

import pandas as pd
from database.mysql_connection import get_mysql_connection

def bulk_csv_upload(
    file_paths,
    table_name,
    columns,
    row_mapper,
    update_columns=None,
    batch_size=10_000
):
    if not file_paths:
        raise ValueError("No file paths provided")

    conn = get_mysql_connection()
    cursor = conn.cursor()
    inserted = 0

    update_sql = ""
    if update_columns:
        update_sql = ", ".join(
            f"{c}=VALUES({c})" for c in update_columns
        )

    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"""
        INSERT INTO {table_name} ({",".join(columns)})
        VALUES ({placeholders})
        {f"ON DUPLICATE KEY UPDATE {update_sql}" if update_sql else ""}
    """

    try:
        for file in file_paths:
            for chunk in pd.read_csv(file, chunksize=batch_size):
                rows = [row_mapper(row) for row in chunk.itertuples(index=False)]
                cursor.executemany(insert_sql, rows)
                conn.commit()
                inserted += len(rows)

        return inserted

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
