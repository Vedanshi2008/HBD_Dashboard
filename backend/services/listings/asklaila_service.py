# servies/listing/asklaila_service.py

from utils.safe_get import safe_get
from utils.clean_data_decimal import clean_data_decimal
from services.listings.base_csv_uploader import bulk_csv_upload

def upload_asklaila_data(file_paths):
    return bulk_csv_upload(
        file_paths=file_paths,
        table_name="asklaila",
        columns=[
            "name","number1","number2","category","subcategory",
            "email","url","ratings","address","pincode",
            "area","city","state","country"
        ],
        update_columns=[
            "number1","number2","category","subcategory","email",
            "url","ratings","pincode","area","city","state","country"
        ],
        row_mapper=lambda r: (
            safe_get(r, "name"),
            clean_data_decimal(safe_get(r, "phone_1")),
            clean_data_decimal(safe_get(r, "phone_2")),
            safe_get(r, "category"),
            safe_get(r, "sub_category"),
            safe_get(r, "email"),
            safe_get(r, "url"),
            safe_get(r, "ratings"),
            safe_get(r, "address"),
            safe_get(r, "pincode"),
            safe_get(r, "area"),
            safe_get(r, "city"),
            safe_get(r, "state"),
            safe_get(r, "country"),
        )
    )
