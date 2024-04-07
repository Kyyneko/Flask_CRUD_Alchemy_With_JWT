from app import app, db
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import get_jwt
from app.models.DataDokumen import DataDokumen
from app.models.BlacklistToken import BlacklistToken

# Fungsi untuk memeriksa apakah token sudah logout
def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    return BlacklistToken.query.filter_by(token=jti).first() is not None

# ---------------------------------- UNTUK CREATE DATA di Table data_dokumen --------------------------------- #
@app.route("/data-dokumen", methods=["POST", "GET"])
@jwt_required()  # Endpoint ini memerlukan autentikasi JWT
def data_dokumens():
    current_user_id = get_jwt_identity()  # Mendapatkan identitas pengguna dari token JWT

    # Periksa apakah token yang digunakan sudah logout
    if current_user_id:
        decoded_token = get_jwt()
        if is_token_revoked(decoded_token):
            return jsonify({"message": "Token JWT sudah logout"}), 401

    if request.method == "POST":
        id = request.json["id"]
        nip = request.json["nip"]
        type_dokumen = request.json["type_dokumen"]
        nama_dokumen = request.json["nama_dokumen"]
        nama_file = request.json["nama_file"]

        if type_dokumen != "file" and type_dokumen != "url":
            return jsonify({"message": "Tipe dokumen harus file atau url"})

        new_datadokumen = DataDokumen(id=id, nip=nip, type_dokumen=type_dokumen, nama_dokumen=nama_dokumen, nama_file=nama_file)
        db.session.add(new_datadokumen)
        db.session.commit()

        return jsonify({"message": "Data Dokumen berhasil ditambahkan"})
    
    if request.method == "GET":
        datadokumen = DataDokumen.query.all()
        print(datadokumen)
        datadokumen_list = []
        for dokumen in datadokumen:
            datadokumen_list.append({
                "id": dokumen.id,
                "nip": dokumen.nip,
                "type_dokumen": dokumen.type_dokumen,
                "nama_dokumen": dokumen.nama_dokumen,
                "nama_file": dokumen.nama_file,
            })
        return jsonify(datadokumen_list)
    

# ---------------------------------- UNTUK UPDATE, DELETE, DAN READ DATA di Table data_dokumen --------------------------------- #
@app.route("/data-dokumen/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()  # Endpoint ini memerlukan autentikasi JWT
def data_dokumen(id):
    current_user_id = get_jwt_identity()  # Mendapatkan identitas pengguna dari token JWT

    # Periksa apakah token yang digunakan sudah logout
    if current_user_id:
        decoded_token = get_jwt()
        if is_token_revoked(decoded_token):
            return jsonify({"message": "Token JWT sudah logout"}), 401

    datadokumen = DataDokumen.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
                "id": datadokumen.id,
                "nip": datadokumen.nip,
                "type_dokumen": datadokumen.type_dokumen,
                "nama_dokumen": datadokumen.nama_dokumen,
                "nama_file": datadokumen.nama_file,
        })
    
    if request.method == "PUT":
        datadokumen.id = request.json["id"]
        datadokumen.nip = request.json["nip"]
        datadokumen.type_dokumen = request.json["type_dokumen"]
        datadokumen.nama_dokumen = request.json["nama_dokumen"]
        datadokumen.nama_file = request.json["nama_file"]

        if datadokumen.type_dokumen != "file" and datadokumen.type_dokumen != "url":
            return jsonify({"message": "Tipe dokumen harus file atau url"})

        db.session.commit()
        return jsonify({"message": "Data Dokumen berhasil diperbarui"})
    
    if request.method == "DELETE":
        db.session.delete(datadokumen)
        db.session.commit()
        return jsonify({"message": "Data Dokumen berhasil dihapus"})
