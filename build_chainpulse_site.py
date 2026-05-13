from __future__ import annotations

import html
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path("/Users/skylerlan/Documents/Codex/2026-04-26/netlify-site")
CONTENT_PATH = ROOT / "content.json"
POSTS_DIR = ROOT / "posts"
CATEGORIES_DIR = ROOT / "categories"

CSS = """
:root{--paper:rgba(255,255,255,.82);--line:rgba(17,24,39,.08);--text:#131827;--muted:#5c6478;--grad:linear-gradient(135deg,#8b1fe8 0%,#5a4dff 38%,#10c8c6 70%,#64d96b 100%);--shadow:0 20px 50px rgba(15,23,42,.08)}*{box-sizing:border-box}html,body{margin:0;padding:0}body{font-family:"Avenir Next","SF Pro Display","PingFang SC","Helvetica Neue",sans-serif;color:var(--text);background:radial-gradient(circle at 14% 18%,rgba(182,32,224,.09),transparent 22%),radial-gradient(circle at 84% 16%,rgba(47,128,255,.09),transparent 22%),radial-gradient(circle at 72% 76%,rgba(20,213,204,.12),transparent 20%),linear-gradient(180deg,#fbfdff 0%,#f5f7fb 100%);min-height:100vh}a{color:inherit;text-decoration:none}.wrap{width:min(1240px,calc(100% - 36px));margin:24px auto 48px}.top-nav{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}.top-nav a{padding:12px 16px;border-radius:999px;background:rgba(255,255,255,.82);border:1px solid var(--line);font-size:14px;box-shadow:0 8px 24px rgba(15,23,42,.05)}.top-nav a:hover{background:rgba(255,255,255,.96)}.hero,.panel,.card,.side,.logic,.data,.category-card,.post-card{background:var(--paper);backdrop-filter:blur(18px);border:1px solid var(--line);box-shadow:var(--shadow)}.hero{padding:34px;border-radius:32px;overflow:hidden;position:relative;margin-bottom:20px}.hero:after{content:"";position:absolute;right:-120px;top:-120px;width:320px;height:320px;background:var(--grad);opacity:.12;filter:blur(36px);border-radius:50%}.brand{display:flex;align-items:center;gap:16px;margin-bottom:18px}.mark{width:74px;height:74px;border-radius:24px;background:rgba(255,255,255,.88);display:grid;place-items:center;border:1px solid rgba(255,255,255,.75);box-shadow:0 16px 40px rgba(47,128,255,.10)}.kicker{display:inline-block;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.80);border:1px solid var(--line);color:var(--muted);font-size:11px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px}h1{margin:0;font-size:clamp(34px,6vw,70px);line-height:.98;letter-spacing:-.04em}.accent{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}.hero p{margin:16px 0 0;max-width:860px;color:var(--muted);font-size:16px;line-height:1.9}.stats,.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-top:24px}.stat,.stat-card{padding:18px;border-radius:22px;background:rgba(255,255,255,.86);border:1px solid var(--line)}.label,.stat-label{font-size:12px;color:var(--muted);margin-bottom:10px;letter-spacing:.06em;text-transform:uppercase}.value,.stat-value{font-size:24px;font-weight:700;letter-spacing:-.03em}.grid,.main-grid,.detail{display:grid;grid-template-columns:320px minmax(0,1fr);gap:20px}.stack,.category-grid,.post-grid{display:grid;gap:16px}.panel,.side,.card,.category-card,.post-card{padding:24px;border-radius:26px}.panel h2,.title2,.panel-title{margin:0 0 14px;font-size:34px;letter-spacing:-.04em}.panel p,.panel li,.side p,.side li{color:var(--muted);line-height:1.85;font-size:14px}.panel ul,.side ul{margin:0;padding-left:18px}.category-grid{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.category-card,.card,.post-card{position:relative;overflow:hidden}.category-card:before,.card:before,.post-card:before{content:"";position:absolute;left:0;top:0;width:100%;height:4px;background:var(--grad)}.category-card h3,.cat h3{margin:0 0 10px;font-size:22px;letter-spacing:-.03em}.category-card p{margin:0;color:var(--muted);line-height:1.8}.category-count{margin-top:18px;font-size:14px;font-weight:650}.post-grid{grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}.meta,.meta-row,.chips{display:flex;flex-wrap:wrap;gap:8px}.pill,.chip{padding:8px 12px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.76);font-size:12px}.card h3,.post-card h3{margin:14px 0 10px;font-size:28px;line-height:1.18;letter-spacing:-.04em}.summary{margin:0;color:var(--muted);line-height:1.85;font-size:15px}.side{position:sticky;top:20px;height:fit-content}.side h3{margin:0 0 12px;font-size:18px;letter-spacing:-.02em}.article{padding:28px;border-radius:28px}.article h1{font-size:clamp(28px,5vw,56px);line-height:1.02;margin:16px 0 12px}.lead{color:var(--muted);line-height:1.9;font-size:16px;margin:0 0 16px}.section{border-top:1px solid var(--line);margin-top:18px;padding-top:18px}.section h2{margin:0 0 12px;font-size:22px;letter-spacing:-.03em}.section p{margin:0 0 14px;line-height:1.95}.section ul{margin:0;padding-left:18px}.section li{line-height:1.9;margin-bottom:6px}.logic-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.logic,.data{padding:16px;border-radius:22px}.logic .k,.data .k{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}.logic .v{font-size:15px;line-height:1.8}.data-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}.data .v{font-size:24px;font-weight:700;letter-spacing:-.03em}.quote,.warn{border-radius:22px;padding:18px;line-height:1.9}.quote{background:linear-gradient(180deg,rgba(47,128,255,.08),rgba(20,213,204,.08));border:1px solid rgba(47,128,255,.16)}.warn{background:linear-gradient(180deg,rgba(182,32,224,.08),rgba(255,166,0,.08));border:1px solid rgba(182,32,224,.14)}.side-note,.note{margin-top:18px;color:var(--muted);font-size:13px;line-height:1.7}.video-mini{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px}.video-pill{padding:7px 10px;border-radius:999px;border:1px solid rgba(17,24,39,.08);background:rgba(255,255,255,.84);color:#485065;font-size:12px;line-height:1}.video-title-panel{margin:18px 0 0;padding:18px;border-radius:20px;background:linear-gradient(180deg,rgba(255,255,255,.88),rgba(250,252,255,.92));border:1px solid rgba(17,24,39,.08);box-shadow:0 12px 28px rgba(26,31,53,.06)}.video-title-panel h2{margin:0 0 12px;font-size:22px;line-height:1.2}.video-title-note{margin:0 0 12px;color:#697386;font-size:14px;line-height:1.75}.video-title-list{display:grid;gap:10px}.video-title-item{padding:12px 14px;border-radius:16px;background:rgba(255,255,255,.86);border:1px solid rgba(17,24,39,.08);color:#131827;font-size:15px;font-weight:600;line-height:1.6}@media (max-width:980px){.grid,.main-grid,.detail{grid-template-columns:1fr}.side{position:static}.hero{padding:24px}h1{font-size:clamp(32px,11vw,56px)}}
""".strip()

