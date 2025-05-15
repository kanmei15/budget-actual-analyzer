from app import db
from datetime import datetime, timezone

# 集計損益モデル
class AggregatedProfitAndLoss(db.Model):
    __tablename__ = 'aggregated_profit_and_loss'

    id = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(1), nullable=False) # 0: budget, 1: actual
    parent_group_key = db.Column(db.String(1), nullable=False)
    group_by_key = db.Column(db.String(20), nullable=False)
    month_number = db.Column(db.Integer, nullable=False)
    total_order_amount = db.Column(db.Integer, default=0)
    total_sales = db.Column(db.Integer, default=0)
    total_profit = db.Column(db.Integer, default=0)
    total_internal_man_hours = db.Column(db.Numeric(5, 2), default=0.00)
    total_partner_man_hours = db.Column(db.Numeric(5, 2), default=0.00)
    total_bulk_man_hours = db.Column(db.Numeric(5, 2), default=0.00)
    aggregated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('source_type', 'parent_group_key', 'group_by_key', 'month_number', name='unique_source_parent_group_month'),
    )

    def __repr__(self):
        return f"<AggregatedProfitAndLoss {self.id} - {self.source_type} - {self.parent_group_key} - {self.group_by_key} - {self.month_number}>"