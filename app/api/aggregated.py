from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from app.models import AggregatedProfitAndLoss
from app.logger import get_logger

# ロガー取得
logger = get_logger('aggregated') 

aggregated_ns = Namespace('aggregated', description='集計済み損益データ取得')

aggregated_parser = aggregated_ns.parser()
aggregated_parser.add_argument('month_number', type=int, help='月 (1〜12)', location='args')
aggregated_parser.add_argument('source_type', type=str, help='ソース種別 (0: 予算, 1: 実績)', choices=['0', '1'], location='args')

aggregated_model = aggregated_ns.model('AggregatedProfitAndLoss', {
    'id': fields.Integer(description='一意の識別子', example=123),
    'source_type': fields.String(
        description='ソース種別 (0: 予算, 1: 実績)',
        enum=['0', '1'],
        example='1'
    ),
    'parent_group_key': fields.String(description='集計軸（親）', example='1'),
    'group_by_key': fields.String(description='集計軸', example='〇〇〇会社'),
    'month_number': fields.Integer(description='月 (1〜12)', example=4),
    'total_order_amount': fields.Integer(description='集計した受注額', example=1200000),
    'total_sales': fields.Integer(description='集計した売上計上額', example=1100000),
    'total_profit': fields.Integer(description='集計した利益計上額', example=300000),
    'total_internal_man_hours': fields.Float(description='集計した自社工数', example=130.5),
    'total_partner_man_hours': fields.Float(description='集計した協力会社工数', example=80.0),
    'total_bulk_man_hours': fields.Float(description='集計した一括契約工数', example=80.0),
    'aggregated_at': fields.DateTime(description='集計日時', example='2025-04-20T15:00:00Z')
})

@aggregated_ns.route('')
class AggregatedListResource(Resource):
    @aggregated_ns.expect(aggregated_parser)
    @aggregated_ns.marshal_list_with(aggregated_model)
    @aggregated_ns.response(200, '取得成功')
    @aggregated_ns.response(400, '不正なリクエストパラメータ')
    @aggregated_ns.response(500, 'サーバーエラー')
    @aggregated_ns.doc(description="集計済み損益データを取得します。")
    @jwt_required()
    def get(self):
        month_number = request.args.get('month_number', type=int)
        source_type = request.args.get('source_type')

        try:
            logger.info(f"集計済み損益データ取得リクエスト: month_number={month_number}, source_type={source_type}")
            query = AggregatedProfitAndLoss.query

            if month_number is not None:
                query = query.filter_by(month_number=month_number)
            if source_type is not None:
                query = query.filter_by(source_type=source_type)

            results = query.all()
            logger.info(f"集計済み損益データ取得成功: 件数={len(results)}")
            return results
        except Exception as e:
            logger.exception("集計済み損益データ取得失敗")
            return {'message': 'サーバーエラー', 'error': str(e)}, 500
