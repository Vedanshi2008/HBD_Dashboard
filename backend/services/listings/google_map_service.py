# backend/services/listing/google_map_service.py

from flask import jsonify
import threading
from sqlalchemy.exc import SQLAlchemyError

from scrapers.google_maps_scraper import run_google_maps_scraper
from model.googlemap_data import GooglemapData
from extensions import db


# --------------------------------------------------
# START GOOGLE MAP SCRAPING
# --------------------------------------------------
def start_google_map_scrape(data: dict):
    """
    Starts Google Maps scraping in background.

    Expected payload:
    {
        "queries": [
            "restaurant, Pune, Maharashtra",
            "hospital, Mumbai, Maharashtra"
        ]
    }
    """
    if not data or "queries" not in data:
        return jsonify({
            "error": "queries field is required"
        }), 400

    search_list = []

    for q in data["queries"]:
        if not isinstance(q, str):
            continue

        parts = [p.strip() for p in q.split(",")]
        if len(parts) != 3:
            continue

        search_list.append({
            "category": parts[0],
            "city": parts[1],
            "state": parts[2],
        })

    if not search_list:
        return jsonify({
            "error": "No valid queries found"
        }), 400

    # Background scraping (no DB session used here)
    threading.Thread(
        target=run_google_maps_scraper,
        args=(search_list,),
        daemon=True
    ).start()

    return jsonify({
        "success": True,
        "message": "Google Maps scraping started",
        "total_queries": len(search_list)
    }), 202


# --------------------------------------------------
# FETCH GOOGLE MAP DATA
# --------------------------------------------------
def fetch_google_map_data():
    """
    Fetch all Google Map records
    """
    try:
        records = db.session.query(GooglemapData).all()

        data = [{
            "id": r.id,
            "name": r.name,
            "address": r.address,
            "website": r.website,
            "phone_number": r.phone_number,
            "reviews_count": r.reviews_count,
            "reviews_average": r.reviews_average,
            "category": r.category,
            "subcategory": r.subcategory,
            "city": r.city,
            "state": r.state,
            "area": r.area,
            "created_at": (
                r.created_at.isoformat()
                if r.created_at else None
            )
        } for r in records]

        return jsonify({
            "count": len(data),
            "data": data
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database error occurred",
            "details": str(e)
        }), 500
