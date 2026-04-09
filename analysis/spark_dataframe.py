from pyspark.sql import SparkSession
from pyspark.sql.functions import length, count, when, avg

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("paper_analysis") \
    .getOrCreate()

# 샘플 데이터
data = [
    ("2026-04-09", "AI research on multimodal learning"),
    ("2026-04-09", "Deep learning for image analysis"),
    ("2026-04-10", "LLM based reasoning model"),
]
columns = ["date", "text"]

df = spark.createDataFrame(data, columns)
print("=== DataFrame ===")
df.show()

# 텍스트 길이 분석
print("=== 텍스트 길이 추가 ===")
df = df.withColumn("text_length", length(df["text"]))
df.show()

# 날짜별 논문 수 집계
print("=== 날짜별 논문 수 집계 ===")
df.groupBy("date").agg(
    count("*").alias("paper_count")
).show()

# 키워드 기반 집계 (AI 포함 여부)
print("=== 'AI' 키워드 포함 여부 집계 ===")
df = df.withColumn(
    "is_ai",
    when(df["text"].contains("AI"), 1).otherwise(0)
)
df.groupBy("is_ai").count().show()

# 길이 기준 그룹 집계 (평균 길이)
print("=== 날짜별 논문 수 및 평균 길이 ===")
df.groupBy("date").agg(
    count("*").alias("count"),
    avg("text_length").alias("avg_text_length")
).show()

# 세션 종료
df.unpersist()
spark.stop()
