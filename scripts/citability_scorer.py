#!/usr/bin/env python3
"""
Citability Scorer — Analyzes content blocks for AI citation readiness.
Scores passages based on how likely AI models are to cite them.

Based on research showing optimal AI-cited passages are:
- 134-167 words long
- Self-contained (extractable without context)
- Fact-rich with specific statistics
- Structured with clear answer patterns
"""

import sys
import json
import re
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("エラー：必要なパッケージがインストールされていません。pip install -r requirements.txt を実行してください")
    sys.exit(1)


def is_japanese_text(text: str) -> bool:
    """Return True if the text is predominantly Japanese (hiragana/katakana/kanji)."""
    jp_chars = len(re.findall(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff66-\uff9f]', text))
    total_chars = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    return total_chars > 0 and jp_chars / total_chars >= 0.2


def score_passage(text: str, heading: Optional[str] = None) -> dict:
    """Score a single passage for AI citability (0-100).
    Supports both English and Japanese text with language-appropriate heuristics."""
    is_ja = is_japanese_text(text)
    words = text.split()
    word_count = len(words)
    # For Japanese, character count / 2 is a rough word-count equivalent
    char_count = len(text.replace(' ', '').replace('\n', ''))
    effective_word_count = char_count // 2 if is_ja else word_count

    scores = {
        "answer_block_quality": 0,
        "self_containment": 0,
        "structural_readability": 0,
        "statistical_density": 0,
        "uniqueness_signals": 0,
    }

    # === 1. Answer Block Quality (30%) ===
    abq_score = 0

    if is_ja:
        # Japanese definition patterns: 〜とは、〜です。〜は〜を指す。〜のことです。
        ja_definition_patterns = [
            r'[\u3040-\u9fff]+とは[、,\s]',
            r'[\u3040-\u9fff]+(?:とは|というのは)[^\。]*(?:です|ます|である)',
            r'[\u3040-\u9fff]+を指(?:す|します)',
            r'[\u3040-\u9fff]+のことです',
            r'[\u3040-\u9fff]+とも呼ばれ',
        ]
        for pattern in ja_definition_patterns:
            if re.search(pattern, text):
                abq_score += 15
                break

        # Check if answer appears early (first ~120 characters)
        first_120_chars = text[:120]
        if any(
            re.search(p, first_120_chars)
            for p in [
                r'\d+(?:\.\d+)?%',
                r'¥[\d,]+',
                r'\d+(?:,\d{3})*(?:\.\d+)?\s*(?:万円|億円|円)',
                r'\d+(?:,\d{3})*\s*(?:人|社|件|店|倍)',
                r'(?:です|ます|である)[。、]',
            ]
        ):
            abq_score += 15

        # Japanese question-based heading
        if heading and (heading.endswith('？') or heading.endswith('?') or
                        re.search(r'(?:とは|でしょうか|ますか|ますか？|ですか)$', heading)):
            abq_score += 10

        # Sentence clarity for Japanese (split by 。！？)
        sentences = re.split(r'[。！？]+', text)
        short_clear_sentences = sum(
            1 for s in sentences if 10 <= len(s) <= 100
        )
        if sentences:
            clarity_ratio = short_clear_sentences / len(sentences)
            abq_score += int(clarity_ratio * 10)

        # Quotable claim with source
        if re.search(r'(?:によると|によれば|の調査|の研究|のデータ|調査では|研究では)', text):
            abq_score += 10
    else:
        # Check for definition patterns ("X is...", "X refers to...", "X means...")
        definition_patterns = [
            r"\b\w+\s+is\s+(?:a|an|the)\s",
            r"\b\w+\s+refers?\s+to\s",
            r"\b\w+\s+means?\s",
            r"\b\w+\s+(?:can be |are )?defined\s+as\s",
            r"\bin\s+(?:simple|other)\s+(?:terms|words)\s*,",
        ]
        for pattern in definition_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                abq_score += 15
                break

        # Check if answer appears early (first 60 words)
        first_60_words = " ".join(words[:60])
        if any(
            re.search(p, first_60_words, re.IGNORECASE)
            for p in [
                r"\b(?:is|are|was|were|means?|refers?)\b",
                r"\d+%",
                r"\$[\d,]+",
                r"\d+\s+(?:million|billion|thousand)",
            ]
        ):
            abq_score += 15

        # Question-based heading bonus
        if heading and heading.endswith("?"):
            abq_score += 10

        # Clear, direct sentence structure
        sentences = re.split(r"[.!?]+", text)
        short_clear_sentences = sum(
            1 for s in sentences if 5 <= len(s.split()) <= 25
        )
        if sentences:
            clarity_ratio = short_clear_sentences / len(sentences)
            abq_score += int(clarity_ratio * 10)

        # Has specific, quotable claim
        if re.search(
            r"(?:according to|research shows|studies? (?:show|indicate|suggest|found)|data (?:shows|indicates|suggests))",
            text,
            re.IGNORECASE,
        ):
            abq_score += 10

    scores["answer_block_quality"] = min(abq_score, 30)

    # === 2. Self-Containment (25%) ===
    sc_score = 0

    # Optimal length check (uses effective_word_count for both languages)
    # Japanese optimal: ~200-400 chars (~100-200 effective words)
    if 134 <= effective_word_count <= 167:
        sc_score += 10
    elif 100 <= effective_word_count <= 200:
        sc_score += 7
    elif 80 <= effective_word_count <= 250:
        sc_score += 4
    elif effective_word_count < 30 or effective_word_count > 400:
        sc_score += 0
    else:
        sc_score += 2

    if is_ja:
        # Japanese pronoun density check (demonstratives that reduce self-containment)
        ja_pronoun_count = len(re.findall(
            r'(?:これ|それ|あれ|この|その|あの|ここ|そこ|あそこ|彼|彼女|彼ら|彼女ら|同社|同氏|同書)',
            text
        ))
        if char_count > 0:
            pronoun_ratio = ja_pronoun_count / (char_count / 100)
            if pronoun_ratio < 1.0:
                sc_score += 8
            elif pronoun_ratio < 2.0:
                sc_score += 5
            elif pronoun_ratio < 3.0:
                sc_score += 3

        # Named entities: Japanese companies (株式会社), brands, product names
        ja_entities = len(re.findall(r'(?:株式会社|有限会社|合同会社|一般社団法人|公益財団法人)[^\s、。]{1,20}', text))
        ja_entities += len(re.findall(r'[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*', text))  # English brand names
        if ja_entities >= 3:
            sc_score += 7
        elif ja_entities >= 1:
            sc_score += 4
    else:
        # Low pronoun density (fewer pronouns = more self-contained)
        pronoun_count = len(
            re.findall(
                r"\b(?:it|they|them|their|this|that|these|those|he|she|his|her)\b",
                text,
                re.IGNORECASE,
            )
        )
        if word_count > 0:
            pronoun_ratio = pronoun_count / word_count
            if pronoun_ratio < 0.02:
                sc_score += 8
            elif pronoun_ratio < 0.04:
                sc_score += 5
            elif pronoun_ratio < 0.06:
                sc_score += 3

        # Contains named entities (proper nouns, brands, specific terms)
        proper_nouns = len(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text))
        if proper_nouns >= 3:
            sc_score += 7
        elif proper_nouns >= 1:
            sc_score += 4

    scores["self_containment"] = min(sc_score, 25)

    # === 3. Structural Readability (20%) ===
    sr_score = 0

    if is_ja:
        # Sentence count and avg length for Japanese (in characters)
        if sentences:
            avg_sentence_chars = char_count / len(sentences)
            if 20 <= avg_sentence_chars <= 80:
                sr_score += 8
            elif 15 <= avg_sentence_chars <= 120:
                sr_score += 5
            else:
                sr_score += 2

        # Japanese list-like connectors
        if re.search(r'(?:まず|次に|つぎに|また|さらに|加えて|一方|最後に|ただし|なお|ちなみに)', text):
            sr_score += 4

        # Numbered/bulleted items
        if re.search(r'(?:\d+[．\.\)）]\s|第\d+[条節]|【\d+】)', text):
            sr_score += 4
    else:
        # Sentence count and length distribution
        if sentences:
            avg_sentence_length = word_count / len(sentences)
            if 10 <= avg_sentence_length <= 20:
                sr_score += 8
            elif 8 <= avg_sentence_length <= 25:
                sr_score += 5
            else:
                sr_score += 2

        # Contains list-like structures
        if re.search(r"(?:first|second|third|finally|additionally|moreover|furthermore)", text, re.IGNORECASE):
            sr_score += 4

        # Contains numbered items or bullet-like content
        if re.search(r"(?:\d+[\.\)]\s|\b(?:step|tip|point)\s+\d+)", text, re.IGNORECASE):
            sr_score += 4

    # Paragraph breaks (indicates structure) — applies to both languages
    if "\n" in text:
        sr_score += 4

    scores["structural_readability"] = min(sr_score, 20)

    # === 4. Statistical Density (15%) ===
    sd_score = 0

    # Percentages
    pct_count = len(re.findall(r"\d+(?:\.\d+)?%", text))
    sd_score += min(pct_count * 3, 6)

    # Currency amounts (yen, dollar, euro)
    dollar_count = len(re.findall(
        r"(?:\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|M|B|K))?"
        r"|¥[\d,]+(?:\.\d+)?(?:\s*(?:万|億|千))?"
        r"|\d+(?:,\d{3})*(?:\.\d+)?\s*(?:万円|億円|千円|円))",
        text
    ))
    sd_score += min(dollar_count * 3, 5)

    # Other numbers with context (English and Japanese units)
    number_count = len(re.findall(
        r"(?:\b\d+(?:,\d{3})*(?:\.\d+)?\s+(?:users|customers|pages|sites|companies|businesses|people|percent|times|x\b)"
        r"|\d+(?:,\d{3})*(?:\.\d+)?\s*(?:人|社|件|店|か所|ヶ所|倍|割|分))",
        text, re.IGNORECASE
    ))
    sd_score += min(number_count * 2, 4)

    # Year references (indicates timeliness)
    year_count = len(re.findall(r"\b20(?:2[3-6]|1\d)\b", text))
    if year_count > 0:
        sd_score += 2

    # Named sources
    source_patterns = [
        r"(?:according to|per|from|by)\s+[A-Z]",
        r"(?:Gartner|Forrester|McKinsey|Harvard|Stanford|MIT|Google|Microsoft|OpenAI|Anthropic)",
        r"\([A-Z][a-z]+(?:\s+\d{4})?\)",
    ]
    for pattern in source_patterns:
        if re.search(pattern, text):
            sd_score += 2

    scores["statistical_density"] = min(sd_score, 15)

    # === 5. Uniqueness Signals (10%) ===
    us_score = 0

    if is_ja:
        # Japanese original data indicators
        if re.search(r'(?:自社(?:調査|データ|研究|分析|調べ)|独自(?:調査|データ|研究|分析)|弊社(?:調査|調べ))', text):
            us_score += 5
        # Case study / example indicators
        if re.search(r'(?:事例|具体例|例えば|たとえば|ケーススタディ|実際に|実践)', text):
            us_score += 3
        # Specific tool/service mentions
        if re.search(r'(?:を使(?:用|って)|を活用|を導入|により|にて)[、。]?[\u3040-\u9fff]', text):
            us_score += 2
    else:
        # Original data indicators
        if re.search(
            r"(?:our (?:research|study|data|analysis|survey|findings)|we (?:found|discovered|analyzed|surveyed|measured))",
            text,
            re.IGNORECASE,
        ):
            us_score += 5

        # Case study or example indicators
        if re.search(
            r"(?:case study|for example|for instance|in practice|real-world|hands-on)",
            text,
            re.IGNORECASE,
        ):
            us_score += 3

        # Specific tool/product mentions (shows practical experience)
        if re.search(r"(?:using|with|via|through)\s+[A-Z][a-z]+", text):
            us_score += 2

    scores["uniqueness_signals"] = min(us_score, 10)

    # === Calculate total ===
    total = sum(scores.values())

    # Determine grade
    if total >= 80:
        grade = "A"
        label = "引用されやすい"
    elif total >= 65:
        grade = "B"
        label = "引用性が高い"
    elif total >= 50:
        grade = "C"
        label = "引用性が中程度"
    elif total >= 35:
        grade = "D"
        label = "引用性が低い"
    else:
        grade = "F"
        label = "引用性が不十分"

    preview = text[:150] + "..." if len(text) > 150 else text
    return {
        "heading": heading,
        "word_count": effective_word_count,
        "char_count": char_count,
        "is_japanese": is_ja,
        "total_score": total,
        "grade": grade,
        "label": label,
        "breakdown": scores,
        "preview": preview,
    }


