#!/usr/bin/env python3
"""
Explorer Social v1.0 - 探索 Reddit 和 X 的热门 AI 话题
- Reddit: r/MachineLearning, r/ArtificialIntelligence, r/LocalLLaMA
- X: AI 相关热门讨论
"""

import subprocess
import json
from datetime import datetime
import os
import re
from pathlib import Path

OUTPUT_DIR = os.path.expanduser("~/clawd/hank-second-brain/tech/exploration")
REPORT_FILE = f"{OUTPUT_DIR}/{datetime.now().strftime('%Y-%m-%d')}-social.md"
LEARNINGS_FILE = f"{OUTPUT_DIR}/learnings-social.json"

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
        "metrics": {"total_runs": 0, "avg_posts_per_run": 0}
    }

def save_learnings(data):
    """保存学习数据"""
    data["updated"] = datetime.now().isoformat()
    with open(LEARNINGS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_social_sources():
    """获取社交媒体来源列表"""
    return [
        {
            "name": "Reddit r/MachineLearning",
            "query": "site:reddit.com/r/MachineLearning artificial intelligence machine learning",
            "category": "💬 Reddit"
        },
        {
            "name": "Reddit r/ArtificialIntelligence", 
            "query": "site:reddit.com/r/ArtificialIntelligence AI LLMs agents",
            "category": "💬 Reddit"
        },
        {
            "name": "Reddit r/LocalLLaMA",
            "query": "site:reddit.com/r/LocalLLaMA local models Ollama LM Studio",
            "category": "💬 Reddit"
        },
        {
            "name": "X AI Discussions",
            "query": "site:x.com OR site:twitter.com AI artificial intelligence trending",
            "category": "🐦 X (Twitter)"
        },
        {
            "name": "X AI Researchers",
            "query": "site:x.com AI research GPT Claude models",
            "category": "🐦 X (Twitter)"
        }
    ]

def tavily_search(query, max_results=8):
    """使用 Tavily 搜索"""
    cmd = [SEARCH_SCRIPT, json.dumps({
        "query": query,
        "topic": "news",
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

def clean_social_text(text):
    """清理社交媒体文本"""
    if not text:
        return ""
    # 移除常见噪音
    noise = ['click to see', 'more:', 'read more', 'continue reading',
             'subscribe', 'sign up', 'log in', 'sign in']
    for n in noise:
        text = re.sub(n, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:300] + "..." if len(text) > 300 else text

def evaluate_source(name, posts_list, data):
    """评估来源质量"""
    if name not in data["sources"]:
        data["sources"][name] = {
            "success_rate": 0, "quality_score": 0,
            "attempts": 0, "successes": 0,
            "avg_posts": 0
        }
    
    source = data["sources"][name]
    source["attempts"] += 1
    
    if posts_list and len(posts_list) > 0:
        source["successes"] += 1
        source["avg_posts"] = len(posts_list)
        source["success_rate"] = source["successes"] / source["attempts"]
        # 质量分数基于成功率和帖子数量
        source["quality_score"] = min(source["success_rate"] * (len(posts_list) / 5), 1.0)
    
    return source

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🐦💬 [Explorer Social v1.0] 探索 Reddit 和 X 的 AI 话题...")
    
    # 加载学习数据
    learnings = load_learnings()
    learnings["metrics"]["total_runs"] += 1
    
    sources = get_social_sources()
    results = {}
    total_posts = 0
    
    for source_info in sources:
        name = source_info["name"]
        query = source_info["query"]
        category = source_info["category"]
        
        print(f"🔍 {name}...")
        
        data = tavily_search(query)
        posts_list = []
        
        if data and 'results' in data:
            for r in data['results'][:8]:
                title = r.get('title', '')
                content = clean_social_text(r.get('content', '') or r.get('snippet', ''))
                
                # 清理标题中的站点名
                title = re.sub(r'\s*[-|]\s*(reddit|x|twitter|Reuters|News)$', '', title)
                title = re.sub(r'\|.*$', '', title)
                
                if title and len(title) > 10:
                    posts_list.append({
                        'title': title.strip(),
                        'content': content,
                        'url': r.get('url', '')
                    })
        
        results[category] = results.get(category, [])
        results[category].extend(posts_list)
        
        # 评估并学习
        evaluate_source(name, posts_list, learnings)
        
        print(f"   → {len(posts_list)} 条")
        total_posts += len(posts_list)
    
    save_learnings(learnings)
    
    # 生成报告
    report = f"""# 社交媒体 AI 话题探索报告 | {today}

## 📊 概览

- **探索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **数据来源**: Reddit + X (Twitter) via Tavily Search
- **版本**: v1.0

---

"""
    
    category_emojis = {
        "💬 Reddit": "💬",
        "🐦 X (Twitter)": "🐦"
    }
    
    for category, posts in results.items():
        if not posts:
            continue
        emoji = category_emojis.get(category, "📱")
        report += f"## {emoji} {category}\n\n"
        
        # 去重并显示前 10 条
        seen = set()
        for i, item in enumerate(posts[:10], 1):
            title = item['title']
            if title in seen:
                continue
            seen.add(title)
            
            report += f"{i}. **{title}**\n"
            if item.get('content'):
                report += f"   📝 {item['content']}\n"
            if item.get('url'):
                report += f"   🔗 [链接]({item['url']})\n"
            report += "\n"
    
    avg_posts = learnings["metrics"]["avg_posts_per_run"]
    learnings["metrics"]["avg_posts_per_run"] = (avg_posts * (learnings["metrics"]["total_runs"] - 1) + total_posts) / learnings["metrics"]["total_runs"]
    save_learnings(learnings)
    
    report += f"""---

**总帖子数**: {total_posts} 条
**探索类别**: {len(sources)} 个
**运行次数**: {learnings['metrics']['total_runs']}
"""
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"\n✅ 完成！报告: {REPORT_FILE}")
    print(f"🐦💬 共获取 {total_posts} 条社交媒体内容")

if __name__ == "__main__":
    main()
