#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Returns a response"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Creates a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        new_user = AUTH.register_user(email=email, password=password)
        return jsonify(
            {"email": f"{new_user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login():
    """Creates a new session for the user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id is None:
            abort(401)
        else:
            resp = jsonify({"email": f"{email}", "message": "logged in"})
            resp.set_cookie("session_id", session_id, max_age=3600)
            return resp
    else:
        abort(401)


@app.route('/sessions', methods=["DELETE"])
def logout():
    """Deletes a users session id"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    else:
        abort(403)


@app.route('/profile', methods=["GET"])
def profile():
    """Returns a users profile based on session_id"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=["POST"])
def get_reset_password_token():
    """retreives the reset_token from the user using email"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email=email)
        return jsonify(
            {"email": f"{email}", "reset_token": f"{reset_token}"}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=["PUT"])
def update_password():
    """Updates a users password"""
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": f"{email}", "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
