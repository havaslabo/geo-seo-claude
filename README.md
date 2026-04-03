<p align="center">
  <img src="assets/banner.svg" alt="GEO-SEO Claude Code Skill" width="900"/>
</p>

<p align="center">
  <strong>GEO ファースト、SEO サポート。</strong><br/>
  ChatGPT・Claude・Perplexity・Gemini・Google AI Overviews などの AI 検索エンジンに<br/>
  コンテンツを引用・紹介してもらうための最適化ツールです。
</p>

<p align="center">
  検索トラフィックは AI に移行しつつあります。<br/>このツールは「今後トラフィックが集まる場所」に向けて最適化します。
</p>

---

## GEO が注目される理由（2026年現在）

| 指標 | 数値 |
|------|------|
| GEO サービスの市場規模 | 8.5億ドル以上（2031年には73億ドルへ拡大予測） |
| AI 経由トラフィックの伸び率 | 前年比 +527% |
| AI 流入のコンバージョン率（オーガニック検索比） | 4.4倍 |
| Gartner 予測：2028年までの検索トラフィック減少率 | -50% |
| バックリンクよりもブランド言及が AI 可視性に与える影響 | 3倍の相関 |
| すでに GEO に取り組んでいるマーケター | わずか 23% |

---

## インストール

### ワンコマンドで完了（macOS / Linux）

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install.sh | bash
```

### 手動でインストールする場合

```bash
git clone https://github.com/zubair-trabzada/geo-seo-claude.git
cd geo-seo-claude
./install.sh
```

### Windows の場合（Git Bash を使用）

[Git for Windows](https://git-scm.com/downloads) をインストールすると Git Bash が使えるようになります。

```bash
# 方法 1：ワンコマンドインストール（必ず Git Bash から実行してください）
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install-win.sh | bash

# 方法 2：手動インストール
git clone https://github.com/zubair-trabzada/geo-seo-claude.git
cd geo-seo-claude
./install-win.sh
```

> **注意：** フォルダを右クリックして「Git Bash Here」を選択するか、Git Bash を起動してディレクトリを移動してください。PowerShell やコマンドプロンプトからは実行しないでください。

### 動作環境

- Python 3.8 以上
- Claude Code CLI
- Git
- Playwright（任意・スクリーンショット撮影に使用）

---

## 使い方

Claude Code 上で以下のコマンドを入力します：

| コマンド | できること |
|---------|-----------|
| `/geo audit <url>` | サイト全体の GEO + SEO 総合監査 |
| `/geo quick <url>` | 約60秒で GEO 可視性をざっくり確認 |
| `/geo citability <url>` | ページが AI に引用されやすいか採点 |
| `/geo crawlers <url>` | AI クローラーがサイトに入れるか確認（robots.txt 解析） |
| `/geo llmstxt <url>` | llms.txt の検証・自動生成 |
| `/geo brands <url>` | 各プラットフォームでのブランド言及状況を確認 |
| `/geo platforms <url>` | プラットフォーム別に最適化ポイントを確認 |
| `/geo schema <url>` | 構造化データの分析・生成 |
| `/geo technical <url>` | テクニカル SEO の問題点を洗い出す |
| `/geo content <url>` | コンテンツ品質・E-E-A-T の評価 |
| `/geo report <url>` | クライアントに渡せる GEO レポートを生成 |
| `/geo report-pdf` | グラフ入りの PDF レポートを生成 |

---

## ディレクトリ構成

```
geo-seo-claude/
├── geo/                          # メインスキル（コマンド定義・処理の振り分け）
│   └── SKILL.md
├── skills/                       # 13 種類の専門スキル
│   ├── geo-audit/                # 総合監査・スコア計算
│   ├── geo-citability/           # AI 引用スコアリング
│   ├── geo-crawlers/             # AI クローラーのアクセス解析
│   ├── geo-llmstxt/              # llms.txt の分析・生成
│   ├── geo-brand-mentions/       # ブランド言及の調査
│   ├── geo-platform-optimizer/   # プラットフォーム別最適化
│   ├── geo-schema/               # 構造化データの管理
│   ├── geo-technical/            # テクニカル SEO
│   ├── geo-content/              # コンテンツ品質・E-E-A-T
│   ├── geo-report/               # Markdown レポート生成
│   ├── geo-report-pdf/           # PDF レポート生成
│   ├── geo-prospect/             # 営業パイプライン管理（CRM）
│   ├── geo-proposal/             # 提案書の自動生成
│   └── geo-compare/              # 月次の改善状況レポート
├── agents/                       # 5 つの並列サブエージェント
│   ├── geo-ai-visibility.md      # GEO 監査・引用性・クローラー・ブランド言及
│   ├── geo-platform-analysis.md  # プラットフォーム別最適化
│   ├── geo-technical.md          # テクニカル SEO 分析
│   ├── geo-content.md            # コンテンツ・E-E-A-T 分析
│   └── geo-schema.md             # スキーママークアップ分析
├── scripts/                      # Python スクリプト群
│   ├── fetch_page.py             # ページ取得・解析
│   ├── citability_scorer.py      # AI 引用スコアの計算エンジン
│   ├── brand_scanner.py          # ブランド言及の検出
│   ├── llmstxt_generator.py      # llms.txt の検証・生成
│   └── generate_pdf_report.py    # PDF レポート生成（ReportLab 使用）
├── schema/                       # JSON-LD テンプレート集
│   ├── organization.json         # Organization スキーマ（sameAs 対応）
│   ├── local-business.json       # LocalBusiness スキーマ
│   ├── article-author.json       # Article + Person スキーマ（E-E-A-T 対応）
│   ├── software-saas.json        # SoftwareApplication スキーマ
│   ├── product-ecommerce.json    # Product スキーマ（価格情報付き）
│   └── website-searchaction.json # WebSite + SearchAction スキーマ
├── install.sh                    # インストールスクリプト
├── uninstall.sh                  # アンインストールスクリプト
├── requirements.txt              # Python パッケージ一覧
└── README.md                     # このファイル
```

---

## データの保存先

CRM・レポート系の機能（`/geo prospect`・`/geo proposal`・`/geo compare`）が生成するデータは、Claude Code のインストールディレクトリとは別の場所に保存されます。

```
~/.geo-prospects/
├── prospects.json              # 見込み客・クライアントのパイプライン情報
├── proposals/                  # 自動生成された提案書
│   └── <domain>-proposal-<date>.md
└── reports/                    # 月次の進捗レポート
    └── <domain>-monthly-<YYYY-MM>.md
