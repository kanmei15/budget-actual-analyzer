from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
import openpyxl
from openpyxl.utils import column_index_from_string
from werkzeug.utils import secure_filename

from app import db
from app.models import BudgetProfitAndLoss, ActualProfitAndLoss
from app.logger import get_logger

# ロガー取得
logger = get_logger('upload')

# 各エンドポイントのNamespace
upload_budget_ns = Namespace('upload-budget', description='BNオーダ損益状況（予算）データのアップロード')
upload_actual_ns = Namespace('upload-actual', description='BNオーダ損益状況（実績）データのアップロード')

upload_model = upload_budget_ns.model('UploadModel', {
    'file': fields.String(
        required=True,
        description='アップロードするExcelファイル（FormData形式で送信）',
        example='損益_予算.xlsx'
    )
})

ALLOWED_EXTENSIONS = {'xlsx'}
ALLOWED_MIME_TYPES = {
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}
# 列マッピング
BASE_COLUMN_MAP = {
    'internal_man_hours': 'CL',
    'partner_man_hours': 'CM',
    'bulk_man_hours': 'CN',
    'order_amount': 'CP',
    'recognized_sales': 'CR',
    'recognized_profit': 'CW',
}

COLUMN_SPAN = 13
START_ROW = 4

# ファイル拡張子 + MIMEタイプを検証
def allowed_file(file):
    filename = file.filename
    ext = filename.rsplit('.', 1)[-1].lower()
    return (
        '.' in filename and
        ext in ALLOWED_EXTENSIONS and
        file.mimetype in ALLOWED_MIME_TYPES
    )

# 列のオフセット計算（1月あたり13列ずれていく想定）
def get_column_index(base_col, offset):
    return column_index_from_string(base_col) - 1 + offset * COLUMN_SPAN

# 月ごとのデータ抽出
def extract_month_data(row, month):
    offset = month - 2
    data = {}
    for key, base_col in BASE_COLUMN_MAP.items():
        col_index = get_column_index(base_col, offset)
        data[key] = row[col_index].value
    return data

# 共通のアップロード処理
def handle_upload(sheet, model_class):
    logger.info(f"データ登録開始: model={model_class.__name__}")
    # テーブル初期化
    db.session.query(model_class).delete()

    for row_idx, row in enumerate(sheet.iter_rows(min_row=START_ROW), start=START_ROW):
        try:
            order_code = row[2].value + row[3].value + row[4].value # D+E+F列（オーダーコード）
            order_name = row[5].value # G列（オーダー名）
            deal_status = row[6].value # H列（商談区分）
            customer_code = row[11].value # M列（取引先コード）
            start_dt = row[15].value # Q列（作業開始日）
            end_dt = row[16].value # R列（作業終了日）
            manager_code = row[17].value # S列（マネジャーコード）
            leader_code = row[19].value # U列（リーダコード）

            for month in range(2, 14):  # 2~13（13=翌年1月）
                month_data = extract_month_data(row, month)

                entry = model_class(
                    order_code=order_code,
                    order_name=order_name,
                    deal_status=deal_status,
                    customer_code=customer_code,
                    start_dt=start_dt,
                    end_dt=end_dt,
                    manager_code=manager_code,
                    leader_code=leader_code,
                    month_number=1 if month == 13 else month,
                    internal_man_hours=month_data['internal_man_hours'] or 0,
                    partner_man_hours=month_data['partner_man_hours'] or 0,
                    bulk_man_hours=month_data['bulk_man_hours'] or 0,
                    order_amount=month_data['order_amount'] or 0,
                    recognized_sales=month_data['recognized_sales'] or 0,
                    recognized_profit=month_data['recognized_profit'] or 0
                )
                db.session.add(entry)
        except Exception as e:
            logger.warning(f"{row_idx}行目の処理中にエラー: {e}")

    db.session.commit()
    logger.info(f"データ登録完了: model={model_class.__name__}")

# リソース定義（汎用化）
def create_upload_resource(namespace, model_class):
    @namespace.route('')
    class UploadResource(Resource):
        @namespace.expect(upload_model)
        @namespace.response(200, 'アップロード成功')
        @namespace.response(400, 'ファイルが未指定または形式不正')
        @namespace.response(500, 'サーバーエラー（DBロールバック含む）')
        @namespace.doc(description="Excelファイルをアップロードして、損益データ（予算または実績）を登録します。")
        @jwt_required()
        def post(self):
            file = request.files['file']

            if not file or not allowed_file(file):
                logger.warning(f"不正なファイル形式: {file.filename if file else '未指定'} / MIME: {file.mimetype if file else '不明'}")
                return {'message': 'xlsx形式のファイルのみ許可されています'}, 400

            try:
                filename = secure_filename(file.filename)
                logger.info(f"アップロード開始: model={model_class.__name__}, filename={filename}")

                wb = openpyxl.load_workbook(file, data_only=True)
                sheet = wb.active
                handle_upload(sheet, model_class)

                logger.info(f"アップロード成功: model={model_class.__name__}")
                return {'message': 'アップロード成功'}, 200

            except openpyxl.utils.exceptions.InvalidFileException:
                logger.warning("無効なExcelファイル形式")
                return {'message': '無効なExcelファイルです'}, 400

            except Exception as e:
                db.session.rollback()
                logger.exception("アップロード失敗（ロールバック）")
                return {'message': 'アップロード失敗', 'error': str(e)}, 500

# 各APIのルートを生成
create_upload_resource(upload_budget_ns, BudgetProfitAndLoss)
create_upload_resource(upload_actual_ns, ActualProfitAndLoss)
