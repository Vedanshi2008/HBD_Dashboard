# backend/app.py

from flask import Flask, jsonify
from dotenv import load_dotenv
from sqlalchemy import inspect

from config import Config
from extensions import db, jwt, cors

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()


# --------------------------------------------------
# Application Factory
# --------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    initialize_extensions(app)
    register_models(app)
    register_blueprints(app)
    register_health_check(app)

    return app


# --------------------------------------------------
# Extensions Initialization
# --------------------------------------------------
def initialize_extensions(app: Flask) -> None:
    cors(app)
    db.init_app(app)
    jwt.init_app(app)


# --------------------------------------------------
# Database Model Registration & Verification
# --------------------------------------------------
def register_models(app: Flask) -> None:
    with app.app_context():
        # Import models so SQLAlchemy knows them
        from model.user import User
        from model.amazon_product_model import AmazonProduct
        from model.googlemap_data import GooglemapData
        from model.item_csv_model import ItemData
        from model.listing_master import ListingMaster

        db.create_all()

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print("Database connection successful.")
        print("Tables found:", tables)


# --------------------------------------------------
# Blueprint Registration (ONE PLACE ONLY)
# --------------------------------------------------
def register_blueprints(app: Flask) -> None:
    """
    Register all API blueprints.
    Do NOT import individual blueprints here.
    """

    from api import register_api
    register_api(app)

    print("All blueprints registered successfully.")


# --------------------------------------------------
# Health Check
# --------------------------------------------------
def register_health_check(app: Flask) -> None:
    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "OK",
            "service": "HBD Backend",
            "environment": app.config.get("ENV", "development")
        })


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
