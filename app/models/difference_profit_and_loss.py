from app import db
from datetime import datetime, timezone

# 差分損益モデル
class DifferenceProfitAndLoss(db.Model):
    __tablename__ = 'difference_profit_and_loss'

    id = db.Column(db.Integer, primary_key=True)
    parent_group_key = db.Column(db.String(1), nullable=False)
    group_by_key = db.Column(db.String(20), nullable=False)
    month_number = db.Column(db.Integer, nullable=False)
    diff_order_amount = db.Column(db.Integer, default=0)
    diff_sales = db.Column(db.Integer, default=0)
    diff_profit = db.Column(db.Integer, default=0)
    diff_internal_man_hours = db.Column(db.Numeric(5, 2), default=0.00)
    diff_partner_man_hours = db.Column(db.Numeric(5, 2), default=0.00)
    diff_bulk_man_hours = db.Column(db.Numeric(5, 2), default=0.00)
    difference_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('parent_group_key', 'group_by_key', 'month_number', name='unique_parent_group_month'),
    )

    def __repr__(self):
        return f"<DifferenceProfitAndLoss {self.id} - {self.parent_group_key} - {self.group_by_key} - {self.month_number}>"