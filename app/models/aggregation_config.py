from app import db
from datetime import datetime, timezone

# 集計設定モデル
class AggregationConfig(db.Model):
    __tablename__ = 'aggregation_config'

    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    parent_group_key = db.Column(db.String(1), nullable=False)  # 集計軸（親）
    group_by_key = db.Column(db.String(20), nullable=False)  # 集計軸
    customer_code = db.Column(db.String(5), nullable=False)  # 取引先コード
    manager_code = db.Column(db.String(4), nullable=False)  # マネジャーコード
    leader_code = db.Column(db.String(4), nullable=False)  # リーダコード
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 作成日時

    __table_args__ = (
        db.UniqueConstraint('customer_code', 'manager_code', 'leader_code', name='unique_customer_manager_leader'),
    )

    def __repr__(self):
        return f'<AggregationConfig {self.id} - {self.customer_code} - {self.manager_code} - {self.leader_code}>'
