"""cost_analyzer.py"""

from .bigquery_client import BigQueryClient
from .budget_client import BudgetClient
from .queries import get_last_30_days_query


class CostAnalyzer:
    """コスト分析クラス"""

    def __init__(
        self,
        project_id: str,
        billing_account_id: str,
        dataset_id: str,
        table_id: str,
    ):
        """コスト分析クラスを初期化します。

        Args:
            project_id (str): GCPプロジェクトID
            billing_account_id (str): 請求アカウントID
            dataset_id (str): BigQueryデータセットID
            table_id (str): BigQueryテーブルID
        """
        self.project_id = project_id
        self.billing_account_id = billing_account_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.bq_client = BigQueryClient(project_id)
        self.budget_client = BudgetClient()

    def get_project_costs(self) -> list[dict]:
        """プロジェクトごとの利用料金を取得します。

        Returns:
            List[Dict]: プロジェクトごとの利用料金情報
        """
        query = get_last_30_days_query(
            project_id=self.project_id,
            dataset_id=self.dataset_id,
            table_id=self.table_id,
        )
        return self.bq_client.execute_query(query)

    def analyze_budget_costs(self) -> list[dict]:
        """予算ごとの利用料金を分析します。

        Returns:
            List[Dict]: 予算ごとの分析結果
        """
        # 利用料金を取得
        costs = self.get_project_costs()
        # 予算情報を取得
        budgets = self.budget_client.list_budgets(self.billing_account_id)
        analysis_results = []

        for budget in budgets:
            budget_name = budget["display_name"]
            budget_amount = budget["amount"]
            project_ids = budget["project_ids"]

            # 予算に設定されたプロジェクトのコストを合計
            total_cost = 0.0
            project_costs = []

            for cost in costs:
                if cost["number"] in project_ids:
                    total_cost += cost["total"]
                    project_costs.append(
                        {
                            "project_id": cost["id"],
                            "project_number": cost["number"],
                            "cost": cost["total"],
                        },
                    )

            # 予算に対する割合を計算
            percentage = (
                (total_cost / budget_amount) * 100 if budget_amount > 0 else 0
            )

            analysis_results.append(
                {
                    "budget_name": budget_name,
                    "budget_amount": budget_amount,
                    "total_cost": total_cost,
                    "percentage": percentage,
                    "project_costs": project_costs,
                },
            )

        return analysis_results

    def print_analysis(self) -> None:
        """利用料金と予算の分析結果を表示します。"""
        try:
            results = self.analyze_budget_costs()
            print("\n予算ごとの利用料金分析結果:")
            print("-" * 50)

            for result in results:
                print(f"予算名: {result['budget_name']}")
                print(f"予算金額: ${result['budget_amount']:.2f}")
                print(f"合計利用料金: ${result['total_cost']:.2f}")
                print(f"予算に対する割合: {result['percentage']:.1f}%")
                print("\nプロジェクトごとの利用料金:")

                for project in result["project_costs"]:
                    print(
                        f"  プロジェクト {project['project_id']} "
                        f"({project['project_number']}): "
                        f"${project['cost']:.2f}",
                    )

                print("-" * 50)
        except Exception as e:
            print(f"分析中にエラーが発生しました: {str(e)}")
            raise
