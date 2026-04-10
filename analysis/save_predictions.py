import csv
from datetime import datetime
from typing import Dict, List

import mysql.connector


CREATE_PAPER_PREDICTIONS_SQL = """
CREATE TABLE IF NOT EXISTS paper_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id VARCHAR(50) NOT NULL,
    batch_id VARCHAR(50) NOT NULL,
    topic_rule_label VARCHAR(255) NOT NULL,
    sensitivity_rule_label VARCHAR(255) NOT NULL,
    ml_pred_label VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

try:
    from analysis.ml_classifier import (
        build_training_dataset,
        predict_papers_by_ml,
        train_text_classifier,
    )
    from analysis.rule_based_classifier import classify_papers_by_rules
except ModuleNotFoundError:
    from ml_classifier import build_training_dataset, predict_papers_by_ml, train_text_classifier
    from rule_based_classifier import classify_papers_by_rules


def build_sample_papers() -> List[Dict[str, str]]:
    return [
        {
            "paper_id": "P001",
            "title": "Transformer model for diagnosis support",
            "summary": "A medical deep learning system for hospital patient triage.",
        },
        {
            "paper_id": "P002",
            "title": "Ethical issues in AI decision systems",
            "summary": "Bias, fairness and responsibility concerns in automated decisions.",
        },
        {
            "paper_id": "P003",
            "title": "Customer strategy in digital business",
            "summary": "A platform marketing study for business growth.",
        },
    ]


def merge_prediction_results(
    rule_based_rows: List[Dict[str, str]],
    ml_rows: List[Dict[str, str]],
    batch_id: str,
) -> List[Dict[str, str]]:
    ml_by_paper_id = {row["paper_id"]: row for row in ml_rows}
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    merged_rows: List[Dict[str, str]] = []
    for row in rule_based_rows:
        ml_row = ml_by_paper_id.get(row["paper_id"], {})
        merged_rows.append(
            {
                "paper_id": row["paper_id"],
                "batch_id": batch_id,
                "topic_rule_label": row["topic_rule_label"],
                "sensitivity_rule_label": row["sensitivity_rule_label"],
                "ml_pred_label": ml_row.get("ml_pred_label", "기타"),
                "created_at": created_at,
            }
        )

    return merged_rows


def save_predictions_to_csv(rows: List[Dict[str, str]], csv_path: str) -> None:
    fieldnames = [
        "paper_id",
        "batch_id",
        "topic_rule_label",
        "sensitivity_rule_label",
        "ml_pred_label",
        "created_at",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def ensure_paper_predictions_table(cursor) -> None:
    cursor.execute("SHOW TABLES LIKE 'paper_predictions'")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        cursor.execute(CREATE_PAPER_PREDICTIONS_SQL)
        return

    cursor.execute("SHOW COLUMNS FROM paper_predictions")
    existing_columns = {row[0] for row in cursor.fetchall()}

    if "clean_paper_id" in existing_columns and "paper_id" not in existing_columns:
        cursor.execute(
            "ALTER TABLE paper_predictions CHANGE COLUMN clean_paper_id paper_id VARCHAR(50) NOT NULL"
        )
        existing_columns.remove("clean_paper_id")
        existing_columns.add("paper_id")

    if "topic_label" in existing_columns and "topic_rule_label" not in existing_columns:
        cursor.execute(
            "ALTER TABLE paper_predictions CHANGE COLUMN topic_label topic_rule_label VARCHAR(255) NOT NULL"
        )
        existing_columns.remove("topic_label")
        existing_columns.add("topic_rule_label")

    if "predicted_at" in existing_columns and "created_at" not in existing_columns:
        cursor.execute(
            "ALTER TABLE paper_predictions CHANGE COLUMN predicted_at created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
        )
        existing_columns.remove("predicted_at")
        existing_columns.add("created_at")

    if "sensitivity_rule_label" not in existing_columns:
        cursor.execute(
            "ALTER TABLE paper_predictions ADD COLUMN sensitivity_rule_label VARCHAR(255) NOT NULL AFTER topic_rule_label"
        )

    if "ml_pred_label" not in existing_columns:
        cursor.execute(
            "ALTER TABLE paper_predictions ADD COLUMN ml_pred_label VARCHAR(100) NOT NULL AFTER sensitivity_rule_label"
        )


def save_predictions_to_db(rows: List[Dict[str, str]]) -> None:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="paper_pipeline_db"
    )
    cursor = conn.cursor()

    ensure_paper_predictions_table(cursor)

    insert_sql = """
    INSERT INTO paper_predictions
    (paper_id, batch_id, topic_rule_label, sensitivity_rule_label, ml_pred_label, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for row in rows:
        cursor.execute(
            insert_sql,
            (
                row["paper_id"],
                row["batch_id"],
                row["topic_rule_label"],
                row["sensitivity_rule_label"],
                row["ml_pred_label"],
                row["created_at"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    batch_id = "20260410_0900"
    papers = build_sample_papers()

    rule_based_rows = classify_papers_by_rules(papers)

    train_texts, train_labels = build_training_dataset()
    vectorizer, model = train_text_classifier(train_texts, train_labels)
    ml_rows = predict_papers_by_ml(papers, vectorizer, model)

    prediction_rows = merge_prediction_results(rule_based_rows, ml_rows, batch_id)
    save_predictions_to_csv(prediction_rows, "outputs/prediction_sample.csv")
    save_predictions_to_db(prediction_rows)

    for row in prediction_rows:
        print(row)

    print("prediction_sample.csv 저장 완료")
    print("paper_predictions 테이블 저장 완료")