from flask import Blueprint, jsonify, request
from sqlalchemy import func
from extensions import db
from model.listing_master import ListingMaster

listing_master_bp = Blueprint('listing_master_bp', __name__)

@listing_master_bp.route('/listing-master', methods=['GET'])
def get_aggregated_listings():
    try:
        # SQL Query: Select Name, Category, Count(*), and list of Sources
        # Group by Name and Category to find duplicates/branches
        query = db.session.query(
            ListingMaster.business_name,
            ListingMaster.category,
            func.count(ListingMaster.id).label('total_count'),
            func.group_concat(ListingMaster.source.distinct()).label('sources')
        ).group_by(
            ListingMaster.business_name, 
            ListingMaster.category
        ).order_by(func.count(ListingMaster.id).desc()) # Show highest counts first

        # Search Filters (Optional)
        search = request.args.get('search')
        if search:
            query = query.filter(ListingMaster.business_name.ilike(f"%{search}%"))

        results = query.limit(100).all()

        # Format the data for Frontend
        data = []
        for name, category, count, sources in results:
            data.append({
                "business_name": name,
                "category": category,
                "total_listings": count,
                "sources": sources  # e.g., "JustDial,GoogleMap"
            })
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500