LOGO = """
<svg width="52" height="52" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><linearGradient id="cp-logo-grad" x1="14" y1="96" x2="102" y2="22" gradientUnits="userSpaceOnUse"><stop stop-color="#8B1FE8"/><stop offset="0.38" stop-color="#5A4DFF"/><stop offset="0.7" stop-color="#10C8C6"/><stop offset="1" stop-color="#64D96B"/></linearGradient></defs><path d="M30 63C22 63 16 57 16 49C16 41 22 35 30 35H41" stroke="url(#cp-logo-grad)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M84 41C92 41 98 47 98 55C98 63 92 69 84 69H73" stroke="url(#cp-logo-grad)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M43 61L71 33" stroke="url(#cp-logo-grad)" stroke-width="8" stroke-linecap="round"/><path d="M68 23L42 49C37 54 37 62 42 67C47 72 55 72 60 67L86 41C95 32 95 19 86 10C77 1 64 1 55 10L48 17" stroke="url(#cp-logo-grad)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 48L36 36C42 30 52 30 58 36C64 42 64 52 58 58L46 70C38 78 26 78 18 70C10 62 10 50 18 42L24 36" stroke="url(#cp-logo-grad)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity=".96"/></svg>
""".strip()


def e(value: str) -> str:
    return html.escape(str(value), quote=True)


