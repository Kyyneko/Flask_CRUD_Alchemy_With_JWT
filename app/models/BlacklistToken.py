from app import db

class BlacklistToken(db.Model):
    __tablename__ = 'blacklisttoken'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
