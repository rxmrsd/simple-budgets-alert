# Google Cloudの予算と利用料金を直近30日で比較する

# はじめに

Google Cloud Platform (GCP) を利用する際、予算管理は重要な課題の一つです。特に複数のプロジェクトやフォルダを管理している場合、予算と実際の利用料金を比較・分析することは、コスト最適化の第一歩となります。

GCPは予算アラート機能を提供していますが、月間や年間といった期間単位での設定しかできません。より柔軟な予算管理を行うためには、直近の利用状況をリアルタイムで把握し、予算との比較を行う必要があります。

本記事では、GCPの予算と利用料金を直近30日で比較・分析できるPythonスクリプトを作成し、その実装方法と使い方について解説します。なお、本スクリプトはプロジェクト単位での予算アラート設定を前提としています。フォルダ単位や組織単位など、異なる粒度で予算アラートを設定している場合は、コードの修正が必要となります。

# お題

以下の要件を満たすスクリプトを作成します：

1. GCPの予算情報を取得
2. 直近30日間の利用料金を取得
3. 予算と利用料金を比較・分析
4. プロジェクト単位またはフォルダ単位での予算管理に対応
5. 分析結果を見やすく表示

# コードの作成

## 1. プロジェクト構成

```
.
├── main.py
├── src/
│   ├── cost_analyzer.py
│   ├── bigquery_client.py
│   ├── budget_client.py
│   └── queries.py
├── pyproject.toml
└── .env
```

## 2. 主要なコンポーネント

### CostAnalyzer クラス

`CostAnalyzer`クラスは、予算と利用料金の分析を担当する中心的なクラスです。主な機能は以下の通りです：

- プロジェクトごとの利用料金の取得
- 予算情報の取得と分析
- 予算と利用料金の比較
- 分析結果の表示

```python
class CostAnalyzer:
    def __init__(
        self,
        project_id: str,
        billing_account_id: str,
        dataset_id: str,
        table_id: str,
    ):
        self.project_id = project_id
        self.billing_account_id = billing_account_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.bq_client = BigQueryClient(project_id)
        self.budget_client = BudgetClient()
```

### 分析ロジック

予算と利用料金の分析は以下の手順で行われます：

1. BigQueryから直近30日間の利用料金を取得
2. 予算情報を取得
3. プロジェクト単位またはフォルダ単位で予算と利用料金を比較
4. 予算に対する割合を計算

```python
def analyze_budget_costs(self) -> list[dict]:
    costs = self.get_project_costs()
    budgets = self.budget_client.list_budgets(self.billing_account_id)
    analysis_results = []

    for budget in budgets:
        # 予算情報の取得
        budget_name = budget["display_name"]
        budget_amount = budget["amount"]
        project_ids = budget["project_ids"]
        folder_ids = budget["folder_ids"]

        # 利用料金の集計
        total_cost = 0.0
        project_costs = []

        # プロジェクト単位またはフォルダ単位での集計
        if project_ids:
            # プロジェクト単位の処理
            ...
        elif folder_ids:
            # フォルダ単位の処理
            ...

        # 予算に対する割合を計算
        percentage = (total_cost / budget_amount) * 100 if budget_amount > 0 else 0

        analysis_results.append({
            "budget_name": budget_name,
            "budget_amount": budget_amount,
            "total_cost": total_cost,
            "percentage": percentage,
            "project_costs": project_costs,
            "budget_type": "folder" if folder_ids else "project",
        })

    return analysis_results
```

# 結果

スクリプトを実行すると、以下のような形式で分析結果が表示されます：

```
予算ごとの利用料金分析結果:
--------------------------------------------------
予算名: Production Budget
予算タイプ: project単位
予算金額: $1000.00
合計利用料金: $750.50
予算に対する割合: 75.1%

プロジェクトごとの利用料金:
  プロジェクト prod-project-1 (123456789): $450.25
  プロジェクト prod-project-2 (987654321): $300.25
--------------------------------------------------
```

この結果から、以下の情報が一目で分かります：

- 各予算の設定金額
- 実際の利用料金
- 予算に対する利用率
- プロジェクトごとの詳細な利用料金

# まとめ

本記事で作成したスクリプトにより、以下のメリットが得られます：

1. 予算と利用料金の比較が容易になる
2. プロジェクト単位またはフォルダ単位での分析が可能
3. 直近30日間の利用状況を把握できる
4. コスト最適化のための意思決定をサポート

このスクリプトを定期的に実行することで、GCPの利用料金を効果的に管理することができます。

# 参考

- [Google Cloud Billing API](https://cloud.google.com/billing/docs/apis)
- [Google Cloud BigQuery API](https://cloud.google.com/bigquery/docs/reference/rest)
- [Python Google Cloud Client Libraries](https://cloud.google.com/python/docs/reference)

このスクリプトは、GCPの予算管理を自動化し、コスト最適化を支援するための基本的なツールとして活用できます。必要に応じて、アラート機能の追加や、より詳細な分析機能の実装など、機能を拡張することも可能です。
