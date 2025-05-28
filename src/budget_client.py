"""budget_client.py"""

import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from google.cloud.billing import budgets_v1beta1
from google.cloud.billing.budgets_v1beta1.types import ListBudgetsRequest

load_dotenv()


class BudgetClient:
    """予算クライアント"""

    def __init__(self) -> None:
        """予算クライアントを初期化します。"""
        self.client = budgets_v1beta1.BudgetServiceClient()

    def list_budgets(self, billing_account_id: str) -> list[dict]:
        """予算の一覧を取得します。

        Args:
            billing_account_id (str): 請求アカウントID

        Returns:
            List[Dict]: 予算情報のリスト
        """
        parent = f"billingAccounts/{billing_account_id}"
        budgets = []

        try:
            request = ListBudgetsRequest(parent=parent)
            response = self.client.list_budgets(request=request)

            for budget in response:
                # プロジェクトIDのリストを取得
                project_ids = [
                    project.split("/")[-1]
                    for project in budget.budget_filter.projects
                ]

                budget_info = {
                    "display_name": budget.display_name,
                    "amount": float(
                        f"{budget.amount.specified_amount.units}.{budget.amount.specified_amount.nanos:09d}",
                    ),
                    "thresholds": [
                        threshold.threshold_percent
                        for threshold in budget.threshold_rules
                    ],
                    "project_ids": project_ids,
                }
                budgets.append(budget_info)

            return budgets

        except Exception as e:
            print(f"予算取得中にエラーが発生しました: {str(e)}")
            raise

    def get_budgets_by_project_number(
        self,
        billing_account_id: str,
        project_number: str,
    ) -> list[dict]:
        """プロジェクト番号に関連する予算情報を取得します。

        Args:
            billing_account_id (str): 請求アカウントID
            project_number (str): プロジェクト番号

        Returns:
            List[Dict]: プロジェクトに関連する予算情報のリスト
        """
        budgets = self.list_budgets(billing_account_id)
        return [
            budget
            for budget in budgets
            if project_number in budget["project_ids"]
        ]

    def get_budget_info(
        self,
        billing_account_id: str,
        project_number: str,
    ) -> dict | None:
        """プロジェクト番号に関連する予算情報を取得します。
        複数の予算が存在する場合は、最初に見つかった予算を返します。

        Args:
            billing_account_id (str): 請求アカウントID
            project_number (str): プロジェクト番号

        Returns:
            Optional[Dict]: 予算情報。見つからない場合はNone
        """
        budgets = self.get_budgets_by_project_number(
            billing_account_id,
            project_number,
        )
        return budgets[0] if budgets else None


def main() -> None:
    """メイン実行関数"""
    # 環境変数から設定を取得
    billing_account_id = os.getenv("BILLING_ACCOUNT_ID")

    if not billing_account_id:
        raise ValueError(
            "必要な環境変数が設定されていません。"
            "BILLING_ACCOUNT_IDを設定してください。",
        )

    budget_client = BudgetClient()

    try:
        budgets = budget_client.list_budgets(billing_account_id)
        print(budgets)
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
