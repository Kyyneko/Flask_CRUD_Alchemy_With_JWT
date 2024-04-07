from flask import request, jsonify
from app.models.DataDosen import DataDosen  # Pastikan mengimpor model yang sesuai

# Ambil objek Flask app dari modul utama
from app import app, db

@app.route('/register', methods=['POST'])
def register():
    # Ambil data yang dikirim dalam request
    nama_lengkap = request.json.get('nama_lengkap', None)
    nip = request.json.get('nip', None)
    prodi_id = request.json.get('prodi_id', None)

    # Periksa apakah pengguna sudah terdaftar
    existing_user = DataDosen.query.filter_by(nama_lengkap=nama_lengkap, nip=nip).first()
    if existing_user:
        return jsonify({"msg": "Pengguna sudah terdaftar"}), 400

    # Buat pengguna baru
    new_user = DataDosen(nama_lengkap=nama_lengkap, nip=nip, prodi_id=prodi_id)

    # Tambahkan pengguna baru ke database
    db.session.add(new_user)
    db.session.commit()

    # Mengembalikan pesan berhasil tanpa membuat token JWT
    return jsonify({"msg": "Pendaftaran berhasil"}), 200
