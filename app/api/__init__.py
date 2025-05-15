from .aggregate import aggregate_ns
from .aggregated import aggregated_ns
from .difference import difference_ns
from .upload import upload_budget_ns, upload_actual_ns

# 必要なNamespaceをリスト化
namespaces = [
    aggregate_ns,
    aggregated_ns,
    difference_ns,
    upload_actual_ns,
    upload_budget_ns
]