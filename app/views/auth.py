from flask import Blueprint, jsonify, render_template, url_for, request, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import check_password_hash

from app.models.user import User

# Blueprintの定義
auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_submit():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))

        response = make_response(jsonify({
            'login': True,
            'redirect_url': url_for('web.aggregated_summary')
        }))
        # JWTクッキーの設定
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({'msg': 'Invalid username or password'}), 401
