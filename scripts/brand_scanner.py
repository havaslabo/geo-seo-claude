#!/usr/bin/env python3
"""
Brand Mention Scanner — Checks brand presence across AI-cited platforms.

Brand mentions correlate 3x more strongly with AI visibility than backlinks.
(Ahrefs December 2025 study of 75,000 brands)

Platform importance for AI citations:
1. YouTube mentions (~0.737 correlation - STRONGEST)
2. Reddit mentions (high)
3. Wikipedia presence (high)
4. LinkedIn presence (moderate)
5. Domain Rating/backlinks (~0.266 - weak)
"""

import sys
import json
import re
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("エラー：必要なパッケージがインストールされていません。pip install -r requirements.txt を実行してください")
    sys.exit(1)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def check_youtube_presence(brand_name: str) -> dict:
    """Check brand presence on YouTube."""
    result = {
        "platform": "YouTube",
        "correlation": 0.737,
        "weight": "25%",
        "has_channel": False,
        "mentioned_in_videos": False,
        "search_url": f"https://www.youtube.com/results?search_query={quote_plus(brand_name)}",
        "recommendations": [],
    }

    # Note: Actual YouTube API would be used in production
    # This provides the framework for Claude Code to use WebFetch
    result["check_instructions"] = [
        f"Search YouTube for '{brand_name}' and check:",
        "1. Does the brand have an official YouTube channel?",
        "2. Are there videos FROM the brand (tutorials, demos, thought leadership)?",
        "3. Are there videos ABOUT the brand from other creators?",
        "4. What's the view count on brand-related videos?",
        "5. Are there positive reviews or demonstrations?",
    ]

    result["recommendations"] = [
        "Create a YouTube channel if none exists",
        "Publish educational/tutorial content related to your niche",
        "Encourage customers to create review/demo videos",
        "Optimize video titles and descriptions with brand name",
        "Add timestamps and chapters to improve AI parseability",
        "Include transcripts (YouTube auto-generates, but review for accuracy)",
    ]

    return result


def check_reddit_presence(brand_name: str) -> dict:
    """Check brand presence on Reddit."""
    result = {
        "platform": "Reddit",
        "correlation": "High",
        "weight": "25%",
        "has_subreddit": False,
        "mentioned_in_discussions": False,
        "search_url": f"https://www.reddit.com/search/?q={quote_plus(brand_name)}",
        "recommendations": [],
    }

    result["check_instructions"] = [
        f"Search Reddit for '{brand_name}' and check:",
        "1. Does the brand have its own subreddit (r/brandname)?",
        "2. Is the brand discussed in relevant industry subreddits?",
        "3. What's the sentiment (positive, negative, neutral)?",
        "4. Are there recommendation threads mentioning the brand?",
        "5. Does the brand have an official Reddit presence?",
        "6. Are mentions recent (within last 6 months)?",
    ]

    result["recommendations"] = [
        "Monitor relevant subreddits for brand mentions",
        "Participate authentically in industry discussions (no spam)",
        "Create an official Reddit account for customer support",
        "Share valuable content (not just self-promotion)",
        "Respond to questions about your product/service category",
        "Reddit authenticity matters — don't use marketing speak",
    ]

    return result


