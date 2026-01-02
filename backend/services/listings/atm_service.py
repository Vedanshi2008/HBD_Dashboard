# services/items/duplicate_service.py

from utils.safe_get import safe_get
from services.listings.base_csv_uploader import bulk_csv_upload

def upload_atm_data(file_paths):
    return bulk_csv_upload(
        file_paths,
        table_name="atm",
        columns=["bank","address","city","state","country","category"],
        update_columns=["city","state","country","category"],
        row_mapper=lambda r: (
            safe_get(r, "Bank"),
            safe_get(r, "Address"),
            safe_get(r, "City"),
            safe_get(r, "State"),
            safe_get(r, "Country"),
            safe_get(r, "Category"),
        )
    )
