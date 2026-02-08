import requests
import time
import re
import json
from datetime import date

TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
# Create a token at https://github.com/settings/tokens
# Scope: Public repositories (read-only)

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
}

SEARCH_URL = "https://api.github.com/search/issues"
COMMENTS_URL = "https://api.github.com/repos/ruanyf/weekly/issues/{}/comments"

IMAGE_PATTERN = re.compile(r"!\[.*?\]\(.*?\)")


def clean_text(md: str) -> str:
    if not md:
        return ""
    return IMAGE_PATTERN.sub("", md).strip()


def fetch_issues(start, end):
    page = 1
    issues = []

    while True:
        r = requests.get(
            SEARCH_URL,
            headers=HEADERS,
            params={
                "q": f"repo:ruanyf/weekly 谁在招人 created:{start}..{end}",
                "per_page": 100,
                "page": page,
                "sort": "created",
                "order": "asc",
            },
        )
        data = r.json()
        items = data.get("items", [])
        if not items:
            break

        issues.extend(items)
        page += 1
        time.sleep(1)

    return issues


def fetch_comments(issue_number):
    page = 1
    comments = []

    while True:
        r = requests.get(
            COMMENTS_URL.format(issue_number),
            headers=HEADERS,
            params={
                "per_page": 100,
                "page": page
            },
        )
        data = r.json()
        if not data:
            break

        comments.extend(data)
        page += 1
        time.sleep(0.5)

    return comments


# -------- 主流程 --------

all_hiring_posts = []

for y in range(2018, date.today().year + 1):
    print(f"fetching issues {y}")
    issues = fetch_issues(f"{y}-01-01", f"{y}-12-31")

    for issue in issues:
        issue_number = issue["number"]
        print(f"  issue {issue_number}")

        comments = fetch_comments(issue_number)

        for c in comments:
            text = clean_text(c["body"])
            if not text:
                continue

            all_hiring_posts.append({
                "issue": issue_number,
                "author": c["user"]["login"],
                "created_at": c["created_at"],
                "text": text,
                "url": c["html_url"],
            })

print("total hiring posts:", len(all_hiring_posts))

with open("weekly_hiring_comments.json", "w", encoding="utf-8") as f:
    json.dump(all_hiring_posts, f, ensure_ascii=False, indent=2)
