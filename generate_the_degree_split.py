import json
import re
from pathlib import Path

# === 读入数据 ===
with open("weekly_hiring_comments.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# === 规则 ===
bachelor_patterns = [
    r"本科及以上",
    r"本科以上",
    r"本科起",
    r"本科起步",
    r"本科起算",
    r"本科起点",
    r"本科学历",
    r"本科及本科以上",
    r"本科或以上",
    r"学士及以上",
    r"学士以上",
    r"学士学位",
]

master_patterns = [
    r"硕士及以上",
    r"硕士以上",
    r"硕士起",
    r"硕士起步",
    r"硕士起点",
    r"研究生及以上",
    r"研究生以上",
    r"研究生学历",
    r"硕士研究生及以上",
]

bachelor_re = re.compile("|".join(bachelor_patterns))
master_re = re.compile("|".join(master_patterns))

# === 分类容器 ===
bachelor_posts = []
master_posts = []

# === 分类 ===
for p in posts:
    text = p.get("text", "")
    if master_re.search(text):
        master_posts.append(p)
    elif bachelor_re.search(text):
        bachelor_posts.append(p)

# === 输出目录 ===
out_dir = Path("degree_split")
out_dir.mkdir(exist_ok=True)

# === 写文件 ===
with open(out_dir / "本科及以上.json", "w", encoding="utf-8") as f:
    json.dump(bachelor_posts, f, ensure_ascii=False, indent=2)

with open(out_dir / "硕士及以上.json", "w", encoding="utf-8") as f:
    json.dump(master_posts, f, ensure_ascii=False, indent=2)

# === 统计 ===
print("本科及以上:", len(bachelor_posts))
print("硕士及以上:", len(master_posts))
print("合计:", len(bachelor_posts) + len(master_posts))

import json
from collections import defaultdict
from pathlib import Path


def json_to_md(json_path: Path, md_path: Path, title: str):
    with json_path.open("r", encoding="utf-8") as f:
        posts = json.load(f)

    issues = defaultdict(list)
    for p in posts:
        issues[p["issue"]].append(p)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"共 {len(posts)} 条评论，{len(issues)} 个 Issue\n\n")

        for issue_id in sorted(issues):
            f.write(f"## Issue {issue_id}\n\n")
            for c in issues[issue_id]:
                f.write(f"- Author: `{c['author']}`\n")
                f.write(f"- Time: {c['created_at']}\n")
                f.write(f"- URL: {c['url']}\n\n")
                f.write(c["text"].strip())
                f.write("\n\n---\n\n")


base_dir = Path("degree_split")

json_to_md(base_dir / "本科及以上.json", base_dir / "本科及以上.md", "本科及以上学历要求")

json_to_md(base_dir / "硕士及以上.json", base_dir / "硕士及以上.md", "硕士及以上学历要求")
