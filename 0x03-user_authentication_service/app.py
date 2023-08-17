#!/usr/bin/env python3
"""Flask App"""
from flask import Flask, jsonify


app = Flask(__name__)


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
        Auth.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ = '__main__':
    app.run(host='0.0.0.0', port=5000)