def nav(prefix: str = "") -> str:
    return (
        '<nav class="top-nav">'
        f'<a href="{prefix}index.html">首页</a>'
        f'<a href="{prefix}archive.html">时间归档</a>'
        f'<a href="{prefix}categories/travel.html">旅行相关</a>'
        f'<a href="{prefix}categories/products.html">物品 / 硬件</a>'
        f'<a href="{prefix}categories/food.html">食品 / 消费品</a>'
        f'<a href="{prefix}categories/smallbiz.html">小生意雷达</a>'
        f'<a href="{prefix}categories/websites.html">网站 / 独立站</a>'
        f'<a href="{prefix}categories/solo.html">一人公司 / 数字产品</a>'
        f'<a href="{prefix}categories/growth.html">内容分发 / 营销增长</a>'
        f'<a href="{prefix}categories/tools.html">工具 / SaaS</a>'
        "</nav>"
    )


def shell(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8" />'
        '<meta name="viewport" content="width=device-width, initial-scale=1" />'
        f"<title>{e(title)}</title><style>{CSS}</style></head><body><div class=\"wrap\">"
        f"{body}</div></body></html>"
    )


def chips(post: dict, categories: dict, link_prefix: str = "", category_links: bool = False) -> str:
    items = []
    for category_slug in post["categories"]:
        name = categories[category_slug]["name"]
        if category_links:
            items.append(f'<a class="chip" href="{link_prefix}categories/{category_slug}.html">{e(name)}</a>')
        else:
            items.append(f'<span class="chip">{e(name)}</span>')
    items.extend(f"<span class=\"chip\">{e(tag)}</span>" for tag in post["tags"])
    return "".join(items)


def video_pills(post: dict) -> str:
    return "".join(f'<span class="video-pill">{e(item)}</span>' for item in post.get("video_titles", []))


def post_card(post: dict, categories: dict, href: str, category_links: bool, link_prefix: str = "") -> str:
    return (
        '<article class="post-card">'
        f'<div class="meta-row"><span class="pill">{e(post["date"])}</span><span class="pill">{e(post["weekday"])}</span><span class="pill">{e(post["duration"])}</span></div>'
        f'<h3><a href="{href}">{e(post["title"])}</a></h3>'
        f'<p class="summary">{e(post["summary"])}</p>'
        f'<div class="chips">{chips(post, categories, link_prefix=link_prefix, category_links=category_links)}</div>'
        f'<div class="video-mini">{video_pills(post)}</div>'
        "</article>"
    )


def archive_card(post: dict, categories: dict, href: str, link_prefix: str = "") -> str:
    return (
        '<article class="card">'
        f'<div class="meta"><span class="pill">{e(post["date"])}</span><span class="pill">{e(post["weekday"])}</span><span class="pill">{e(post["duration"])}</span></div>'
        f'<h3><a href="{href}">{e(post["title"])}</a></h3>'
        f'<p class="summary">{e(post["summary"])}</p>'
        f'<div class="chips">{chips(post, categories, link_prefix=link_prefix, category_links=True)}</div>'
        f'<div class="video-mini">{video_pills(post)}</div>'
        "</article>"
    )