def check_wikipedia_presence(brand_name: str) -> dict:
    """Check brand/entity presence on Wikipedia and Wikidata."""
    result = {
        "platform": "Wikipedia",
        "correlation": "High",
        "weight": "20%",
        "has_wikipedia_page": False,
        "has_wikidata_entry": False,
        "cited_in_articles": False,
        "search_url": f"https://en.wikipedia.org/wiki/Special:Search?search={quote_plus(brand_name)}",
        "wikidata_url": f"https://www.wikidata.org/w/index.php?search={quote_plus(brand_name)}",
        "recommendations": [],
    }

    # Check Wikipedia API
    try:
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand_name)}&format=json"
        response = requests.get(api_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                # Check if top result is about the brand
                top_title = search_results[0].get("title", "").lower()
                if brand_name.lower() in top_title:
                    result["has_wikipedia_page"] = True
                result["wikipedia_search_results"] = len(search_results)
    except Exception:
        pass

    # Check Wikidata
    try:
        wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={quote_plus(brand_name)}&language=en&format=json"
        response = requests.get(wikidata_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            entities = data.get("search", [])
            if entities:
                result["has_wikidata_entry"] = True
                result["wikidata_id"] = entities[0].get("id", "")
                result["wikidata_description"] = entities[0].get("description", "")
    except Exception:
        pass

    result["recommendations"] = [
        "If eligible, create a Wikipedia article (requires notability criteria)",
        "Ensure Wikidata entry exists with complete structured data",
        "Add sameAs links in schema markup pointing to Wikipedia/Wikidata",
        "Get cited in existing Wikipedia articles as a source",
        "Build notability through press coverage and independent reviews",
        "Note: Wikipedia has strict notability guidelines — PR coverage helps establish this",
    ]

    return result


def check_linkedin_presence(brand_name: str) -> dict:
    """Check brand presence on LinkedIn."""
    result = {
        "platform": "LinkedIn",
        "correlation": "Moderate",
        "weight": "15%",
        "has_company_page": False,
        "employee_thought_leadership": False,
        "search_url": f"https://www.linkedin.com/search/results/companies/?keywords={quote_plus(brand_name)}",
        "recommendations": [],
    }

    result["check_instructions"] = [
        f"Search LinkedIn for '{brand_name}' and check:",
        "1. Does the company have a LinkedIn page?",
        "2. How many followers?",
        "3. Is the page active with recent posts?",
        "4. Do employees post thought leadership content?",
        "5. Are there LinkedIn articles about the brand?",
        "6. Is there engagement on posts (likes, comments, shares)?",
    ]

    result["recommendations"] = [
        "Create/optimize LinkedIn company page",
        "Post regular thought leadership content",
        "Encourage employees to share company content",
        "Publish long-form LinkedIn articles",
        "Engage with industry discussions and comments",
        "Add company LinkedIn URL to schema sameAs property",
    ]

    return result


def check_x_presence(brand_name: str) -> dict:
    """Check brand presence on X (formerly Twitter)."""
    result = {
        "platform": "X (Twitter)",
        "correlation": "High",
        "weight": "20%",
        "note": "日本はX利用率が世界最高水準。AI引用との相関も高い",
        "has_official_account": False,
        "search_url": f"https://x.com/search?q={quote_plus(brand_name)}&src=typed_query",
        "recommendations": [],
    }

    result["check_instructions"] = [
        f"X（Twitter）で '{brand_name}' を検索して確認：",
        "1. 公式アカウントが存在するか？（フォロワー数・認証バッジ）",
        "2. ブランド名・商品名の言及ツイートがあるか？",
        "3. 言及のセンチメント（ポジティブ・ネガティブ・中立）",
        "4. 直近6ヶ月以内の言及か？",
        "5. インフルエンサーや業界メディアによる言及があるか？",
    ]

    result["recommendations"] = [
        "公式Xアカウントを開設・最適化する（プロフィール・ヘッダー・固定ツイート）",
        "製品・サービスのアップデートを定期的に投稿する",
        "業界関連のハッシュタグを活用してリーチを拡大する",
        "ユーザーからの言及・質問に積極的に返信する",
        "スキーマの sameAs プロパティに X アカウント URL を追加する",
        "スペースや長文ポストで専門性をアピールする",
    ]

    return result


def check_chiebukuro_presence(brand_name: str) -> dict:
    """Check brand presence on Yahoo! Chiebukuro (Japan's leading Q&A platform)."""
    result = {
        "platform": "Yahoo!知恵袋",
        "correlation": "High",
        "weight": "15%",
        "note": "日本最大のQ&Aプラットフォーム。AI検索が回答を引用するソースとして重要",
        "has_mentions": False,
        "search_url": f"https://chiebukuro.yahoo.co.jp/search?p={quote_plus(brand_name)}",
        "recommendations": [],
    }

    result["check_instructions"] = [
        f"Yahoo!知恵袋で '{brand_name}' を検索して確認：",
        "1. ブランド・製品に関する質問投稿があるか？",
        "2. 質問への回答の質・量はどうか？",
        "3. ブランド公式または関係者が回答しているか？",
        "4. ネガティブな投稿が上位に出ていないか？",
        "5. カテゴリー（ビジネス・生活・健康など）のどこに多いか？",
    ]

    result["recommendations"] = [
        "知恵袋でのブランド関連の質問を定期的にモニタリングする",
        "誠実で有益な回答を投稿して専門性を示す（過度な宣伝は禁止）",
        "よくある質問をまとめた FAQ ページをサイトに作成し、知恵袋から誘導する",
        "ネガティブな質問には公式として丁寧に回答する",
        "ブランドの公式知恵袋アカウントを取得・運用する",
    ]

    return result


def check_japan_review_platforms(brand_name: str, industry: str = "") -> dict:
    """Check brand presence on Japan-specific review and content platforms."""
    result = {
        "platform": "日本の専門プラットフォーム",
        "weight": "10%",
        "note": "日本のAI引用で参照されやすい国内プラットフォーム群",
        "platforms_checked": {},
        "recommendations": [],
    }

    platforms = {
        "価格.com": f"https://kakaku.com/search_results/?query={quote_plus(brand_name)}",
        "食べログ": f"https://tabelog.com/rst/search/Srt=D/sa={quote_plus(brand_name)}/",
        "@cosme": f"https://www.cosme.net/search/item/search/q/{quote_plus(brand_name)}/",
        "note.com": f"https://note.com/search?q={quote_plus(brand_name)}",
        "Qiita": f"https://qiita.com/search?q={quote_plus(brand_name)}",
        "Zenn": f"https://zenn.dev/search?q={quote_plus(brand_name)}",
        "はてなブックマーク": f"https://b.hatena.ne.jp/search/text?q={quote_plus(brand_name)}",
    }

    result["platforms_checked"] = {
        name: {
            "search_url": url,
            "check_instruction": f"「{brand_name}」を {name} で検索",
        }
        for name, url in platforms.items()
    }

    result["recommendations"] = [
        "価格.com：製品・サービスを登録しレビューを集める（ECサイト・家電・サービス業に重要）",
        "食べログ：飲食店・食品ブランドは必ずプロフィールを整備する",
        "@cosme：美容・化粧品ブランドは公式ページを開設し成分・使い方情報を充実させる",
        "note.com：代表・社員が業界知識を発信してブランドの専門性を示す",
        "Qiita / Zenn：技術系ブランドはエンジニアによるアウトプットを奨励する",
        "はてなブックマーク：良質なコンテンツを発信して自然にブックマークされる状態を作る",
    ]

    return result


def check_google_business_profile(brand_name: str, domain: str = None) -> dict:
    """Check Google Business Profile presence (critical for local businesses in Japan)."""
    result = {
        "platform": "Google ビジネスプロフィール",
        "correlation": "High",
        "weight": "15%",
        "note": "地域ビジネスのAI検索での表示に直結。未登録はAI回答で不利になる",
        "has_gbp": False,
        "search_url": f"https://www.google.com/maps/search/{quote_plus(brand_name)}",
        "recommendations": [],
    }

    # Check via Wikipedia API if the brand has a knowledge panel
    if domain:
        result["domain"] = domain

    result["check_instructions"] = [
        f"Google マップ・検索で '{brand_name}' を検索して確認：",
        "1. Google ビジネスプロフィールが登録されているか？",
        "2. 店舗情報（住所・電話・営業時間）が正確か？",
        "3. 写真・投稿が最新の状態か？",
        "4. Googleレビューの件数・評価はどうか？",
        "5. Q&Aセクションに回答があるか？",
        "6. Google ナレッジパネルが表示されるか？",
    ]

    result["recommendations"] = [
        "Google ビジネスプロフィールを登録・オーナー確認する",
        "NAP（名称・住所・電話番号）をウェブサイトと完全に一致させる",
        "営業時間・定休日を常に最新状態に保つ",
        "商品・サービスのカテゴリを詳細に設定する",
        "週1回以上「投稿」機能で最新情報を発信する",
        "Googleレビューへの返信を徹底する（AI の信頼性評価に影響）",
        "LocalBusiness スキーマの sameAs に GBP の URL を追加する",
    ]

    return result


def check_other_platforms(brand_name: str) -> dict:
    """Check brand presence on additional platforms."""
    result = {
        "platform": "Other Platforms",
        "weight": "15%",
        "platforms_checked": {},
        "recommendations": [],
    }

    platforms = {
        "Quora": f"https://www.quora.com/search?q={quote_plus(brand_name)}",
        "Stack Overflow": f"https://stackoverflow.com/search?q={quote_plus(brand_name)}",
        "GitHub": f"https://github.com/search?q={quote_plus(brand_name)}",
        "Crunchbase": f"https://www.crunchbase.com/textsearch?q={quote_plus(brand_name)}",
        "Product Hunt": f"https://www.producthunt.com/search?q={quote_plus(brand_name)}",
        "G2": f"https://www.g2.com/search?utf8=&query={quote_plus(brand_name)}",
        "Trustpilot": f"https://www.trustpilot.com/search?query={quote_plus(brand_name)}",
    }

    result["platforms_checked"] = {
        name: {
            "search_url": url,
            "check_instruction": f"Search for '{brand_name}' on {name}",
        }
        for name, url in platforms.items()
    }

    result["recommendations"] = [
        "Maintain profiles on industry-relevant platforms",
        "Respond to questions on Quora and Stack Overflow",
        "Encourage customer reviews on G2 and Trustpilot",
        "Keep Crunchbase profile updated (important for B2B)",
        "Open-source contributions on GitHub boost developer brand authority",
        "Product Hunt launch can generate significant initial buzz",
    ]

    return result


def generate_brand_report(brand_name: str, domain: str = None, industry: str = "") -> dict:
    """Generate a comprehensive brand mention report (Japan-optimized)."""
    report = {
        "brand_name": brand_name,
        "domain": domain,
        "analysis_date": "GEO-SEO Claude ツールにより生成",
        "key_insight": "ブランド言及はバックリンクの3倍 AI 可視性と相関する（Ahrefs 2025年12月・75,000ブランド調査）",
        "market": "日本",
        "platforms": {},
        "overall_recommendations": [],
    }

    # Check all platforms
    report["platforms"]["youtube"] = check_youtube_presence(brand_name)
    report["platforms"]["x_twitter"] = check_x_presence(brand_name)
    report["platforms"]["wikipedia"] = check_wikipedia_presence(brand_name)
    report["platforms"]["chiebukuro"] = check_chiebukuro_presence(brand_name)
    report["platforms"]["linkedin"] = check_linkedin_presence(brand_name)
    report["platforms"]["reddit"] = check_reddit_presence(brand_name)
    report["platforms"]["google_business_profile"] = check_google_business_profile(brand_name, domain)
    report["platforms"]["japan_platforms"] = check_japan_review_platforms(brand_name, industry)
    report["platforms"]["other"] = check_other_platforms(brand_name)

    # Overall recommendations (Japan-focused)
    report["overall_recommendations"] = [
        "優先度1：YouTube — AI引用との相関が最も高い（0.737）。教育・解説コンテンツを継続的に発信する",
        "優先度2：X（Twitter）— 日本はX利用率が世界最高水準。ブランドアカウントを運用し言及を増やす",
        "優先度3：Yahoo!知恵袋 — 日本のAI検索が多く参照するQ&Aソース。質問への回答で専門性を示す",
        "優先度4：Wikipedia / Wikidata — プレスカバレッジを積み上げてエントリーを作成・充実させる",
        "優先度5：Google ビジネスプロフィール — 地域ビジネスは登録・最適化が必須",
        "優先度6：業界特化プラットフォーム — 価格.com・食べログ・Qiita など業種に合ったサイトに展開する",
        "共通：全プラットフォームで NAP（名称・住所・電話番号）を統一する",
        "スキーマ：sameAs プロパティに全プラットフォームの URL を追加する",
        "モニタリング：ブランド名のアラートを設定し言及を継続的に把握する",
    ]

    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用法：python brand_scanner.py <brand_name> [domain]")
        print("例：python brand_scanner.py 'Acme Corp' acmecorp.com")
        sys.exit(1)

    brand = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else None

    result = generate_brand_report(brand, domain)
    print(json.dumps(result, indent=2, default=str))
