import re
import mysql.connector

def remove_urls(text):
    """문장에서 URL을 제거합니다."""
    return re.sub(r'http\S+|www\S+', '', text)

def remove_special_chars(text):
    """특수문자 제거 (영문, 숫자, 공백만 남김)"""
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

def normalize_whitespace(text):
    """여러 공백, 줄바꿈, 탭을 하나의 공백으로 정리"""
    return re.sub(r'\s+', ' ', text).strip()

def filter_short_texts(texts, min_length=10):
    """너무 짧은 문장(글자수 기준) 필터링"""
    return [t for t in texts if len(t.strip()) >= min_length]

def deduplicate_papers(papers):
    """paper_id 기준 중복 제거"""
    seen = set()
    unique = []
    for p in papers:
        if p["paper_id"] not in seen:
            seen.add(p["paper_id"])
            unique.append(p)
    return unique

if __name__ == "__main__":
    # 예시 텍스트
    text = "This paper introduces a new method. More details: https://arxiv.org/abs/2504.00001"
    cleaned = remove_urls(text)
    print(cleaned)

    # 추가 실습: 여러 문장 테스트
    examples = [
        "Visit our site at http://example.com for more info.",
        "No URL here, just text.",
        "Multiple links: https://a.com and www.b.com should be gone.",
    ]
    for t in examples:
        print(remove_urls(t))

    # 특수문자 제거 실습
    text2 = "A New!! Approach@@ to AI ###"
    print(remove_special_chars(text2))

    # 공백 정리 실습
    text3 = "A New \n\n Approach\tto AI"
    print(normalize_whitespace(text3))

    # 너무 짧은 문장 제거 실습
    texts = [
        "AI",
        "Deep learning for medical image analysis",
        "Test"
    ]
    print(filter_short_texts(texts, min_length=10))

    # 중복 제거 실습
    papers = [
        {"paper_id": "2504.00001", "title": "Paper A"},
        {"paper_id": "2504.00002", "title": "Paper B"},
        {"paper_id": "2504.00001", "title": "Paper A"}
    ]
    print(deduplicate_papers(papers))

# DB 연결 정보
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="paper_pipeline_db"
)
cursor = conn.cursor()

# 예시: 전처리된 데이터 적재 (여기서는 예시로 texts와 papers 사용)
# 실제로는 전처리 결과 리스트/딕셔너리로 반복

# clean_papers 테이블에 적재 예시
insert_sql = """
INSERT INTO clean_papers (batch_id, raw_paper_id, clean_title, clean_summary)
VALUES (%s, %s, %s, %s)
"""

# 예시 데이터 (실제 전처리 결과로 대체)
example_clean_data = [
    # (batch_id, raw_paper_id, clean_title, clean_summary)
    ("run_20260409_100000", 1, "A New Approach to Artificial Intelligence", "This paper proposes a new framework for AI"),
    ("run_20260409_100000", 2, "Efficient Learning with Limited Data", "This study investigates sample efficient learning")
]

for row in example_clean_data:
    cursor.execute(insert_sql, row)

conn.commit()
cursor.close()
conn.close()
