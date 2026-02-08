import json
from pathlib import Path
from collections import defaultdict

with open("weekly_hiring_comments.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

by_issue = defaultdict(list)
for p in posts:
    by_issue[p["issue"]].append(p)

out_dir = Path("issues_md")
out_dir.mkdir(exist_ok=True)

for issue, items in by_issue.items():
    path = out_dir / f"issue_{issue}.md"
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# Issue #{issue} 招聘汇总\n\n")

        for i, p in enumerate(items, 1):
            f.write(f"## 招聘 {i}\n\n")
            f.write(f"- 作者: {p['author']}\n")
            f.write(f"- 时间: {p['created_at']}\n")
            f.write(f"- 来源: {p['url']}\n\n")
            f.write(p["text"])
            f.write("\n\n---\n\n")
