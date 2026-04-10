#analysis\ml_classifier.py
from typing import Dict, List, Sequence, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

try:
    from analysis.rule_based_classifier import combine_title_and_summary
except ModuleNotFoundError:
    from rule_based_classifier import combine_title_and_summary


def build_training_dataset() -> Tuple[List[str], List[str]]:
    texts = [
        "transformer model for diagnosis support",
        "ethical issues in ai decision systems",
        "customer strategy in digital business",
        "bert based medical image diagnosis",
        "privacy and fairness in recommendation models",
        "platform marketing strategy for customer growth",
    ]
    labels = ["AI", "윤리", "경영", "AI", "윤리", "경영"]
    return texts, labels


def train_text_classifier(texts: Sequence[str], labels: Sequence[str]) -> Tuple[TfidfVectorizer, LogisticRegression]:
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(features, labels)
    return vectorizer, model


def predict_labels(texts: Sequence[str], vectorizer: TfidfVectorizer, model: LogisticRegression) -> List[str]:
    test_features = vectorizer.transform(texts)
    predictions = model.predict(test_features)
    return predictions.tolist()


def predict_papers_by_ml(
    papers: Sequence[Dict[str, str]],
    vectorizer: TfidfVectorizer,
    model: LogisticRegression,
) -> List[Dict[str, str]]:
    combined_texts = [
        combine_title_and_summary(paper.get("title", ""), paper.get("summary", ""))
        for paper in papers
    ]
    predicted_labels = predict_labels(combined_texts, vectorizer, model)

    return [
        {
            **paper,
            "combined_text": combined_text,
            "ml_pred_label": predicted_label,
        }
        for paper, combined_text, predicted_label in zip(papers, combined_texts, predicted_labels)
    ]


if __name__ == "__main__":
    train_texts, train_labels = build_training_dataset()
    vectorizer, model = train_text_classifier(train_texts, train_labels)

    sample_papers = [
        {
            "paper_id": "P001",
            "title": "BERT based hospital prediction system",
            "summary": "A transformer approach for clinical diagnosis support.",
        },
        {
            "paper_id": "P002",
            "title": "Privacy and fairness in recommendation models",
            "summary": "Ethical risks in ai driven personalization.",
        },
        {
            "paper_id": "P003",
            "title": "Customer strategy in platform business",
            "summary": "Marketing and growth planning for digital services.",
        },
    ]

    predictions = predict_papers_by_ml(sample_papers, vectorizer, model)

    for row in predictions:
        print(f"paper_id: {row['paper_id']}")
        print(f"ml_pred_label: {row['ml_pred_label']}")
        print("-" * 40)