def render_home(data: dict) -> str:
    categories = data["categories"]
    posts = data["posts"]
    category_cards = "".join(
        '<a class="category-card" href="categories/{slug}.html"><div class="kicker">Category</div><h3>{name}</h3><p>{desc}</p><div class="category-count">当前 {count} 篇</div></a>'.format(
            slug=e(slug),
            name=e(item["name"]),
            desc=e(item["desc"]),
            count=sum(1 for post in posts if slug in post["categories"]),
        )
        for slug, item in categories.items()
    )
    latest_posts = "".join(
        post_card(post, categories, f'posts/{post["slug"]}.html', category_links=False) for post in posts[:6]
    )
    body = (
        nav()
        + '<section class="hero"><div class="brand"><div class="mark">'
        + LOGO
        + '</div><div><div class="kicker">ChainPulse Research Library</div><h1><span class="accent">ChainPulse</span>案例口播知识库</h1></div></div>'
        f'<p>{e(data["meta"]["description"])}</p>'
        '<div class="stats-grid">'
        f'<div class="stat-card"><div class="stat-label">更新频率</div><div class="stat-value">{e(data["meta"]["schedule"])}</div></div>'
        f'<div class="stat-card"><div class="stat-label">当前稿件</div><div class="stat-value">{len(posts)} 篇</div></div>'
        f'<div class="stat-card"><div class="stat-label">分类数量</div><div class="stat-value">{len(categories)} 类</div></div>'
        f'<div class="stat-card"><div class="stat-label">最近更新时间</div><div class="stat-value">{e(data["meta"]["generatedAt"])}</div></div>'
        '</div></section>'
        '<section class="main-grid"><aside class="side"><h3>这个知识库里有什么</h3><ul><li>每篇内容先判断“适不适合做口播”，再看完整口播稿。</li><li>小生意雷达会收集小红书、闲鱼、淘宝、抖音、独立站里的轻量生意模型。</li><li>详情页保留案例分析、核心数据、逻辑拆解、推荐角度、注意事项和口播正文。</li><li>归档页按时间查看全部内容，分类页按主题持续积累。</li></ul><div class="side-note">品牌入口：ChainPulse<br>结构：Home / Archive / Categories / Posts</div></aside>'
        f'<main class="stack"><section class="panel"><h2 class="panel-title">类目入口</h2><div class="category-grid">{category_cards}</div></section>'
        f'<section class="panel"><h2 class="panel-title">最新稿件</h2><div class="post-grid">{latest_posts}</div></section></main></section>'
    )
    return shell(data["meta"]["title"], body)