```

このディレクトリはアンインストール時に**自動削除されません**。不要になった場合は手動で削除してください。

---

## 動作の仕組み

### 総合監査の流れ

`/geo audit https://example.com` を実行すると、以下のステップで処理が進みます：

1. **調査フェーズ** — ホームページを取得し、ビジネスの種類を判定。サイトマップをたどってページを収集します
2. **並列分析フェーズ** — 5つのサブエージェントが同時に動き出します：
   - AI 可視性（引用性・クローラーアクセス・llms.txt・ブランド言及）
   - プラットフォーム対応度（ChatGPT・Perplexity・Google AIO）
   - テクニカル SEO（Core Web Vitals・SSR・セキュリティ・モバイル対応）
   - コンテンツ品質（E-E-A-T・読みやすさ・情報の鮮度）
   - スキーママークアップ（検出・検証・生成）
3. **集計フェーズ** — 各スコアを重み付けして GEO 総合スコア（0〜100）を算出
4. **出力フェーズ** — 今すぐ取り組める改善策から中長期施策まで、優先度付きでレポートを出力

### スコアの内訳

| カテゴリ | ウェイト |
|----------|---------|
| AI 引用性・可視性 | 25% |
| ブランド権威シグナル | 20% |
| コンテンツ品質・E-E-A-T | 20% |
| 技術的基盤 | 15% |
| 構造化データ | 10% |
| プラットフォーム最適化 | 10% |

---

## 主な機能

### 引用性スコアリング
各コンテンツブロックを「AI に引用されやすいか」という観点で 0〜100 点で評価します。引用されやすいパッセージには「134〜167語程度」「前後の文脈なしで意味が伝わる」「具体的な数値や事実が含まれる」「質問に直接答える形になっている」といった共通点があります。

### AI クローラー分析
GPTBot・ClaudeBot・PerplexityBot など 14 種類以上の AI クローラーが robots.txt でブロックされていないか確認し、推奨設定を提示します。

### ブランド言及スキャン
バックリンクよりもブランド言及のほうが AI 可視性との相関が 3 倍強いことがわかっています（Ahrefs 調査）。YouTube・Reddit・Wikipedia・LinkedIn など 7 つ以上のプラットフォームでの言及状況を調査します。

### プラットフォーム別最適化
同じ検索クエリに対して ChatGPT と Google AI Overviews の両方に引用されているサイトは全体の 11% しかありません。各プラットフォームの特性に合わせた改善策を提案します。

### llms.txt 生成
AI クローラーにサイトの構造と重要なページを伝えるための llms.txt ファイルを自動生成します。robots.txt に似た新しい標準仕様で、対応しているサイトはまだ少なく、先行できる余地が大きい分野です。

### クライアント向けレポート
Markdown または PDF 形式で、そのままクライアントに渡せるプロ仕様のレポートを生成します。PDF にはスコアゲージ・棒グラフ・プラットフォーム対応状況の一覧・優先改善リストが含まれます。

---

## こんな用途に

- **GEO コンサルタント・代理店** — クライアントサイトの監査から提案書・レポート納品まで一気通貫
- **マーケティング担当者** — 自社サイトの AI 検索における露出状況を把握・改善
- **コンテンツライター** — AI に引用されやすいコンテンツ構成を把握
- **地域密着型ビジネス** — AI アシスタントで検索されたときに表示されるよう対策
- **SaaS 企業** — AI プラットフォーム全体でブランドとして認識されるよう強化
- **EC サイト** — AI が買い物の提案をする際に商品が推薦されるよう最適化

---

## アンインストール

```bash
./uninstall.sh
```

手動で削除する場合：
```bash
rm -rf ~/.claude/skills/geo ~/.claude/skills/geo-* ~/.claude/agents/geo-*.md
```

---


## ライセンス

MIT License

---

## コントリビューション

プルリクエスト・Issue 歓迎です！

---

AI 検索の時代に向けて作られたツールです。
