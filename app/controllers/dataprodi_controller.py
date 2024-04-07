from app import app, db
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.BlacklistToken import BlacklistToken
from app.models.DataProdi import DataProdi

# Fungsi untuk memeriksa apakah token sudah logout
def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    return BlacklistToken.query.filter_by(token=jti).first() is not None

@app.route("/data-prodi", methods=["POST", "GET"])
@jwt_required()  # Endpoint ini memerlukan autentikasi JWT
def data_prodis():
    current_user_id = get_jwt_identity()  # Mendapatkan identitas pengguna dari token JWT
    
     # Periksa apakah token yang digunakan sudah logout
    if current_user_id:
        decoded_token = get_jwt()
        if is_token_revoked(decoded_token):
            return jsonify({"message": "Token JWT sudah logout"}), 401
    
    if request.method == "POST":
        kode_prodi = request.json["kode_prodi"]
        nama_prodi = request.json["nama_prodi"]

        new_dataprodi = DataProdi(kode_prodi=kode_prodi, nama_prodi=nama_prodi)
        db.session.add(new_dataprodi)
        db.session.commit()

        return jsonify({"message": "Data Prodi berhasil ditambahkan"})
    
    if request.method == "GET":
        dataprodi = DataProdi.query.all()
        dataprodi_list = []
        for prodi in dataprodi:
            dataprodi_list.append({
                "id": prodi.id,
                "kode_prodi": prodi.kode_prodi,
                "nama_prodi": prodi.nama_prodi
            })
        return jsonify(dataprodi_list)
    
@app.route("/data-prodi/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()  # Endpoint ini memerlukan autentikasi JWT
def data_prodi(id):
    current_user_id = get_jwt_identity()  # Mendapatkan identitas pengguna dari token JWT
    
    # Periksa apakah token yang digunakan sudah logout
    if current_user_id:
        decoded_token = get_jwt()
        if is_token_revoked(decoded_token):
            return jsonify({"message": "Token JWT sudah logout"}), 401
    
    dataprodi = DataProdi.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
            "id": dataprodi.id,
            "kode_prodi": dataprodi.kode_prodi,
            "nama_prodi": dataprodi.nama_prodi
        })
    
    if request.method == "PUT":
        dataprodi.kode_prodi = request.json["kode_prodi"]
        dataprodi.nama_prodi = request.json["nama_prodi"]
        db.session.commit()
        return jsonify({"message": "Data Prodi berhasil diperbarui"})
    
    if request.method == "DELETE":
        db.session.delete(dataprodi)
        db.session.commit()
        return jsonify({"message": "Data Prodi berhasil dihapus"})
