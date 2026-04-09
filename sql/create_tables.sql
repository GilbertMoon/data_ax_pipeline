-- 테이블 생성 SQL 예시
-- 예시: 댓글 테이블
CREATE TABLE comments (
    id INT PRIMARY KEY,
    user_id VARCHAR(50),
    comment_text TEXT,
    created_at TIMESTAMP
);
