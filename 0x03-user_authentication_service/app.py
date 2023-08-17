#!/usr/bin/env python3
"""Flask App"""
from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ Print a object"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """endpoint to register user"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        AUTH.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Login endpint"""
    email = request.form.get('email', '')
    pwd = request.form.get('password', '')
    check_login = AUTH.valid_login(email, pwd)
    if not check_login:
        abort(404)
    res = make_response(json({"email": email, "message": "logged in"}))
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """destroy session"""
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """find user profile"""
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    return jsonify({"email": user}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route() -> str:
    """Reset password"""
    email = request.form.get("email", '')
    is_user = AUTH.create_session(email)
    if not is_user:
        abort(403)
    tok = AUTH.get_reset_password_token(email)
    return jsonify({'email': email, 'reset_taken': tok})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def update_password() -> str:
    """update the password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_pwd = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_pwd)
    except Exception:
        abort(403)
    return jsonify({'email': email, 'message': 'Password updated'}), 200


if __name__ = '__main__':
    app.run(host='0.0.0.0', port=5000)
