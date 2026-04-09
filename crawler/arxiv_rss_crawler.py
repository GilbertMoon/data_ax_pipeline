import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

rss_urls = [
    "https://rss.arxiv.org/rss/cs.AI",
    "https://rss.arxiv.org/rss/cs.LG",
    "https://rss.arxiv.org/rss/cs.CL",
    "https://rss.arxiv.org/rss/cs.CV",
    "https://rss.arxiv.org/rss/cs.RO"
]

all_papers = []

for rss_url in rss_urls:
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.text, "xml")

    category = rss_url.split("/")[-1]
    comments = []

    for i, item in enumerate(soup.find_all("item")):
        title = item.title.text.strip() if item.title else ""
        link = item.link.text.strip() if item.link else ""
        description = item.description.text.strip() if item.description else ""

        paper = {
            "category": category,
            "paper_id": f"{category}_{i}",
            "title": title,
            "link": link,
            "summary": description[:200]
        }
        all_papers.append(paper)
        comments.append(paper)

    # 실습 2. CSV 임시 저장
    df = pd.DataFrame(comments)
    df.to_csv(f"outputs/{category}_comments.csv", index=False, encoding="utf-8-sig")

    # 실습 3. JSON 저장
    with open(f"outputs/{category}_raw_comments.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

    # 실습 4. 로그 파일 생성
    log_text = f"""
[CRAWL START] {datetime.now()}
URL: {rss_url}
COUNT: {len(comments)}
"""
    with open("logs/crawl_log.txt", "a", encoding="utf-8") as f:
        f.write(log_text)

# 전체 논문 리스트도 저장 (옵션)
df_all = pd.DataFrame(all_papers)
df_all.to_csv("outputs/comments.csv", index=False, encoding="utf-8-sig")
with open("outputs/raw_comments.json", "w", encoding="utf-8") as f:
    json.dump(all_papers, f, ensure_ascii=False, indent=2)

print(all_papers[:5])
print("총 수집 논문 수:", len(all_papers))