from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

# Blueprintの定義
web_bp = Blueprint(
    'web',
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

#@web_bp.route('/')
#def index():
#    return render_template('index.html')

@web_bp.route('/summary', methods=['GET'])
@jwt_required()
def aggregated_summary():
    return render_template('aggregated_summary.html')

@web_bp.route('/upload', methods=['GET'])
@jwt_required()
def upload_budget():
    return render_template('upload_budget.html')
