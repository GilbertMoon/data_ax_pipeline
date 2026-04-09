import re
import mysql.connector

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="paper_pipeline_db"
)

cursor = conn.cursor(dictionary=True)

select_sql = """
SELECT id, batch_id, title, summary
FROM raw_papers
"""

insert_sql = """
INSERT INTO clean_papers (batch_id, raw_paper_id, clean_title, clean_summary)
VALUES (%s, %s, %s, %s)
"""

cursor.execute(select_sql)
rows = cursor.fetchall()

for row in rows:
    clean_title = clean_text(row["title"])
    clean_summary = clean_text(row["summary"])

    if len(clean_summary) < 10:
        continue

    cursor.execute(insert_sql, (
        row["batch_id"],
        row["id"],
        clean_title,
        clean_summary
    ))

conn.commit()
cursor.close()
conn.close()
