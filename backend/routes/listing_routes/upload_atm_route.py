from flask import Blueprint, request, jsonify
from extensions import db
from model.atm import Atm

atm_bp = Blueprint('atm_bp', __name__)

@atm_bp.route('/fetch-data', methods=['GET'])
def fetch_atm_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city_filter = request.args.get('city', '')

        query = Atm.query

        if search:
            query = query.filter(Atm.name.ilike(f"%{search}%"))
        
        if city_filter:
            query = query.filter(Atm.city.ilike(f"%{city_filter}%"))

        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500