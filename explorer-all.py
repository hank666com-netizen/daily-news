#!/usr/bin/env python3
"""
Explorer All-in-One v1.0 - 整合所有探索任务
- GitHub AI Agents
- 新闻 + 自定义话题
- 社交媒体 (Reddit + X)
"""

import subprocess
import json
from datetime import datetime
import os
import re
from pathlib import Path

OUTPUT_DIR = os.path.expanduser("~/clawd/hank-second-brain/tech/exploration")
REPORT_FILE = f"{OUTPUT_DIR}/{datetime.now().strftime('%Y-%m-%d')}-explorer.md"
GITHUB_FILE = f"{OUTPUT_DIR}/{datetime.now().strftime('%Y-%m-%d')}-github-agents.md"
SOCIAL_FILE = f"{OUTPUT_DIR}/{datetime.now().strftime('%Y-%m-%d')}-social.md"
LEARNINGS_NEWS = f"{OUTPUT_DIR}/learnings.json"
LEARNINGS_SOCIAL = f"{OUTPUT_DIR}/learnings-social.json"

SEARCH_SCRIPT = os.path.expanduser("~/.agents/skills/search/scripts/search.sh")

def tavily_search(query, max_results=8, topic="news"):
    """Tavily 搜索"""
    cmd = [SEARCH_SCRIPT, json.dumps({
        "query": query,
        "topic": topic,
        "time_range": "day",
        "max_results": max_results,
        "include_raw_content": True
    })]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception as e:
        print(f"   ⚠️ 搜索错误: {e}")
        return None

def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    noise = ['provide news feedback', 'send a tip', 'limited-time offer',
             'subscribe to read', 'please enable js', "we've detected", 
             'test your news', 'election results']
    for n in noise:
        text = re.sub(n, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:300] + "..." if len(text) > 300 else text

def explore_github():
    """探索 GitHub AI Agents"""
    print(f"\n📦 === GitHub AI Agents 探索 ===")
    
    topics = [
        ("AI Agents", "site:github.com trending AI agent autonomous"),
        ("Langflow/RAG", "site:github.com Langflow RAG multi-agent"),
        ("Self-improving", "site:github.com self-improving autonomous agent"),
        ("OpenClaw", "site:github.com OpenClaw agent automation"),
        ("Memory Systems", "site:github.com vector database semantic memory RAG"),
    ]
    
    results = {}
    for name, query in topics:
        print(f"🔍 {name}...")
        data = tavily_search(query)
        items = []
        if data and 'results' in data:
            for r in data['results'][:8]:
                title = r.get('title', '')
                content = clean_text(r.get('content', '') or r.get('snippet', ''))
                if title and len(title) > 10:
                    items.append({'title': title.strip(), 'content': content})
        results[name] = items
        print(f"   → {len(items)} 条")
    
    # 生成 GitHub 报告
    report = f"# GitHub AI Agents 探索报告 | {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += f"**探索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n"
    
    for name, items in results.items():
        report += f"## 🔗 {name}\n\n"
        for i, item in enumerate(items[:10], 1):
            report += f"{i}. **{item['title']}**\n"
            if item.get('content'):
                report += f"   📝 {item['content']}\n"
            report += "\n"
    
    with open(GITHUB_FILE, 'w') as f:
        f.write(report)
    
    print(f"\n✅ GitHub 报告: {GITHUB_FILE}")
    return results

def explore_news():
    """探索新闻 + 自定义话题"""
    print(f"\n📰 === 新闻探索 ===")
    
    # 标准来源
    standard_sources = [
        ("Reuters", "🇬🇧", "site:reuters.com latest news"),
        ("Bloomberg", "💰", "site:bloomberg.com latest"),
        ("WSJ", "📈", "site:wsj.com latest"),
        ("AP News", "🇺🇸", "site:apnews.com latest"),
        ("The Economist", "🇬🇧", "site:economist.com latest"),
        ("Product Hunt", "🚀", "site:producthunt.com today"),
        ("GitHub Trending", "💻", "site:github.com trending today"),
    ]
    
    # 自定义话题
    custom_sources = [
        ("OpenClaw", "🦞", "OpenClaw agent automation workflow AI"),
        ("Claude Code", "🤖", "Claude Code AI coding assistant Anthropic"),
        ("Silicon Valley", "🏙️", "Silicon Valley tech startups AI funding news"),
        ("Hacker News", "🎯", "site:news.ycombinator.com best"),
        ("DevNews", "👨‍💻", "software engineering programming developer news"),
    ]
    
    results = {}
    
    for name, emoji, query in standard_sources + custom_sources:
        category = f"{emoji} {name}"
        print(f"🔍 {category}...")
        data = tavily_search(query)
        items = []
        if data and 'results' in data:
            for r in data['results'][:5]:
                title = r.get('title', '')
                title = re.sub(r'\s*[-|]\s*(Reuters|Economist|News|Hacker News)$', '', title)
                title = re.sub(r'\.com$', '', title)
                content = clean_text(r.get('content', '') or r.get('snippet', ''))
                url = r.get('url', '')
                if title and len(title) > 10:
                    items.append({'title': title.strip(), 'content': content, 'url': url})
        results[category] = items
        print(f"   → {len(items)} 条")
    
    return results