def analyze_page_citability(url: str) -> dict:
    """Analyze all content blocks on a page for citability."""
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            },
            timeout=30,
        )
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch page: {str(e)}"}

    soup = BeautifulSoup(response.text, "lxml")

    # Remove non-content elements
    for element in soup.find_all(
        ["script", "style", "nav", "footer", "header", "aside", "form"]
    ):
        element.decompose()

    # Extract content blocks
    blocks = []
    current_heading = "Introduction"
    current_paragraphs = []

    for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "table"]):
        if element.name.startswith("h"):
            # Save previous section
            if current_paragraphs:
                combined = " ".join(current_paragraphs)
                if len(combined.split()) >= 20:
                    blocks.append(
                        {"heading": current_heading, "content": combined}
                    )
            current_heading = element.get_text(strip=True)
            current_paragraphs = []
        else:
            text = element.get_text(strip=True)
            # Accept text if it has 5+ words (English) or 10+ characters (Japanese)
            if text and (len(text.split()) >= 5 or len(text) >= 10):
                current_paragraphs.append(text)

    # Last block
    if current_paragraphs:
        combined = " ".join(current_paragraphs)
        # Accept block if 20+ words (English) or 40+ characters (Japanese)
        if len(combined.split()) >= 20 or len(combined) >= 40:
            blocks.append({"heading": current_heading, "content": combined})

    # Score each block
    scored_blocks = []
    for block in blocks:
        score = score_passage(block["content"], block["heading"])
        scored_blocks.append(score)

    # Calculate page-level metrics
    if scored_blocks:
        avg_score = sum(b["total_score"] for b in scored_blocks) / len(scored_blocks)
        top_blocks = sorted(scored_blocks, key=lambda x: x["total_score"], reverse=True)[:5]
        bottom_blocks = sorted(scored_blocks, key=lambda x: x["total_score"])[:5]

        # Optimal passage count (134-167 effective words; Japanese uses char_count//2)
        optimal_count = sum(
            1 for b in scored_blocks if 134 <= b["word_count"] <= 167
        )
    else:
        avg_score = 0
        top_blocks = []
        bottom_blocks = []
        optimal_count = 0

    # Grade distribution
    grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for block in scored_blocks:
        grade_dist[block["grade"]] += 1

    return {
        "url": url,
        "total_blocks_analyzed": len(scored_blocks),
        "average_citability_score": round(avg_score, 1),
        "optimal_length_passages": optimal_count,
        "grade_distribution": grade_dist,
        "top_5_citable": top_blocks,
        "bottom_5_citable": bottom_blocks,
        "all_blocks": scored_blocks,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用法：python citability_scorer.py <url>")
        print("すべてのコンテンツブロックの引用性分析を JSON で返します。")
        sys.exit(1)

    url = sys.argv[1]
    result = analyze_page_citability(url)
    print(json.dumps(result, indent=2, default=str))
