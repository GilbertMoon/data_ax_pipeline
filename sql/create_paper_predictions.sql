ALTER TABLE paper_predictions
    CHANGE COLUMN clean_paper_id paper_id VARCHAR(50) NOT NULL,
    CHANGE COLUMN topic_label topic_rule_label VARCHAR(255) NOT NULL,
    CHANGE COLUMN predicted_at created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN sensitivity_rule_label VARCHAR(255) NOT NULL AFTER topic_rule_label,
    ADD COLUMN ml_pred_label VARCHAR(100) NOT NULL AFTER sensitivity_rule_label,
    DROP COLUMN keyword_summary,
    DROP COLUMN trend_score;