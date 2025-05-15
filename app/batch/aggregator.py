from app import db
from sqlalchemy import text
from app.logger import get_logger

# ロガー取得
logger = get_logger('aggregator')

VALID_SOURCE_TABLES = {
    "budget_profit_and_loss",
    "actual_profit_and_loss"
}

def insert_aggregated_data(source_type, source_table):
    logger.info(f"🔄 集計開始: {source_table}")

    if source_table not in VALID_SOURCE_TABLES:
        raise ValueError(f"Invalid source_table: {source_table}")
    
    sql = text(f"""
        INSERT INTO aggregated_profit_and_loss (
            source_type,
            parent_group_key,
            group_by_key,
            month_number,
            total_order_amount,
            total_sales,
            total_profit,
            total_internal_man_hours,
            total_partner_man_hours,
            total_bulk_man_hours,
            aggregated_at
        )
        SELECT 
            :source_type AS source_type,
            ac.parent_group_key,
            ac.group_by_key,
            s.month_number,
            SUM(s.order_amount),
            SUM(s.recognized_sales),
            SUM(s.recognized_profit),
            SUM(s.internal_man_hours),
            SUM(s.partner_man_hours),
            SUM(s.bulk_man_hours),
            CURRENT_TIMESTAMP
        FROM {source_table} s
        JOIN aggregation_config ac
          ON s.customer_code = ac.customer_code
         AND s.manager_code = ac.manager_code
         AND s.leader_code = ac.leader_code
        GROUP BY ac.parent_group_key, ac.group_by_key, s.month_number;
    """)

    try:
        db.session.execute(sql, {'source_type': source_type})
        db.session.commit()
        logger.info(f"✅ 集計完了: {source_table}")
            
    except Exception as e:
        db.session.rollback()
        logger.exception(f"❌ {source_table} の集計中にエラーが発生")
        raise

def clear_aggregated_data(source_type=None):
    try:
        if source_type is None:
            logger.info("🧹 aggregated_profit_and_loss 全体をクリア中...")
            db.session.execute(text("DELETE FROM aggregated_profit_and_loss"))
        else:
            logger.info(f"🧹 source_type={source_type} のデータをクリア中...")
            db.session.execute(
                text("DELETE FROM aggregated_profit_and_loss WHERE source_type = :source_type"),
                {'source_type': source_type}
            )
        db.session.commit()
        logger.info("✅ テーブルクリア完了")
    except Exception as e:
        db.session.rollback()
        logger.exception("❌ データクリア中にエラーが発生")
        raise

def run_aggregator_budget():
    try:
        logger.info("予算集計処理開始")
        clear_aggregated_data('0')
        insert_aggregated_data('0', 'budget_profit_and_loss')
        logger.info("🎉 予算の集計完了")
    except Exception as e:
        logger.exception("❌ 予算集計中にエラーが発生")
        raise

def run_aggregator_actual():
    try:
        logger.info("実績集計処理開始")
        clear_aggregated_data('1')
        insert_aggregated_data('1', 'actual_profit_and_loss')
        logger.info("🎉 実績の集計完了")
    except Exception as e:
        logger.exception("❌ 実績集計中にエラーが発生")
        raise

def run_aggregator():
    try:
        logger.info("すべての集計処理開始")
        clear_aggregated_data()
        insert_aggregated_data('0', 'budget_profit_and_loss')
        insert_aggregated_data('1', 'actual_profit_and_loss')
        logger.info("🎉 すべての集計完了")
    except Exception as e:
        logger.exception("❌ 集計中にエラーが発生")
        raise

# CLIから実行された場合
if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        try:
            run_aggregator()
        except Exception as e:
            logger.exception("❌ CLI実行中にエラーが発生")
            exit(1)