def explore_social():
    """探索社交媒体"""
    print(f"\n🐦💬 === 社交媒体探索 ===")
    
    sources = [
        ("Reddit r/MachineLearning", "💬", "site:reddit.com/r/MachineLearning artificial intelligence"),
        ("Reddit r/LocalLLaMA", "💬", "site:reddit.com/r/LocalLLaMA local models Ollama"),
        ("X AI Discussions", "🐦", "site:x.com OR site:twitter.com AI artificial intelligence"),
    ]
    
    results = {}
    for name, emoji, query in sources:
        category = f"{emoji} {name}"
        print(f"🔍 {category}...")
        data = tavily_search(query)
        items = []
        if data and 'results' in data:
            for r in data['results'][:8]:
                title = r.get('title', '')
                title = re.sub(r'\s*[-|]\s*(reddit|x|twitter)$', '', title)
                content = clean_text(r.get('content', '') or r.get('snippet', ''))
                url = r.get('url', '')
                if title and len(title) > 10:
                    items.append({'title': title.strip(), 'content': content, 'url': url})
        results[category] = items
        print(f"   → {len(items)} 条")
    
    return results

def generate_combined_report(github, news, social):
    """生成整合报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 统计
    total_github = sum(len(v) for v in github.values())
    total_news = sum(len(v) for v in news.values())
    total_social = sum(len(v) for v in social.values())
    total = total_github + total_news + total_social
    
    report = f"""# 📊 Explorer 一体化探索报告 | {today}

## 📊 概览

- **探索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **版本**: v1.0 (All-in-One)
- **数据来源**: Tavily Search

---

## 📦 GitHub AI Agents ({total_github} 条)

"""
    
    for name, items in github.items():
        if not items:
            continue
        report += f"### 🔗 {name}\n\n"
        for i, item in enumerate(items[:5], 1):
            report += f"{i}. **{item['title']}**\n"
            if item.get('content'):
                report += f"   📝 {item['content']}\n"
            report += "\n"
    
    report += f"""
---

## 📰 新闻 + 自定义话题 ({total_news} 条)

"""
    
    # 标准来源
    report += "### 🏛️ 主流媒体\n\n"
    for name in ["Reuters", "Bloomberg", "WSJ", "AP News", "The Economist"]:
        key = f"{'🇬🇧' if name in ['Reuters', 'The Economist'] else '💰' if name == 'Bloomberg' else '🇺🇸' if name == 'AP News' else '📈'} {name}"
        if key in news and news[key]:
            report += f"**{name}**\n"
            for i, item in enumerate(news[key][:3], 1):
                report += f"{i}. {item['title']}\n"
            report += "\n"
    
    report += "### 🎯 自定义话题\n\n"
    for name in ["OpenClaw", "Claude Code", "Silicon Valley", "Hacker News", "DevNews"]:
        emoji = "🦞🤖🏙️🎯👨‍💻"[["OpenClaw", "Claude Code", "Silicon Valley", "Hacker News", "DevNews"].index(name)]
        key = f"{emoji} {name}"
        if key in news and news[key]:
            report += f"**{name}**\n"
            for i, item in enumerate(news[key][:3], 1):
                report += f"{i}. {item['title']}\n"
            report += "\n"
    
    report += f"""
---

## 🐦💬 社交媒体 ({total_social} 条)

"""
    
    for category, items in social.items():
        if not items:
            continue
        report += f"### {category}\n\n"
        for i, item in enumerate(items[:5], 1):
            report += f"{i}. **{item['title']}**\n"
            if item.get('url'):
                report += f"   🔗 [链接]({item['url']})\n"
            report += "\n"
    
    report += f"""---

## 📈 统计

| 类型 | 数量 |
|------|------|
| GitHub AI Agents | {total_github} 条 |
| 新闻 + 话题 | {total_news} 条 |
| 社交媒体 | {total_social} 条 |
| **总计** | **{total} 条** |

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**下次探索**: 明天 08:30
"""
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"\n✅ 整合报告: {REPORT_FILE}")

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🚀 [Explorer All-in-One v1.0] 开始探索... | {today}")
    
    # 1. GitHub 探索
    github_results = explore_github()
    
    # 2. 新闻探索
    news_results = explore_news()
    
    # 3. 社交媒体探索
    social_results = explore_social()
    
    # 生成整合报告
    generate_combined_report(github_results, news_results, social_results)
    
    print(f"\n{'='*50}")
    print(f"✅ 探索完成！")
    print(f"📦 GitHub: {GITHUB_FILE}")
    print(f"🐦💬 Social: {SOCIAL_FILE}")
    print(f"📊 整合: {REPORT_FILE}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
