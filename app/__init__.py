import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Tambahkan ini

import secrets

app = Flask(__name__)

# Generate a secure random key
secret_key = secrets.token_urlsafe(32)
app.config['SECRET_KEY'] = "71a16ebb97764a9f84b013c71c8823c3"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/db_repositori"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inisialisasi SQacLAlchemy
db = SQLAlchemy(app)

# Inisialisasi Flask-Migrate
migrate = Migrate(app, db)  # Tambahkan ini

# Inisialisasi Flask-JWT-Extended
jwt = JWTManager(app)

# Impor dan daftarkan rute dari controller
from app.auth import login, register, logout
from app.controllers import datadosen_controller, dataprodi_controller, datadokumen_controller
