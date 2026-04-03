<p align="center">
  <img src="assets/banner.svg" alt="GEO-SEO Claude Code Skill" width="900"/>
</p>

<p align="center">
  <strong>GEO ファースト、SEO サポート。</strong> ChatGPT・Claude・Perplexity・Gemini・Google AI Overviews など<br/>
  AI検索エンジンへの最適化を、従来のSEO基盤を維持しながら実現します。
</p>

<p align="center">
  AIがトラディショナルな検索を侵食しています。このツールは、トラフィックが「これから向かう場所」に最適化します。
</p>

---

## なぜ GEO が重要なのか（2026年）

| 指標 | 値 |
|------|-----|
| GEO サービス市場規模 | 8.5億ドル以上（2031年には73億ドル予測） |
| AI経由トラフィックの成長率 | 前年比 +527% |
| AI流入のコンバージョン率（オーガニック比） | 4.4倍 |
| Gartner予測：2028年までの検索トラフィック減少 | -50% |
| バックリンクとの比較でのブランド言及の強さ | 3倍の相関 |
| GEOに投資しているマーケター | わずか23% |

---

## クイックスタート

### ワンコマンドインストール（macOS / Linux）

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install.sh | bash
```

### 手動インストール

```bash
git clone https://github.com/zubair-trabzada/geo-seo-claude.git
cd geo-seo-claude
./install.sh
```

### Windows（Git Bash）

[Git for Windows](https://git-scm.com/downloads)（Git Bash 同梱）が必要です。

```bash
# 方法1：ワンコマンドインストール（PowerShell・CMD ではなく Git Bash で実行）
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install-win.sh | bash

# 方法2：手動インストール
git clone https://github.com/zubair-trabzada/geo-seo-claude.git
cd geo-seo-claude
./install-win.sh
```

> **注意：** フォルダを右クリックして「Open Git Bash here」を選択するか、Git Bash を開いてディレクトリに移動してください。PowerShell や コマンドプロンプトは使用しないでください。

### 動作要件

- Python 3.8 以上
- Claude Code CLI
- Git
- 任意：Playwright（スクリーンショット機能用）

---

## コマンド一覧

Claude Code を開いて以下のコマンドを使用します：

| コマンド | 内容 |
|---------|------|
| `/geo audit <url>` | GEO + SEO 総合監査（並列サブエージェント使用） |
| `/geo quick <url>` | 60秒で分かる GEO 可視性スナップショット |
| `/geo citability <url>` | AI引用スコアの採点 |
| `/geo crawlers <url>` | AIクローラーのアクセス状況確認（robots.txt 解析） |
| `/geo llmstxt <url>` | llms.txt の分析・生成 |
| `/geo brands <url>` | AI引用プラットフォームでのブランド言及スキャン |
| `/geo platforms <url>` | プラットフォーム別最適化 |
| `/geo schema <url>` | 構造化データの分析・生成 |
| `/geo technical <url>` | テクニカル SEO 監査 |
| `/geo content <url>` | コンテンツ品質・E-E-A-T 評価 |
| `/geo report <url>` | クライアント向け GEO レポート生成 |
| `/geo report-pdf` | グラフ・ビジュアライゼーション付き PDF レポート生成 |

---

## アーキテクチャ

```
geo-seo-claude/
├── geo/                          # メインスキルオーケストレーター
│   └── SKILL.md                  # コマンド定義・ルーティング
├── skills/                       # 13の専門サブスキル
│   ├── geo-audit/                # 総合監査・スコアリング
│   ├── geo-citability/           # AI引用スコアリング
│   ├── geo-crawlers/             # AIクローラーアクセス解析
│   ├── geo-llmstxt/              # llms.txt 標準の分析・生成
│   ├── geo-brand-mentions/       # AI引用プラットフォームでのブランド存在感
│   ├── geo-platform-optimizer/   # プラットフォーム別AI検索最適化
│   ├── geo-schema/               # AI発見性のための構造化データ
│   ├── geo-technical/            # テクニカルSEO基盤
│   ├── geo-content/              # コンテンツ品質・E-E-A-T
│   ├── geo-report/               # クライアント向けMarkdownレポート生成
│   ├── geo-report-pdf/           # グラフ付きプロ仕様PDFレポート
│   ├── geo-prospect/             # 営業パイプライン管理（CRM）
│   ├── geo-proposal/             # クライアント提案書の自動生成
│   └── geo-compare/              # 月次デルタ追跡・進捗レポート
├── agents/                       # 5つの並列サブエージェント
│   ├── geo-ai-visibility.md      # GEO監査・引用性・クローラー・ブランド
│   ├── geo-platform-analysis.md  # プラットフォーム別最適化
│   ├── geo-technical.md          # テクニカルSEO分析
│   ├── geo-content.md            # コンテンツ・E-E-A-T 分析
│   └── geo-schema.md             # スキーママークアップ分析
├── scripts/                      # Python ユーティリティ
│   ├── fetch_page.py             # ページ取得・解析
│   ├── citability_scorer.py      # AI引用スコアリングエンジン
│   ├── brand_scanner.py          # ブランド言及検出
│   ├── llmstxt_generator.py      # llms.txt バリデーション・生成
│   └── generate_pdf_report.py    # PDFレポート生成（ReportLab）
├── schema/                       # JSON-LD テンプレート
│   ├── organization.json         # Organization スキーマ（sameAs付き）
│   ├── local-business.json       # LocalBusiness スキーマ
│   ├── article-author.json       # Article + Person スキーマ（E-E-A-T）
│   ├── software-saas.json        # SoftwareApplication スキーマ
│   ├── product-ecommerce.json    # Product スキーマ（オファー付き）
│   └── website-searchaction.json # WebSite + SearchAction スキーマ
├── install.sh                    # ワンコマンドインストーラー
├── uninstall.sh                  # アンインストーラー
├── requirements.txt              # Python 依存パッケージ
└── README.md                     # このファイル
```

---

## データの保存場所

CRM・レポート系スキル（`/geo prospect`・`/geo proposal`・`/geo compare`）の実行データは Claude Code ディレクトリの外に保存されます：

```
~/.geo-prospects/
├── prospects.json              # クライアント・見込み客パイプラインデータ
├── proposals/                  # 生成された提案書
│   └── <domain>-proposal-<date>.md
└── reports/                    # 月次デルタレポート
    └── <domain>-monthly-<YYYY-MM>.md
