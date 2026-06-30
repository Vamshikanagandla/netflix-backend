from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

# POST /api/auth/register
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        from app import db
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Check if user already exists
        result = db.session.execute(
            db.text('SELECT id FROM users WHERE email = :email'),
            {'email': email}
        ).fetchone()

        if result:
            return jsonify({'error': 'Email already registered'}), 400

        # Hash the password
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        # Insert new user
        db.session.execute(
            db.text('INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :hash)'),
            {'name': name, 'email': email, 'hash': password_hash}
        )
        db.session.commit()

        return jsonify({'message': 'Registered successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# POST /api/auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        from app import db
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Find user
        user = db.session.execute(
            db.text('SELECT * FROM users WHERE email = :email'),
            {'email': email}
        ).fetchone()

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Check password
        valid = bcrypt.checkpw(
            password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        )
        if not valid:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create token
        token = jwt.encode({
            'userId': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, os.environ.get('SECRET_KEY', 'secret'), algorithm='HS256')

        return jsonify({
            'token': token,
            'user': {'id': user.id, 'name': user.name}
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500