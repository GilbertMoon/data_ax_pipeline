import mysql.connector
from datetime import datetime

# 본인 DB 연결 정보로 수정
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="paper_pipeline_db"
)

cursor = conn.cursor()

batch_id = "run_20260409_100000"

try:
    # 실행 시작 기록
    cursor.execute(
        """
        INSERT INTO pipeline_runs (batch_id, run_status, started_at)
        VALUES (%s, %s, NOW())
        """,
        (batch_id, "STARTED")
    )
    conn.commit()
    print(f"Pipeline run started: {batch_id}")

    # ... (여기에 논문 수집 및 적재 코드가 들어감) ...

    # 실행 성공 기록
    cursor.execute(
        """
        UPDATE pipeline_runs
        SET run_status = %s, ended_at = NOW()
        WHERE batch_id = %s
        """,
        ("SUCCESS", batch_id)
    )
    conn.commit()
    print(f"Pipeline run succeeded: {batch_id}")

except Exception as e:
    # 실패 시 기록
    cursor.execute(
        """
        UPDATE pipeline_runs
        SET run_status = %s, ended_at = NOW(), note = %s
        WHERE batch_id = %s
        """,
        ("FAILED", str(e), batch_id)
    )
    conn.commit()
    print(f"Pipeline run failed: {batch_id}")
    print(e)
finally:
    cursor.close()
    conn.close()
