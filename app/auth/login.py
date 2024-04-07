from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.DataDosen import DataDosen  # Pastikan mengimpor model yang sesuai

# Ambil objek Flask app dari modul utama
from app import app

@app.route('/login', methods=['POST'])
def login():
    # Ambil data yang dikirim dalam request
    nama_lengkap = request.json.get('nama_lengkap', None)
    nip = request.json.get('nip', None)

    # Periksa kredensial pengguna
    user = DataDosen.query.filter_by(nama_lengkap=nama_lengkap, nip=nip).first()
    if user:
        # Jika kredensial valid, buat token JWT
        access_token = create_access_token(identity=user.nip)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid nama_lengkap or nip"}), 401
