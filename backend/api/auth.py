# backend/api/auth.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

from model.user import User
from extensions import db


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate user and return JWT access token
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=12)
    )

    return jsonify({
        "success": True,
        "access_token": access_token,
        "token_type": "Bearer",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200


# --------------------------------------------------
# CURRENT USER (PROTECTED)
# --------------------------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Return currently authenticated user
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "email": user.email
    }), 200


# --------------------------------------------------
# LOGOUT (OPTIONAL / CLIENT-SIDE TOKEN DROP)
# --------------------------------------------------
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    JWT logout (stateless — handled client-side)
    """
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200
