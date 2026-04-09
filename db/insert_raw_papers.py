import mysql.connector

# 본인 DB 연결 정보로 수정
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="paper_pipeline_db"
)

cursor = conn.cursor()

batch_id = "run_20260409_100000"

papers = [
    {
        "category": "cs.AI",
        "paper_id": "2504.00001",
        "title": "A New Approach to Artificial Intelligence",
        "link": "http://arxiv.org/abs/2504.00001",
        "summary": "This paper proposes a new framework for AI...",
        "published_at": "2026-04-09 00:00:00"
    },
    {
        "category": "cs.LG",
        "paper_id": "2504.00002",
        "title": "Efficient Learning with Limited Data",
        "link": "http://arxiv.org/abs/2504.00002",
        "summary": "This study investigates sample-efficient learning...",
        "published_at": "2026-04-09 00:00:00"
    }
]

sql = """
INSERT INTO raw_papers
(batch_id, source, category, paper_id, title, link, summary, published_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for p in papers:
    cursor.execute(sql, (
        batch_id,
        "arxiv_rss",
        p["category"],
        p["paper_id"],
        p["title"],
        p["link"],
        p["summary"],
        p["published_at"]
    ))

conn.commit()
cursor.close()
conn.close()
