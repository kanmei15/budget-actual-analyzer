from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from app.models import DifferenceProfitAndLoss
from app.logger import get_logger

# ロガー取得
logger = get_logger('difference')

difference_ns = Namespace('difference', description='差分損益データ取得')

difference_parser = difference_ns.parser()
difference_parser.add_argument('month_number', type=int, help='月 (1〜12)', location='args')

difference_model = difference_ns.model('DifferenceProfitAndLoss', {
    'id': fields.Integer(description='一意の識別子', example=123),
    'parent_group_key': fields.String(description='集計軸（親）', example='1'),
    'group_by_key': fields.String(description='集計軸', example='〇〇〇会社'),
    'month_number': fields.Integer(description='月 (1〜12)', example=4),
    'diff_order_amount': fields.Integer(description='予実差の受注額', example=1200000),
    'diff_sales': fields.Integer(description='予実差の売上計上額', example=1100000),
    'diff_profit': fields.Integer(description='予実差の利益計上額', example=300000),
    'diff_internal_man_hours': fields.Float(description='予実差の自社工数', example=130.5),
    'diff_partner_man_hours': fields.Float(description='予実差の協力会社工数', example=80.0),
    'diff_bulk_man_hours': fields.Float(description='予実差の一括契約工数', example=80.0),
    'difference_at': fields.DateTime(description='集計日時', example='2025-04-20T15:00:00Z')
})

@difference_ns.route('')
class DifferenceListResource(Resource):
    @difference_ns.expect(difference_parser)
    @difference_ns.marshal_list_with(difference_model)
    @difference_ns.response(200, '取得成功')
    @difference_ns.response(400, '不正なリクエストパラメータ')
    @difference_ns.response(500, 'サーバーエラー')
    @difference_ns.doc(description="集計済み予実差データ取得します。")
    @jwt_required()
    def get(self):
        month_number = request.args.get('month_number', type=int)

        try:
            logger.info(f"予実差データ取得リクエスト: month_number={month_number}")
            query = DifferenceProfitAndLoss.query

            if month_number is not None:
                query = query.filter_by(month_number=month_number)

            results = query.all()
            logger.info(f"予実差データ取得成功: 件数={len(results)}")
            return results
        except Exception as e:
            logger.exception("予実差データ取得失敗")
            return {'message': 'サーバーエラー', 'error': str(e)}, 500
