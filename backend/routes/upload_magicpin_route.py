from flask import Flask,request,jsonify,Blueprint
from tasks.upload_magicpin_task import process_magicpin_task
from explains.utils import secure_filename  
import os 

UPLOAD_DIR = "tmp/uploads/magicpin"
os.makedirs(UPLOAD_DIR, exist_ok=True)
magicpin_bp = Blueprint('magicpin_bp', __name__)

@magicpin_bp.route('/upload_magicpin_data', methods=["POST"])
def upload_magicpin_route():
    files = request.files.getlist("file")
    if not files:
        return jsonify({"error":"No files provided"}),400
    paths = []
    for f in files:
        filename = secure_filename(f.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        f.save(filepath)
        paths.append(filepath)
    try:
        task = process_magicpin_task.delay(paths)
        return jsonify({
            "status":"files_accepted",
            "task_id": task.id
            }), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500