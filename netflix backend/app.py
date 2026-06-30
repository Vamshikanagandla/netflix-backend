from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import get_database_url
import os

# Create Flask app
app = Flask(__name__)

# Allow React to call this API
CORS(app, origins='*')

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret')

db = SQLAlchemy(app)

# Import and register routes
from routes.auth import auth_bp
from routes.content import content_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(content_bp, url_prefix='/api/content')

# Health check — ALB pings this every 30 seconds
@app.route('/health')
def health():
    return {'status': 'healthy', 'server': 'Python Flask'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)