def render_archive(data: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for post in data["posts"]:
        grouped[post["date"][:7]].append(post)
    sections = "".join(
        f'<section class="panel"><div class="title2">{e(month)}</div><div class="post-grid">'
        + "".join(archive_card(post, data["categories"], f'posts/{post["slug"]}.html') for post in month_posts)
        + "</div></section>"
        for month, month_posts in grouped.items()
    )
    body = (
        nav()
        + '<section class="hero"><div class="brand"><div class="mark">'
        + LOGO
        + '</div><div><div class="kicker">Archive</div><h1>时间归档</h1></div></div><p>这里保留所有稿件，不覆盖旧内容。后面每周新增的案例，都会继续沉淀到这个目录里。</p></section>'
        f'<div class="stack">{sections}</div>'
    )
    return shell(f'{data["meta"]["brand"]}｜时间归档', body)


def render_category(slug: str, info: dict, posts: list[dict], categories: dict) -> str:
    cards = "".join(
        archive_card(post, categories, f'../posts/{post["slug"]}.html', link_prefix="../") for post in posts
    )
    if not cards:
        cards = (
            '<article class="card"><div class="kicker">Coming Soon</div>'
            '<h3>这个栏目正在等待第一篇案例</h3>'
            '<p class="summary">后续会优先收录平台小生意、轻交付服务、低库存商品、模板化接单和细分人群需求。</p>'
            "</article>"
        )
    body = (
        nav("../")
        + '<section class="hero"><div class="brand"><div class="mark">'
        + LOGO
        + f'</div><div><div class="kicker">Category</div><h1>{e(info["name"])}</h1></div></div><p>{e(info["desc"])}</p>'
        f'<div class="stats"><div class="stat"><div class="label">当前收录</div><div class="value">{len(posts)} 篇</div></div></div></section>'
        f'<section class="panel"><div class="title2">该类目下的内容</div><div class="post-grid">{cards}</div></section>'
    )
    return shell(f'ChainPulse｜{info["name"]}', body)


def render_detail(post: dict, data: dict) -> str:
    categories = data["categories"]
    analysis = post["analysis"]
    source_list = "".join(
        f'<li><a href="{e(item["url"])}" target="_blank" rel="noreferrer">{e(item["label"])}</a></li>'
        for item in post["sources"]
    )
    logic_cards = (
        f'<div class="logic"><div class="k">适不适合做口播</div><div class="v">{e(analysis["suitable"])}</div></div>'
        f'<div class="logic"><div class="k">为什么值得讲</div><div class="v">{e(analysis.get("worthTelling", post["summary"]))}</div></div>'
        f'<div class="logic"><div class="k">最值得讲的问题</div><div class="v">{e(analysis["coreQuestion"])}</div></div>'
        f'<div class="logic"><div class="k">最一针见血的角度</div><div class="v">{e(analysis["sharpAngle"])}</div></div>'
    )
    data_cards = "".join(
        f'<div class="data"><div class="k">{e(item["label"])}</div><div class="v">{e(item["value"])}</div></div>'
        for item in analysis["coreData"]
    )
    why_worked = "".join(f"<li>{e(item)}</li>" for item in analysis["whyWorked"])
    insights = "".join(f"<li>{e(item)}</li>" for item in post["insights"])
    script = "".join(f"<p>{e(item)}</p>" for item in post["script"])
    video_titles = "".join(
        f'<div class="video-title-item">{index}. {e(item)}</div>'
        for index, item in enumerate(post.get("video_titles", []), start=1)
    )
    body = (
        nav("../")
        + '<div class="detail"><aside class="side"><h3>文章导航</h3><p>这篇内容先看案例判断与核心数据，再看推荐角度，最后看完整口播稿。</p>'
        f'<div class="chips" style="margin-bottom:14px;">{chips(post, categories, link_prefix="../", category_links=True)}</div>'
        f'<h3>一句话结论</h3><p>{e(post["summary"])}</p>'
        f'<h3>推荐怎么讲</h3><p>{e(analysis["recommendedAngle"])}</p>'
        f'<h3>参考链接</h3><ul>{source_list}</ul></aside>'
        '<article class="article panel">'
        f'<div class="meta"><span class="pill">{e(post["date"])}</span><span class="pill">{e(post["weekday"])}</span><span class="pill">{e(post["duration"])}</span><span class="pill">{e(post["status"])}</span></div>'
        f'<h1>{e(post["title"])}</h1>'
        f'<p class="lead"><strong>开头钩子：</strong>{e(post["hook"])}</p>'
        f'<div class="chips">{chips(post, categories, link_prefix="../", category_links=True)}</div>'
        f'<section class="section video-title-panel"><h2>备选短视频标题</h2><p class="video-title-note">这组标题更偏短视频分发和点击率导向，拍视频时可以直接挑一个用。</p><div class="video-title-list">{video_titles}</div></section>'
        f'<section class="section"><h2>案例判断</h2><div class="logic-grid">{logic_cards}</div></section>'
        f'<section class="section"><h2>核心数据</h2><div class="data-grid">{data_cards}</div></section>'
        f'<section class="section"><h2>为什么它能做成</h2><ul>{why_worked}</ul></section>'
        f'<section class="section"><h2>最值得带走的洞察</h2><div class="quote">{e(analysis["keyInsight"])}</div></section>'
        f'<section class="section"><h2>不要怎么讲</h2><div class="warn">{e(analysis["dontSay"])}</div></section>'
        f'<section class="section"><h2>可带走的观点</h2><ul>{insights}</ul></section>'
        f'<section class="section"><h2>完整口播稿</h2>{script}</section>'
        "</article></div>"
    )
    return shell(f'{data["meta"]["brand"]}｜{post["title"]}', body)


def build() -> None:
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    data["meta"]["generatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    CONTENT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)

    (ROOT / "index.html").write_text(render_home(data), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(data), encoding="utf-8")

    for slug, info in data["categories"].items():
        category_posts = [post for post in data["posts"] if slug in post["categories"]]
        (CATEGORIES_DIR / f"{slug}.html").write_text(
            render_category(slug, info, category_posts, data["categories"]),
            encoding="utf-8",
        )

    for post in data["posts"]:
        (POSTS_DIR / f'{post["slug"]}.html').write_text(render_detail(post, data), encoding="utf-8")


if __name__ == "__main__":
    build()
