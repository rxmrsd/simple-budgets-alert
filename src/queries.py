"""queries.py"""
from pathlib import Path


def get_last_30_days_query(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> str:
    """直近30日間のプロジェクトごとの合計コスト（クレジットを含む）を取得するクエリを生成します。

    Args:
        project_id (str): GCPプロジェクトID
        dataset_id (str): データセットID
        table_id (str): テーブルID

    Returns:
        str: 生成されたSQLクエリ
    """
    # SQLファイルのパスを取得
    current_dir = Path(__file__).parent
    sql_file_path = current_dir / "sql" / "last_30_days.sql"

    # SQLファイルを読み込む
    with Path.open(sql_file_path) as f:
        base_query = f.read().strip()

    # クエリのパラメータを置換
    query = base_query.format(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )

    return query
