from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

# ユーザモデル
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)  # 一意の識別子
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'
    
    def check_password(self, password):
        return check_password_hash(self.password, password)