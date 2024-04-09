from flask import request, jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt
from app import app, db
from app.models.BlacklistToken import BlacklistToken 

# Endpoint untuk logout, memerlukan autentikasi JWT
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # Ambil JTI (JWT ID) dari token yang sedang digunakan
    token = BlacklistToken(token=jti)  # Buat objek BlacklistToken
    db.session.add(token)  # Tambahkan objek BlacklistToken ke dalam sesi basis data
    db.session.commit()  # Komit perubahan ke dalam basis data

    # Hapus JWT dari cookie untuk logout
    response = jsonify({"msg": "Logout berhasil"})
    unset_jwt_cookies(response)
    return response, 200
