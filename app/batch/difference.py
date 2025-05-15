from app import db
from sqlalchemy import text
from app.logger import get_logger

# ロガー取得
logger = get_logger('difference')

def insert_difference_profit_and_loss():
    logger.info("🔄 差分処理開始: difference_profit_and_loss")

    sql = text("""
        INSERT INTO difference_profit_and_loss (
            parent_group_key,
            group_by_key,
            month_number,
            diff_internal_man_hours,
            diff_partner_man_hours,
            diff_bulk_man_hours,
            diff_order_amount,
            diff_sales,
            diff_profit
        )
        SELECT
            budget.parent_group_key,
            budget.group_by_key,
            budget.month_number,
            actual.total_internal_man_hours - budget.total_internal_man_hours,
            actual.total_partner_man_hours - budget.total_partner_man_hours,
            actual.total_bulk_man_hours - budget.total_bulk_man_hours,
            actual.total_order_amount - budget.total_order_amount,
            actual.total_sales - budget.total_sales,
            actual.total_profit - budget.total_profit
        FROM
            aggregated_profit_and_loss AS budget
        JOIN
            aggregated_profit_and_loss AS actual
            ON budget.parent_group_key = actual.parent_group_key
            AND budget.group_by_key = actual.group_by_key
            AND budget.month_number = actual.month_number
        WHERE
            budget.source_type = '0'
            AND actual.source_type = '1';
    """)

    try:
        db.session.execute(sql)
        db.session.commit()
        logger.info("✅ 差分処理完了: difference_profit_and_loss")
    except Exception as e:
        db.session.rollback()
        logger.exception("❌ 差分処理中にエラーが発生")
        raise

def run_difference_profit_and_loss():
    try:
        logger.info("🧹 difference_profit_and_loss テーブルをクリア中...")
        db.session.execute(text("DELETE FROM difference_profit_and_loss"))
        db.session.commit()
        logger.info("✅ テーブルクリア完了")

        insert_difference_profit_and_loss()
        logger.info("🎉 すべての差分処理完了")
    except Exception as e:
        db.session.rollback()
        logger.exception("❌ 差分処理中にエラーが発生")
        raise

# CLIから実行された場合
if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        try:
            run_difference_profit_and_loss()
        except Exception as e:
            logger.exception("❌ CLI実行中にエラーが発生")
            exit(1)
