# backend/api/__init__.py

"""
Central API registration module.
ALL API blueprints are registered here.
"""

def register_api(app):
    # -------------------------
    # AUTH
    # -------------------------
    from api.auth import auth_bp
    app.register_blueprint(auth_bp)

    # -------------------------
    # LISTINGS
    # -------------------------
    from api.listing import listing_bp
    app.register_blueprint(listing_bp)

    # -------------------------
    # PRODUCTS
    # -------------------------
    from api.product import product_bp
    app.register_blueprint(product_bp)

    # -------------------------
    # ITEMS
    # -------------------------
    from api.items import items_bp
    app.register_blueprint(items_bp)

    # -------------------------
    # UPLOADS
    # -------------------------
    from api.uploads import uploads_bp
    app.register_blueprint(uploads_bp)
