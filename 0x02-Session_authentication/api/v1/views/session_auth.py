#!/usr/bin/env python3
""" Module of Sessin authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_session():
    """Creates a cookie for a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    elif password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        user_inst = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 400
    if len(user_inst) == 0:
        return jsonify({"error": "no user found for this email"}), 400
    ob_id = user_inst[0]
    user = User.get(ob_id.id)
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        cookie_name = os.getenv('SESSION_NAME')
        resp = jsonify(user.to_json())
        resp.set_cookie(cookie_name, session_id, max_age=3600)
        return resp


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Deletes the users session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
