from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.batch.aggregator import run_aggregator_actual, run_aggregator_budget
from app.batch.difference import run_difference_profit_and_loss
from app.logger import get_logger 

# ロガー取得
logger = get_logger('aggregate') 

aggregate_ns = Namespace('aggregate', description='予算、実績データの集計と予実差の集計API')

@aggregate_ns.route('/budget')
class BudgetResource(Resource):
    @aggregate_ns.response(200, '集計成功')
    @aggregate_ns.response(500, 'サーバーエラー（集計失敗）')
    @aggregate_ns.doc(description="アップロード済みの予算データを集計します。")
    @jwt_required(locations=["cookies"])
    def post(self):
        try:
            logger.info("予算データ集計処理開始")
            # 予算の集計
            run_aggregator_budget()
            logger.info("予算データ集計処理完了")
            
            return {'message': '集計完了'}, 200
        except Exception as e:
            logger.exception("予算データ集計失敗")
            return {'message': '集計失敗', 'error': str(e)}, 500


@aggregate_ns.route('/actual-and-difference')
class ActualAndDifferenceAggregatorResource(Resource):
    @aggregate_ns.response(200, '集計成功')
    @aggregate_ns.response(500, 'サーバーエラー（集計失敗）')
    @aggregate_ns.doc(description="アップロード済みの実績データと予実差の集計します。")
    @jwt_required()
    def post(self):
        try:
            logger.info("実績データ集計処理開始")
            # 実績の集計
            run_aggregator_actual()
            logger.info("実績データ集計処理完了")

            logger.info("予実差集計処理開始")
            # 予実差の集計
            run_difference_profit_and_loss()
            logger.info("予実差集計処理完了")

            return {'message': '集計完了'}, 200
        except Exception as e:
            logger.exception("実績データまたは予実差集計失敗")
            return {'message': '集計失敗', 'error': str(e)}, 500

