# backend/services/product/upload_service.py

from flask import jsonify
from werkzeug.utils import secure_filename
from utils.storage import get_upload_base_dir

from tasks.products_task.upload_amazon_products_task import process_amazon_products_task
from tasks.products_task.upload_big_basket_task import process_big_basket_task
from tasks.products_task.upload_vivo_task import process_vivo_task


TASK_MAP = {
    "amazon": process_amazon_products_task,
    "big-basket": process_big_basket_task,
    "vivo": process_vivo_task,
}


def handle_product_upload(source, request):
    if source not in TASK_MAP:
        return jsonify({"error": f"Unknown product source: {source}"}), 400

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
