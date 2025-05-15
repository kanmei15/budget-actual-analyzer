from app import db
from datetime import datetime, timezone

# 実績損益モデル
class ActualProfitAndLoss(db.Model):
    __tablename__ = 'actual_profit_and_loss'

    id = db.Column(db.Integer, primary_key=True)  # 一意の識別子
    order_code = db.Column(db.String(10), nullable=False)  # オーダーコード
    order_name = db.Column(db.String(1000), nullable=False)  # オーダー名
    deal_status = db.Column(db.String(1), nullable=False)  # 商談区分
    customer_code = db.Column(db.String(5), nullable=False)  # 取引先コード
    start_dt = db.Column(db.Date, nullable=False)  # 作業開始日
    end_dt = db.Column(db.Date, nullable=False)  # 作業終了日
    manager_code = db.Column(db.String(4), nullable=False)  # マネジャーコード
    leader_code = db.Column(db.String(4), nullable=False)  # リーダーコード
    month_number = db.Column(db.Integer, nullable=False)  # 月
    internal_man_hours = db.Column(db.Numeric(5, 2), default=0.00)  # 自社工数
    partner_man_hours = db.Column(db.Numeric(5, 2), default=0.00)  # 協力会社工数
    bulk_man_hours = db.Column(db.Numeric(5, 2), default=0.00)  # 一括契約工数
    order_amount = db.Column(db.Integer, default=0)  # 受注額
    recognized_sales = db.Column(db.Integer, default=0)  # 売上計上額
    recognized_profit = db.Column(db.Integer, default=0)  # 利益計上額
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 作成日時

    _table_args__ = (
        db.UniqueConstraint('order_code', 'month_number', name='unique_order_month'),
    )

    def __repr__(self):
        return f'<ActualProfitAndLoss {self.id} - {self.order_code} - {self.month_number}>'