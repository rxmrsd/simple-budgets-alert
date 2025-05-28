"""main.py"""

import os

from dotenv import load_dotenv

from src import CostAnalyzer

load_dotenv()


def main() -> None:
    """メイン実行関数"""
    # 環境変数から設定を取得
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "project_id")
    billing_account_id = os.getenv("BILLING_ACCOUNT_ID", "billing_account_id")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID", "dataset_id")
    table_id = os.getenv("BIGQUERY_TABLE_ID", "table_id")

    if not all([project_id, billing_account_id, dataset_id, table_id]):
        raise ValueError(
            "必要な環境変数が設定されていません。"
            "GOOGLE_CLOUD_PROJECT, BILLING_ACCOUNT_ID, "
            "BIGQUERY_DATASET_ID, BIGQUERY_TABLE_IDを設定してください。",
        )

    # コスト分析の実行
    analyzer = CostAnalyzer(
        project_id=project_id,
        billing_account_id=billing_account_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )

    try:
        analyzer.print_analysis()
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
