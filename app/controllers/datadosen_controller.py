from app import app, db
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import get_jwt
from app.models.DataDosen import DataDosen
from app.models.BlacklistToken import BlacklistToken

def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    return BlacklistToken.query.filter_by(token=jti).first() is not None


# ---------------------------------- UNTUK CREATE DATA di Table data_dosen --------------------------------- #
@app.route("/data-dosen", methods=["POST", "GET"])
@jwt_required()  # Endpoint ini memerlukan autentikasi JWT
def data_dosens():
    current_user_id = get_jwt_identity()  # Mendapatkan identitas pengguna dari token JWT
    
     # Periksa apakah token yang digunakan sudah logout
    if current_user_id:
        decoded_token = get_jwt()
        if is_token_revoked(decoded_token):
            return jsonify({"message": "Token JWT sudah logout"}), 401
    
    if request.method == "POST":
        nip = request.json["nip"]
        nama_lengkap = request.json["nama_lengkap"]
        prodi_id = request.json["prodi_id"]

        new_datadosen = DataDosen(nip=nip, nama_lengkap=nama_lengkap, prodi_id=prodi_id)
        db.session.add(new_datadosen)
        db.session.commit()

        return jsonify({"message": "Data Dosen berhasil ditambahkan"})
    
    if request.method == "GET":
        datadosen = DataDosen.query.all()
        datadosen_list = []
        for dosen in datadosen:
            datadosen_list.append({
                "nip": dosen.nip,
                "nama_lengkap": dosen.nama_lengkap,
                "prodi_id": dosen.prodi_id
            })
        return jsonify(datadosen_list)

# ---------------------------------- UNTUK UPDATE, DELETE, DAN READ DATA di Table data_dosen --------------------------------- #
@app.route("/data-dosen/<nip>", methods=["GET", "PUT", "DELETE"])
@jwt_required()  # Endpoint ini memerlukan autentikasi JWT
def data_dosen(nip):
    current_user_id = get_jwt_identity()  # Mendapatkan identitas pengguna dari token JWT
    
     # Periksa apakah token yang digunakan sudah logout
    if current_user_id:
        decoded_token = get_jwt()
        if is_token_revoked(decoded_token):
            return jsonify({"message": "Token JWT sudah logout"}), 401
    
    datadosen = DataDosen.query.get_or_404(nip)

    if request.method == "GET":
        return jsonify({
            "nip": datadosen.nip,
            "nama_lengkap": datadosen.nama_lengkap,
            "prodi_id": datadosen.prodi_id
        })
    
    if request.method == "PUT":
        datadosen.nip = request.json["nip"]
        datadosen.nama_lengkap = request.json["nama_lengkap"]
        datadosen.prodi_id = request.json["prodi_id"]
        db.session.commit()
        return jsonify({"message": "Data Dosen berhasil diperbarui"})
    
    if request.method == "DELETE":
        db.session.delete(datadosen)
        db.session.commit()
        return jsonify({"message": "Data Dosen berhasil dihapus"})
