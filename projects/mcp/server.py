#!/usr/bin/env python3
"""
人生OS MCPサーバー - Phase 3
Resources: 22本 / Tools: 12本 / Prompts: 5本
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    Prompt,
    TextContent,
    PromptMessage,
    GetPromptResult,
)

# ---------------------------------------------------------------------------
# パス設定
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent.parent  # リポジトリルート
SELF_DIR = BASE_DIR / "self"
INVESTMENT_DIR = BASE_DIR / "investment"
SNS_DIR = BASE_DIR / "sns"
CLAUDE_MD = BASE_DIR / "CLAUDE.md"

app = Server("life-os")

# ===========================================================================
# RESOURCES（22本）
# ===========================================================================

@app.list_resources()
async def list_resources():
    return [
        Resource(uri="life-os://core/claude-md",          name="CLAUDE.md",              description="Claudeへの指示・人生OS設定"),
        Resource(uri="life-os://self/values",              name="values.md",              description="価値観・人生原則"),
        Resource(uri="life-os://self/money-os",            name="money_os.md",            description="マネーOS・家計方針"),
        Resource(uri="life-os://self/career-os",           name="career_os.md",           description="キャリアOS・仕事方針"),
        Resource(uri="life-os://self/fire-scenarios",      name="fire_scenarios.md",      description="FIREシナリオ試算"),
        Resource(uri="life-os://self/tax-strategy",        name="tax_strategy.md",        description="節税戦略"),
        Resource(uri="life-os://self/post-fire-lifestyle", name="post_fire_lifestyle.md", description="FIRE後のライフスタイル設計"),
        Resource(uri="life-os://self/life-vision",         name="life_vision.md",         description="人生ビジョン"),
        Resource(uri="life-os://self/parenting-os",        name="parenting_os.md",        description="子育てOS"),
        Resource(uri="life-os://self/life-story",          name="life_story.md",          description="人生ストーリー・自分史"),
        Resource(uri="life-os://self/relationships",       name="relationships.md",       description="人間関係マップ"),
        Resource(uri="life-os://investment/strategy",      name="strategy.md",            description="投資戦略"),
        Resource(uri="life-os://investment/holdings",      name="holdings.json",          description="保有資産一覧"),
        Resource(uri="life-os://investment/watchlist",     name="watchlist.md",           description="ウォッチリスト"),
        Resource(uri="life-os://investment/trades",        name="trades.md",              description="売買履歴"),
        Resource(uri="life-os://investment/recent-signals",name="recent_signals.md",      description="直近シグナル"),
        Resource(uri="life-os://sns/persona",              name="persona_prompt.md",      description="SNSペルソナ設定"),
        Resource(uri="life-os://sns/core-beliefs",         name="core_beliefs.md",        description="コアビリーフ"),
        Resource(uri="life-os://sns/mastermind",           name="mastermind.md",          description="マスターマインドノート"),
        Resource(uri="life-os://sns/content-queue",        name="content_queue.md",       description="投稿キュー"),
        Resource(uri="life-os://sns/posted-log",           name="posted_log.md",          description="投稿済みログ"),
        Resource(uri="life-os://sns/coast-fire-plan",      name="coast_fire_plan.md",     description="CoastFIRE計画"),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    mapping = {
        "life-os://core/claude-md":           CLAUDE_MD,
        "life-os://self/values":              SELF_DIR / "values.md",
        "life-os://self/money-os":            SELF_DIR / "money_os.md",
        "life-os://self/career-os":           SELF_DIR / "career_os.md",
        "life-os://self/fire-scenarios":      SELF_DIR / "fire_scenarios.md",
        "life-os://self/tax-strategy":        SELF_DIR / "tax_strategy.md",
        "life-os://self/post-fire-lifestyle": SELF_DIR / "post_fire_lifestyle.md",
        "life-os://self/life-vision":         SELF_DIR / "life_vision.md",
        "life-os://self/parenting-os":        SELF_DIR / "parenting_os.md",
        "life-os://self/life-story":          SELF_DIR / "life_story.md",
        "life-os://self/relationships":       SELF_DIR / "relationships.md",
        "life-os://investment/strategy":      INVESTMENT_DIR / "strategy.md",
        "life-os://investment/holdings":      INVESTMENT_DIR / "holdings.json",
        "life-os://investment/watchlist":     INVESTMENT_DIR / "watchlist.md",
        "life-os://investment/trades":        INVESTMENT_DIR / "trades.md",
        "life-os://investment/recent-signals":INVESTMENT_DIR / "recent_signals.md",
        "life-os://sns/persona":              SNS_DIR / "persona_prompt.md",
        "life-os://sns/core-beliefs":         SNS_DIR / "core_beliefs.md",
        "life-os://sns/mastermind":           SNS_DIR / "mastermind.md",
        "life-os://sns/content-queue":        SNS_DIR / "content_queue.md",
        "life-os://sns/posted-log":           SNS_DIR / "posted_log.md",
        "life-os://sns/coast-fire-plan":      SNS_DIR / "coast_fire_plan.md",
    }
    path = mapping.get(uri)
    if path is None:
        return f"Unknown resource: {uri}"
    if not path.exists():
        return f"File not found: {path}"
    return path.read_text(encoding="utf-8")


# ===========================================================================
# TOOLS（12本）
# ===========================================================================

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_market_snapshot":
        return await get_market_snapshot()
    elif name == "get_asset_snapshot":
        return await get_asset_snapshot()
    elif name == "update_asset_snapshot":
        return await update_asset_snapshot(**arguments)
    elif name == "get_fire_status":
        return await get_fire_status()
    elif name == "record_trade":
        return await record_trade(**arguments)
    elif name == "generate_monthly_review":
        return await generate_monthly_review()
    elif name == "post_tweet":
        return await post_tweet(**arguments)
    elif name == "add_to_content_queue":
        return await add_to_content_queue(**arguments)
    elif name == "get_queue_count":
        return await get_queue_count()
    elif name == "git_push_changes":
        return await git_push_changes(**arguments)
    elif name == "batch_generate_tweets":
        return await batch_generate_tweets(**arguments)
    elif name == "get_sns_analytics":
        return await get_sns_analytics()
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_market_snapshot",
            description="現在の市場スナップショットを取得する（主要指数・為替）",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="get_asset_snapshot",
            description="現在の資産スナップショットをholdings.jsonから取得する",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="update_asset_snapshot",
            description="資産スナップショットをholdings.jsonに更新する",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "更新する資産データ（JSON）"},
                },
                "required": ["data"],
            },
        ),
        Tool(
            name="get_fire_status",
            description="現在のFIRE達成状況を取得する（進捗率・残年数など）",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="record_trade",
            description="売買記録をtrades.mdに追記する",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker":   {"type": "string",  "description": "ティッカーシンボル"},
                    "action":   {"type": "string",  "description": "buy / sell"},
                    "quantity": {"type": "number",  "description": "数量"},
                    "price":    {"type": "number",  "description": "価格"},
                    "note":     {"type": "string",  "description": "メモ"},
                },
                "required": ["ticker", "action", "quantity", "price"],
            },
        ),
        Tool(
            name="generate_monthly_review",
            description="当月の振り返りMarkdownを生成する（保存はしない）",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="post_tweet",
            description="ツイートをposted_log.mdに記録する（実際の投稿はユーザーが行う）",
            inputSchema={
                "type": "object",
                "properties": {
                    "text":  {"type": "string", "description": "ツイート本文"},
                    "theme": {"type": "string", "description": "テーマ（任意）"},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="add_to_content_queue",
            description="コンテンツをcontent_queue.mdに追加する",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "追加するコンテンツ"},
                    "theme":   {"type": "string", "description": "テーマ（任意）"},
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="get_queue_count",
            description="content_queue.mdの現在のキュー件数を返す",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="git_push_changes",
            description="変更をgit add / commit / pushする",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "コミットメッセージ"},
                    "files":   {"type": "array",  "items": {"type": "string"}, "description": "対象ファイルリスト（省略時は全変更）"},
                },
                "required": ["message"],
            },
        ),
        # ── Phase 3 追加 ────────────────────────────────────────────────
        Tool(
            name="batch_generate_tweets",
            description="n本のツイート案生成を依頼するプロンプト文字列を返す（Claude APIは呼ばない）",
            inputSchema={
                "type": "object",
                "properties": {
                    "n":     {"type": "integer", "description": "生成するツイート数（デフォルト7）"},
                    "theme": {"type": "string",  "description": "テーマ（省略時はFIRE/マネー教育/父親哲学の3軸均等）"},
                },
                "required": [],
            },
        ),
        Tool(
            name="get_sns_analytics",
            description="posted_log.mdを読んで直近30日の投稿統計をMarkdown表で返す",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


# ---------------------------------------------------------------------------
# Tool 実装
# ---------------------------------------------------------------------------

async def get_market_snapshot() -> list[TextContent]:
    """主要指数・為替のスナップショット（プレースホルダー）"""
    return [TextContent(type="text", text=(
        "## 市場スナップショット\n\n"
        "- S&P500: （要更新）\n"
        "- NASDAQ: （要更新）\n"
        "- 日経225: （要更新）\n"
        "- USD/JPY: （要更新）\n\n"
        "*実際の値は証券会社APIや Yahoo Finance から取得してください。*"
    ))]


async def get_asset_snapshot() -> list[TextContent]:
    path = INVESTMENT_DIR / "holdings.json"
    if not path.exists():
        return [TextContent(type="text", text="holdings.json が存在しません。")]
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = ["## 資産スナップショット\n"]
    for k, v in data.items():
        lines.append(f"- **{k}**: {v}")
    return [TextContent(type="text", text="\n".join(lines))]


async def update_asset_snapshot(data: dict) -> list[TextContent]:
    path = INVESTMENT_DIR / "holdings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
    existing.update(data)
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return [TextContent(type="text", text="holdings.json を更新しました。")]


async def get_fire_status() -> list[TextContent]:
    path = SELF_DIR / "fire_scenarios.md"
    if not path.exists():
        return [TextContent(type="text", text="fire_scenarios.md が存在しません。")]
    content = path.read_text(encoding="utf-8")
    return [TextContent(type="text", text=f"## FIRE状況\n\n{content[:500]}\n\n*(詳細は fire_scenarios.md を参照)*")]


async def record_trade(ticker: str, action: str, quantity: float, price: float, note: str = "") -> list[TextContent]:
    path = INVESTMENT_DIR / "trades.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"| {today} | {ticker} | {action} | {quantity} | {price} | {note} |\n"
    if not path.exists():
        header = "| 日付 | ティッカー | 売買 | 数量 | 価格 | メモ |\n|------|-----------|------|------|------|------|\n"
        path.write_text(header + entry, encoding="utf-8")
    else:
        with path.open("a", encoding="utf-8") as f:
            f.write(entry)
    return [TextContent(type="text", text=f"取引を記録しました: {today} {action} {ticker} x{quantity} @{price}")]


async def generate_monthly_review() -> list[TextContent]:
    now = datetime.now()
    return [TextContent(type="text", text=(
        f"## {now.year}年{now.month}月 月次レビュー\n\n"
        "### 資産推移\n（holdings.jsonを参照）\n\n"
        "### 売買記録\n（trades.mdを参照）\n\n"
        "### FIRE進捗\n（fire_scenarios.mdを参照）\n\n"
        "### 振り返り\n- 良かった点:\n- 改善点:\n- 来月の目標:\n"
    ))]


async def post_tweet(text: str, theme: str = "") -> list[TextContent]:
    return await add_to_content_queue(content=text, theme=theme, posted=True)


async def add_to_content_queue(content: str, theme: str = "", posted: bool = False) -> list[TextContent]:
    if posted:
        path = SNS_DIR / "posted_log.md"
        label = "投稿済みログ"
    else:
        path = SNS_DIR / "content_queue.md"
        label = "コンテンツキュー"
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n---\n**{now}** [{theme or 'general'}]\n\n{content}\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
    return [TextContent(type="text", text=f"{label}に追加しました。")]


async def get_queue_count() -> list[TextContent]:
    path = SNS_DIR / "content_queue.md"
    if not path.exists():
        return [TextContent(type="text", text="キューは空です（0件）")]
    content = path.read_text(encoding="utf-8")
    count = content.count("\n---\n")
    return [TextContent(type="text", text=f"キュー件数: {count}件")]


async def git_push_changes(message: str, files: list[str] | None = None) -> list[TextContent]:
    try:
        cwd = str(BASE_DIR)
        if files:
            subprocess.run(["git", "add"] + files, cwd=cwd, check=True, capture_output=True)
        else:
            subprocess.run(["git", "add", "-A"], cwd=cwd, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], cwd=cwd, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=cwd, check=True, capture_output=True)
        return [TextContent(type="text", text=f"git push 完了: {message}")]
    except subprocess.CalledProcessError as e:
        return [TextContent(type="text", text=f"git エラー: {e.stderr.decode() if e.stderr else str(e)}")]


# ── Phase 3 追加 Tools ─────────────────────────────────────────────────────

async def batch_generate_tweets(n: int = 7, theme: str = "") -> list[TextContent]:
    """
    n本のツイート案生成を依頼するプロンプト文字列を返す。
    Claude APIは呼ばない。MCPクライアント（Claude Desktop）が実際の生成を担う。
    """
    # 参照ファイルの読み込み
    persona_path = SNS_DIR / "persona_prompt.md"
    life_story_path = SELF_DIR / "life_story.md"
    holdings_path = INVESTMENT_DIR / "holdings.json"
    posted_log_path = SNS_DIR / "posted_log.md"

    persona = persona_path.read_text(encoding="utf-8") if persona_path.exists() else "（ペルソナ未設定）"
    life_story = life_story_path.read_text(encoding="utf-8") if life_story_path.exists() else "（人生ストーリー未設定）"
    holdings_raw = holdings_path.read_text(encoding="utf-8") if holdings_path.exists() else "{}"
    posted_log = posted_log_path.read_text(encoding="utf-8") if posted_log_path.exists() else "（投稿履歴なし）"

    # テーマ指示の構築
    if theme:
        theme_instruction = f'テーマ「{theme}」に沿ったツイートを{n}本生成してください。'
    else:
        each = max(1, n // 3)
        remainder = n - each * 3
        theme_instruction = (
            f"以下の3軸を均等に含めて合計{n}本のツイートを生成してください：\n"
            f"  1. FIRE（経済的自立・早期退職）: {each}本\n"
            f"  2. マネー教育（資産形成・投資入門）: {each}本\n"
            f"  3. 父親哲学（子育て・家族・人生観）: {each + remainder}本"
        )

    prompt = (
        "# ツイート一括生成プロンプト\n\n"
        "## あなたのペルソナ\n"
        f"{persona}\n\n"
        "## 人生ストーリー\n"
        f"{life_story[:800]}\n\n"
        "## 現在の保有資産\n"
        f"{holdings_raw[:400]}\n\n"
        "## 直近の投稿済みツイート（重複を避けるために参照）\n"
        f"{posted_log[-1200:] if len(posted_log) > 1200 else posted_log}\n\n"
        "---\n\n"
        "## 生成指示\n"
        f"{theme_instruction}\n\n"
        "### 制約\n"
        "- 1ツイート140字以内（日本語）\n"
        "- 実体験・数字・具体的エピソードを盛り込む\n"
        "- ハッシュタグは各ツイート末尾に1〜2個（#FIRE #子育て #マネー教育 などから選択）\n"
        "- 過去の投稿と重複しない内容にする\n"
        "- 全ツイートを番号付きリストで出力する\n\n"
        "### 生成後のアクション\n"
        "生成したツイート案を確認したら、採用したいものについて\n"
        "`add_to_content_queue(content=\"<ツイート本文>\", theme=\"<テーマ>\")`\n"
        "を呼び出してキューに追加してください。\n"
    )
    return [TextContent(type="text", text=prompt)]


async def get_sns_analytics() -> list[TextContent]:
    """
    posted_log.mdを読んで直近30日の投稿統計をMarkdown表で返す。
    """
    import re
    path = SNS_DIR / "posted_log.md"
    if not path.exists():
        return [TextContent(type="text", text="投稿履歴なし")]

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return [TextContent(type="text", text="投稿履歴なし")]

    thirty_days_ago = datetime.now() - timedelta(days=30)

    entry_pattern = re.compile(
        r"\*\*(?P<dt>\d{4}-\d{2}-\d{2} \d{2}:\d{2})\*\* \[(?P<theme>[^\]]+)\]"
    )

    posts = []
    for m in entry_pattern.finditer(content):
        try:
            dt = datetime.strptime(m.group("dt"), "%Y-%m-%d %H:%M")
            if dt >= thirty_days_ago:
                posts.append({"dt": dt, "theme": m.group("theme")})
        except ValueError:
            continue

    total = len(posts)
    if total == 0:
        return [TextContent(type="text", text="直近30日の投稿はありません。")]

    weekday_names = ["月", "火", "水", "木", "金", "土", "日"]
    weekday_counts = {d: 0 for d in weekday_names}
    for p in posts:
        weekday_counts[weekday_names[p["dt"].weekday()]] += 1

    theme_counts: dict[str, int] = {}
    for p in posts:
        t = p["theme"]
        theme_counts[t] = theme_counts.get(t, 0) + 1

    output_lines = [
        "## SNS投稿統計（直近30日）\n",
        f"**総投稿数**: {total}本\n",
        "### 曜日別分布\n",
        "| 曜日 | 投稿数 |",
        "|------|--------|"
    ]
    for day, count in weekday_counts.items():
        bar = "█" * count
        output_lines.append(f"| {day}曜日 | {count} {bar} |")

    output_lines += [
        "\n### テーマ別比率\n",
        "| テーマ | 投稿数 | 比率 |",
        "|--------|--------|------|"
    ]
    for theme_name, count in sorted(theme_counts.items(), key=lambda x: -x[1]):
        ratio = f"{count / total * 100:.1f}%"
        output_lines.append(f"| {theme_name} | {count} | {ratio} |")

    return [TextContent(type="text", text="\n".join(output_lines))]


# ===========================================================================
# PROMPTS（5本）
# ===========================================================================

@app.list_prompts()
async def list_prompts():
    return [
        Prompt(name="monthly_review_prompt",  description="月次レビュープロンプトを生成する"),
        Prompt(name="fire_check_prompt",       description="FIRE進捗チェックプロンプトを生成する"),
        Prompt(name="weekly_batch_prompt",     description="週次ツイート一括生成の手順プロンプト"),
        Prompt(name="market_tweet_prompt",     description="市場連動ツイート生成の手順プロンプト"),
        Prompt(name="note_article_prompt",     description="note記事骨格生成の手順プロンプト"),
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None = None) -> GetPromptResult:
    if name == "monthly_review_prompt":
        return await monthly_review_prompt()
    elif name == "fire_check_prompt":
        return await fire_check_prompt()
    elif name == "weekly_batch_prompt":
        return await weekly_batch_prompt()
    elif name == "market_tweet_prompt":
        return await market_tweet_prompt()
    elif name == "note_article_prompt":
        return await note_article_prompt()
    else:
        return GetPromptResult(messages=[
            PromptMessage(role="user", content=TextContent(type="text", text=f"Unknown prompt: {name}"))
        ])


# ---------------------------------------------------------------------------
# Prompt 実装
# ---------------------------------------------------------------------------

async def monthly_review_prompt() -> GetPromptResult:
    now = datetime.now()
    text = (
        f"# {now.year}年{now.month}月 月次レビュー生成手順\n\n"
        "以下の順番でツールを呼び出し、月次レビューを作成してください。\n\n"
        "1. `get_asset_snapshot()` を呼び出して現在の資産状況を取得する\n"
        "2. `get_fire_status()` を呼び出してFIRE進捗を確認する\n"
        "3. `get_market_snapshot()` を呼び出して市場状況を確認する\n"
        "4. 上記の情報をもとに `generate_monthly_review()` を呼び出してレビューを生成する\n"
        "5. 生成されたレビューの内容を確認・編集する\n"
        f"6. `git_push_changes(message=\"{now.year}-{now.month:02d} monthly review\")` でコミットする\n"
    )
    return GetPromptResult(messages=[
        PromptMessage(role="user", content=TextContent(type="text", text=text))
    ])


async def fire_check_prompt() -> GetPromptResult:
    text = (
        "# FIRE進捗チェック手順\n\n"
        "以下の順番でツールを呼び出し、FIRE達成状況を確認してください。\n\n"
        "1. `get_fire_status()` を呼び出してFIRE進捗を取得する\n"
        "2. `get_asset_snapshot()` を呼び出して現在の資産を確認する\n"
        "3. `get_market_snapshot()` を呼び出して最新の市場状況を確認する\n"
        "4. 取得した情報をもとに以下を分析する:\n"
        "   - FIRE目標額までの残額と達成率\n"
        "   - 現在のペースでの達成予定時期\n"
        "   - 市場環境を考慮したシナリオ分岐（楽観・中立・悲観）\n"
        "5. 必要に応じてfire_scenarios.mdを更新する\n"
    )
    return GetPromptResult(messages=[
        PromptMessage(role="user", content=TextContent(type="text", text=text))
    ])


# ── Phase 3 追加 Prompts ───────────────────────────────────────────────────

async def weekly_batch_prompt() -> GetPromptResult:
    text = (
        "# 週次ツイート一括生成 手順\n\n"
        "毎週のツイート7本をまとめて準備するワークフローです。\n\n"
        "## ステップ\n\n"
        "**Step 1: ツイート案の生成**\n"
        "以下のツールを呼び出します:\n"
        "`batch_generate_tweets(n=7)`\n"
        "返ってきたプロンプト文字列の指示に従い、7本のツイート案を生成してください。\n\n"
        "**Step 2: ツイート案のレビュー**\n"
        "- 生成された各ツイートが140字以内か確認する\n"
        "- 内容の重複・ハッシュタグの適切さを確認する\n"
        "- 必要に応じて内容を微調整する\n\n"
        "**Step 3: キューへの追加**\n"
        "採用するツイートごとに以下を呼び出します:\n"
        "`add_to_content_queue(content=\"<ツイート本文>\", theme=\"<FIRE|マネー教育|父親哲学>\")`\n\n"
        "**Step 4: キュー確認**\n"
        "`get_queue_count()`\n"
        "7本がキューに入っていることを確認する。\n\n"
        "**Step 5: コミット**\n"
        "`git_push_changes(message=\"sns: add weekly tweet batch\")`\n"
    )
    return GetPromptResult(messages=[
        PromptMessage(role="user", content=TextContent(type="text", text=text))
    ])


async def market_tweet_prompt() -> GetPromptResult:
    text = (
        "# 市場連動ツイート生成 手順\n\n"
        "今日の市場状況に連動したタイムリーなツイートを1本生成するワークフローです。\n\n"
        "## ステップ\n\n"
        "**Step 1: 市場・資産データの取得**\n"
        "`get_market_snapshot()`\n"
        "`get_fire_status()`\n\n"
        "**Step 2: ツイート生成**\n"
        "取得した以下の情報を使って、今日の市場状況に連動したツイートを1本生成してください:\n"
        "- 主要指数の動き（上昇/下落率）\n"
        "- 自分のFIRE進捗への影響（ポジティブ/ネガティブな変化）\n"
        "- 長期投資家としての感想・学び\n\n"
        "ツイート生成の指針:\n"
        "- 相場の一時的な動きに一喜一憂せず、長期視点を伝える\n"
        "- 具体的な数字を含める（例: 含み益が◯万円増えた）\n"
        "- 読者が行動できるアドバイスや問いかけを末尾に入れる\n"
        "- 140字以内、ハッシュタグ1〜2個\n\n"
        "**Step 3: 投稿・記録**\n"
