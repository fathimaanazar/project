import os
import logging
from flask import Flask
from extensions import db   #added
'''from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase'''
from werkzeug.middleware.proxy_fix import ProxyFix




# Configure logging
logging.basicConfig(level=logging.DEBUG)

'''class Base(DeclarativeBase):
    pass

#db = SQLAlchemy(model_class=Base)'''

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///blood_donation.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

from flask_moment import Moment

moment = Moment(app)


# Initialize the app with the extension
db.init_app(app)

from utils import can_donate  # Import it first

app.jinja_env.globals['can_donate'] = can_donate  # Register it globally

from utils import calculate_age  # ✅ Import the function

app.jinja_env.globals['calculate_age'] = calculate_age  # ✅ Register as template global

from utils import format_urgency_level  # Import the function

app.jinja_env.globals['format_urgency_level'] = format_urgency_level  # Register as template global


with app.app_context():
    # Import models to create tables
    import models
    db.create_all()

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
