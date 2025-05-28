"""bigquery_client.py"""
import os
from typing import Any

from dotenv import load_dotenv
from google.cloud import bigquery

from src.queries import get_last_30_days_query

load_dotenv()


class BigQueryClient:
    """BigQueryクライアント"""
    def __init__(self, project_id: str):
        """BigQueryクライアントを初期化します。

        Args:
            project_id (str): GCPプロジェクトID
        """
        self.client = bigquery.Client(project=project_id)

    def execute_query(self, query: str) -> list[dict[str, Any]]:
        """SQLクエリを実行し、結果を返します。

        Args:
            query (str): 実行するSQLクエリ

        Returns:
            List[Dict[str, Any]]: クエリ結果のリスト
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()

            return [dict(row.items()) for row in results]
        except Exception as e:
            print(f"クエリ実行中にエラーが発生しました: {str(e)}")
            raise

    def get_table_schema(
        self, dataset_id: str, table_id: str,
    ) -> list[dict[str, Any]]:
        """テーブルのスキーマ情報を取得します。

        Args:
            dataset_id (str): データセットID
            table_id (str): テーブルID

        Returns:
            List[Dict[str, Any]]: スキーマ情報のリスト
        """
        try:
            table_ref = f"{self.client.project}.{dataset_id}.{table_id}"
            table = self.client.get_table(table_ref)
            return [
                {"name": field.name, "type": field.field_type}
                for field in table.schema
            ]
        except Exception as e:
            print(f"スキーマ取得中にエラーが発生しました: {str(e)}")
            raise


def main() -> None:
    """メイン実行関数"""
    # 環境変数からプロジェクトIDを取得
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dataset_id = os.getenv("DATASET_ID")
    table_id = os.getenv("TABLE_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT環境変数が設定されていません。")

    # BigQueryクライアントのインスタンスを作成
    bq_client = BigQueryClient(project_id)

    # サンプルクエリの実行
    query = get_last_30_days_query(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )

    try:
        results = bq_client.execute_query(query)
        print("クエリ結果:")
        for row in results:
            print(row)
    except Exception as e:
        print(f"エラー: {str(e)}")


if __name__ == "__main__":
    main()