```

このディレクトリはアンインストーラーでは**削除されません**。見込み客データが不要になった場合は手動で削除してください。

---

## 仕組み

### 総合監査のフロー

`/geo audit https://example.com` を実行すると：

1. **調査** — ホームページ取得・ビジネスタイプ検出・サイトマップクロール
2. **並列分析** — 5つのサブエージェントを同時起動：
   - AI可視性（引用性・クローラー・llms.txt・ブランド言及）
   - プラットフォーム分析（ChatGPT・Perplexity・Google AIO 対応度）
   - テクニカルSEO（Core Web Vitals・SSR・セキュリティ・モバイル）
   - コンテンツ品質（E-E-A-T・可読性・鮮度）
   - スキーママークアップ（検出・バリデーション・生成）
3. **統合** — スコアを集計し、GEO 総合スコア（0〜100）を算出
4. **レポート** — クイックウィン付きの優先アクションプランを出力

### スコアリング方式

| カテゴリ | 重み |
|----------|------|
| AI 引用性・可視性 | 25% |
| ブランド権威シグナル | 20% |
| コンテンツ品質・E-E-A-T | 20% |
| 技術的基盤 | 15% |
| 構造化データ | 10% |
| プラットフォーム最適化 | 10% |

---

## 主な機能

### 引用性スコアリング
コンテンツブロックをAI引用の観点で採点します。AIに引用されやすいパッセージは134〜167語・自己完結・事実が豊富・質問に直接答える構成が最適です。

### AIクローラー分析
robots.txt を対象に14種類以上のAIクローラー（GPTBot・ClaudeBot・PerplexityBot 等）のアクセス状況を確認し、許可・ブロックの具体的な推奨設定を提示します。

### ブランド言及スキャン
ブランド言及はバックリンクの3倍AI可視性との相関があります。YouTube・Reddit・Wikipedia・LinkedIn・その他7つ以上のプラットフォームをスキャンします。

### プラットフォーム別最適化
同じクエリに対してChatGPTとGoogle AI Overviewsの両方から引用されているドメインは全体のわずか11%です。プラットフォームごとにカスタマイズされた推奨事項を提供します。

### llms.txt 生成
AIクローラーがサイト構造を把握するための新興標準ファイル llms.txt を自動生成します。

### クライアント向けレポート
Markdown または PDF 形式のプロ仕様 GEO レポートを生成します。PDF レポートにはスコアゲージ・棒グラフ・プラットフォーム対応状況のビジュアライゼーション・カラーコード付きテーブル・優先アクションプランが含まれ、そのままクライアントへ納品できます。

---

## 活用シーン

- **GEO 代理店** — クライアント監査の実施と成果物の生成
- **マーケティングチーム** — AI検索での可視性のモニタリングと改善
- **コンテンツクリエイター** — AIに引用されるコンテンツへの最適化
- **地域ビジネス** — AIアシスタントに見つけてもらいやすい状態を作る
- **SaaS 企業** — AIプラットフォーム全体でのエンティティ認知度を向上
- **ECサイト** — AI購買推薦に向けた商品ページの最適化

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

## このツールをビジネスにしたい方へ

ツール自体は無料です。収益化の方法はコミュニティで学べます。

**[AI Workshop コミュニティに参加する →](https://skool.com/aiworkshop)**

コミュニティでは以下を提供しています：
- **動画チュートリアル** — セットアップ・監査の実施・結果の読み方をステップバイステップで解説
- **クライアント獲得プレイブック** — 見込み客の発掘・GEOサービスの提案・クロージング方法
- **ライブオフィスアワー** — 監査結果を持ち込んで直接サポートを受けられる
- **GEO 代理店の価格設定＆テンプレート** — 提案書・アウトリーチスクリプト・オンボーディングワークフロー

GEO 代理店の月額単価は $2,000〜$12,000。このツールが監査を担い、コミュニティが販売方法を教えます。

---

## ライセンス

MIT License

---

## コントリビューション

コントリビューション歓迎です！

---

AI検索時代のために作られました。
