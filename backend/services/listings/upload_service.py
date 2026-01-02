# backend/services/listing/upload_service.py

from flask import jsonify
from werkzeug.utils import secure_filename
from utils.storage import get_upload_base_dir

# Import all tasks
from tasks.listings_task.upload_atm_task import process_atm_task
from tasks.listings_task.upload_bank_task import process_bank_task
from tasks.listings_task.upload_asklaila_task import process_asklaila_task
from tasks.listings_task.upload_college_dunia_task import process_college_dunia_task
from tasks.listings_task.upload_freelisting_task import process_freelisting_task
from tasks.listings_task.upload_google_map_task import process_google_map_task
from tasks.listings_task.upload_google_map_scrape_task import process_google_map_scrape_task
from tasks.listings_task.upload_heyplaces_task import process_heyplaces_task
from tasks.listings_task.upload_justdial_task import process_justdial_task
from tasks.listings_task.upload_magicpin_task import process_magicpin_task
from tasks.listings_task.upload_nearbuy_task import process_nearbuy_task
from tasks.listings_task.upload_pinda_task import process_pinda_task
from tasks.listings_task.upload_post_office_task import process_post_office_task
from tasks.listings_task.upload_schoolgis_task import process_schoolgis_task
from tasks.listings_task.upload_shiksha_task import process_shiksha_task
from tasks.listings_task.upload_yellow_pages_task import process_yellow_pages_task


TASK_MAP = {
    "atm": process_atm_task,
    "bank": process_bank_task,
    "asklaila": process_asklaila_task,
    "college-dunia": process_college_dunia_task,
    "freelisting": process_freelisting_task,
    "google-map": process_google_map_task,
    "google-map-scrape": process_google_map_scrape_task,
    "heyplaces": process_heyplaces_task,
    "justdial": process_justdial_task,
    "magicpin": process_magicpin_task,
    "nearbuy": process_nearbuy_task,
    "pinda": process_pinda_task,
    "post-office": process_post_office_task,
    "schoolgis": process_schoolgis_task,
    "shiksha": process_shiksha_task,
    "yellow-pages": process_yellow_pages_task,
}


def handle_listing_upload(source, request):
    if source not in TASK_MAP:
        return jsonify({"error": f"Unknown source: {source}"}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files provided"}), 400

    upload_dir = get_upload_base_dir() / source.replace("-", "_")
    upload_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for f in files:
        filename = secure_filename(f.filename)
        filepath = upload_dir / filename
        f.save(filepath)
        paths.append(str(filepath))

    task = TASK_MAP[source].delay(paths)

    return jsonify({
        "status": "files_accepted",
        "source": source,
        "task_id": task.id
    }), 202
