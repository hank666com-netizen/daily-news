#!/usr/bin/env python3
"""
Explorer News v4.0 - 自我学习版本
- 追踪来源质量
- 自动优化策略
- 学习成功/失败
- 持续进化
"""

import subprocess
import json
from datetime import datetime
import os
import re
from pathlib import Path

OUTPUT_DIR = os.path.expanduser("~/clawd/hank-second-brain/tech/exploration")
REPORT_FILE = f"{OUTPUT_DIR}/{datetime.now().strftime('%Y-%m-%d')}-news.md"
LEARNINGS_FILE = f"{OUTPUT_DIR}/learnings.json"

SEARCH_SCRIPT = os.path.expanduser("~/.agents/skills/search/scripts/search.sh")

def load_learnings():
    """加载学习数据"""
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE) as f:
            return json.load(f)
    return {
        "version": "1.0",
        "updated": datetime.now().isoformat(),
        "sources": {},
        "strategies": {
            "preferred_order": [],
            "blocked_sources": [],
            "auto_retry_failed": False
        },
        "metrics": {"total_runs": 0, "avg_news_per_run": 0, "avg_quality_score": 0}
    }

def save_learnings(data):
    """保存学习数据"""
    data["updated"] = datetime.now().isoformat()
    with open(LEARNINGS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_sources_from_learnings(learnings):
    """从学习数据中获取来源列表（按优先级排序）"""
    sources = {}
    blocked = learnings.get("strategies", {}).get("blocked_sources", [])
    
    for name, data in learnings.get("sources", {}).items():
        if name not in blocked:
            sources[name] = data
    
    # 按质量分数排序
    sorted_sources = sorted(sources.items(), key=lambda x: x[1].get("quality_score", 0), reverse=True)
    return [name for name, _ in sorted_sources]

def get_query(name):
    """根据来源名称生成查询"""
    queries = {
        "Reuters": "site:reuters.com latest news",
        "The Economist": "site:economist.com latest",
        "Product Hunt": "site:producthunt.com today",
        "GitHub Trending": "site:github.com trending today",
        "AP News": "site:apnews.com latest",
        # 自定义话题
        "OpenClaw": "OpenClaw agent automation AI",
        "Claude Code": "Claude Code AI coding assistant",
        "Silicon Valley": "Silicon Valley tech news startups",
        "Hacker News": "site:news.ycombinator.com front page",
        "DevNews": "software engineering programming news",
    }
    return queries.get(name, f"site:{name.lower()}.com latest news")

def get_custom_sources():
    """获取自定义话题来源"""
    return [
        {"name": "OpenClaw", "emoji": "🦞", "query": "OpenClaw agent automation workflow AI", "category": "🤖 OpenClaw"},
        {"name": "Claude Code", "emoji": "🤖", "query": "Claude Code AI coding assistant Anthropic", "category": "💻 Claude Code"},
        {"name": "Silicon Valley", "emoji": "🏙️", "query": "Silicon Valley tech startups AI funding news", "category": "🏙️ 硅谷新闻"},
        {"name": "Hacker News", "emoji": "🎯", "query": "site:news.ycombinator.com best", "category": "🎯 Hacker News"},
        {"name": "DevNews", "emoji": "👨‍💻", "query": "software engineering programming developer news", "category": "👨‍💻 程序员新闻"},
    ]

def tavily_search(query, max_results=5):
    cmd = [SEARCH_SCRIPT, json.dumps({
        "query": query, "topic": "news",
        "time_range": "day", "max_results": max_results,
        "include_raw_content": True
    })]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return json.loads(result.stdout) if result.returncode == 0 else None
    except:
        return None

def clean_text(text):
    if not text:
        return ""
    noise = ['provide news feedback', 'send a tip', 'limited-time offer',
             'subscribe to read', 'please enable js', "we've detected", 
             'test your news', 'election results']
    for n in noise:
        text = re.sub(n, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:350] + "..." if len(text) > 350 else text

def evaluate_source(name, news_list, data):
    """评估来源质量并更新学习数据"""
    if name not in data["sources"]:
        data["sources"][name] = {
            "success_rate": 0, "quality_score": 0, "content_clean": False,
            "avg_content_length": 0, "attempts": 0, "successes": 0,
            "last_success": None, "failure_reason": None
        }
    
    source = data["sources"][name]
    source["attempts"] += 1
    
    if news_list:
        source["successes"] += 1
        source["last_success"] = datetime.now().strftime('%Y-%m-%d')
        
        # 计算质量分数
        total_content = sum(len(n.get('content', '')) for n in news_list)
        avg_length = total_content / len(news_list)
        content_clean = all(len(n.get('content', '')) > 50 for n in news_list if n.get('content'))
        
        # 更新分数
        source["avg_content_length"] = avg_length
        source["content_clean"] = content_clean
        
        # 质量分数 = 成功率 × 内容质量 × 长度因子
        length_factor = min(avg_length / 300, 1.0)
        quality_factor = 0.9 if content_clean else 0.6
        source["quality_score"] = 1.0 * quality_factor * length_factor
        source["success_rate"] = source["successes"] / source["attempts"]
    else:
        source["failure_reason"] = "no_content"
    
    return source

def optimize_strategy(data):
    """根据学习结果优化策略"""
    # 更新优先顺序
    sorted_sources = sorted(
        [(n, d.get("quality_score", 0)) for n, d in data["sources"].items()],
        key=lambda x: x[1], reverse=True
    )
    data["strategies"]["preferred_order"] = [n for n, _ in sorted_sources if n not in data["strategies"].get("blocked_sources", [])]
    
    # 标记完全失败的来源
    blocked = []
    for name, source in data["sources"].items():
        if source.get("attempts", 0) >= 2 and source.get("success_rate", 0) == 0:
            blocked.append(name)
            source["failure_reason"] = "consistently_blocked"
    
    data["strategies"]["blocked_sources"] = blocked
    
    return data

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"📰 [Explorer v4.0] 自我学习探索开始...")
    
    # 加载学习数据
    learnings = load_learnings()
    learnings["metrics"]["total_runs"] += 1
    
    # 获取来源列表（按学习优先级）
    sources = get_sources_from_learnings(learnings)
    if not sources:
        sources = ["Reuters", "The Economist", "Product Hunt", "GitHub Trending", "AP News"]
    
    print(f"🧠 已学习 {len(sources)} 个来源，按质量排序")
    
    results = {}
    total_news = 0
    
    # 处理标准来源
    for name in sources:
        query = get_query(name)
        print(f"🔍 {name}...")
        
        data = tavily_search(query)
        news_list = []
        
        if data and 'results' in data:
            for r in data['results'][:5]:
                title = r.get('title', '').replace(' - Reuters', '').replace(' - The Economist', '')
                title = re.sub(r'\.com$', '', title)
                content = clean_text(r.get('content', '') or r.get('snippet', ''))
                if title and len(title) > 10:
                    news_list.append({'title': title.strip(), 'content': content})
        
        results[name] = news_list
        
        # 评估并学习
        evaluate_source(name, news_list, learnings)
        
        print(f"   → {len(news_list)} 条")
        total_news += len(news_list)
    
    # 处理自定义话题来源
    print(f"\n🔎 探索自定义话题...")
    custom_sources = get_custom_sources()
    custom_results = {}
    
    for source_info in custom_sources:
        name = source_info["name"]
        query = source_info["query"]
        category = source_info["category"]
        emoji = source_info["emoji"]
        
        print(f"🔍 {category}...")
        
        data = tavily_search(query)
        news_list = []
        
        if data and 'results' in data:
            for r in data['results'][:5]:
                title = r.get('title', '')
                content = clean_text(r.get('content', '') or r.get('snippet', ''))
                # 清理标题
                title = re.sub(r'\s*[-|]\s*(Reuters|Economist|News|Hacker News)$', '', title)
                title = re.sub(r'\.com$', '', title)
                title = re.sub(r'\|.*$', '', title)
                
                if title and len(title) > 10:
                    news_list.append({
                        'title': title.strip(),
                        'content': content,
                        'url': r.get('url', '')
                    })
        
        custom_results[category] = {
            'emoji': emoji,
            'news': news_list
        }
        
        print(f"   → {len(news_list)} 条")
        total_news += len(news_list)
    
    # 优化策略
    learnings = optimize_strategy(learnings)
    save_learnings(learnings)
    
    # 更新指标
    learnings["metrics"]["avg_news_per_run"] = (learnings["metrics"]["avg_news_per_run"] * (learnings["metrics"]["total_runs"] - 1) + total_news) / learnings["metrics"]["total_runs"]
    
    avg_quality = sum(d.get("quality_score", 0) for d in learnings["sources"].values()) / len(learnings["sources"]) if learnings["sources"] else 0
    learnings["metrics"]["avg_quality_score"] = avg_quality
    save_learnings(learnings)
    
    # 生成报告
    report = f"""# 每日新闻探索报告 | {today}

## 📊 概览

- **探索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **数据来源**: Tavily Search + Self-Learning + Custom Topics
- **自我进化**: v4.0 + Custom Topics
- **新增话题**: OpenClaw, Claude Code, 硅谷新闻, 程序员新闻

---

"""
    
    # 标准来源
    emojis = {"Reuters": "🇬🇧", "The Economist": "🇬🇧", "Product Hunt": "🚀",
              "GitHub Trending": "💻", "AP News": "🇺🇸"}
    
    for name in sources:
        if name not in emojis:
            emojis[name] = "📰"
    
    for name in sources:
        news = results.get(name, [])
        if not news:
            continue
        report += f"## {emojis.get(name, '📰')} {name}\n\n"
        for i, item in enumerate(news, 1):
            report += f"{i}. **{item['title']}**\n"
            if item.get('content'):
                report += f"   📝 {item['content']}\n"
            report += "\n"
    
    # 自定义话题
    report += "\n---\n\n## 🎯 自定义话题\n\n"
    
    for category, data in custom_results.items():
        if not data['news']:
            continue
        report += f"### {data['emoji']} {category}\n\n"
        for i, item in enumerate(data['news'][:5], 1):
            report += f"{i}. **{item['title']}**\n"
            if item.get('content'):
                report += f"   📝 {item['content']}\n"
            if item.get('url'):
                report += f"   🔗 [链接]({item['url']})\n"
            report += "\n"
    
    report += f"""---

**总新闻数**: {total_news} 条 | **标准来源**: {len(sources)} | **自定义话题**: {len(custom_sources)}
**平均质量**: {avg_quality:.2f} | **运行次数**: {learnings['metrics']['total_runs']}
**学习时间**: {learnings['updated']}
**下次探索**: 明天 08:15
"""
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"\n✅ 完成！报告: {REPORT_FILE}")
    print(f"🧠 学习数据已更新")

if __name__ == "__main__":
    main()
