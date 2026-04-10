#nalysis\rule_based_classifier.py    

import re
from typing import Dict, Iterable, List


topic_rules: Dict[str, List[str]] = {
    "AI": ["ai", "transformer", "llm", "bert", "deep learning", "neural network"],
    "의료": ["clinical", "diagnosis", "hospital", "patient", "medical"],
    "경영": ["marketing", "customer", "business", "platform", "strategy"],
}

sensitivity_rules: Dict[str, List[str]] = {
    "윤리": ["ethics", "bias", "fairness", "responsibility"],
    "규제": ["regulation", "policy", "compliance", "law"],
    "개인정보": ["privacy", "personal data", "consent", "security"],
}


def combine_title_and_summary(title: str, summary: str) -> str:
    return f"{title or ''} {summary or ''}".strip()


def classify_by_rules(text: str, rule_dict: Dict[str, Iterable[str]]) -> List[str]:
    text_lower = (text or "").lower()
    matched_labels: List[str] = []

    for label, keywords in rule_dict.items():
        for keyword in keywords:
            if contains_keyword(text_lower, keyword):
                matched_labels.append(label)
                break

    return matched_labels if matched_labels else ["기타"]


def contains_keyword(text: str, keyword: str) -> bool:
    pattern = rf"\b{re.escape(keyword.lower())}\b"
    return re.search(pattern, text) is not None


def format_labels(labels: List[str]) -> str:
    return ", ".join(labels)


def classify_papers_by_rules(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    classified_rows: List[Dict[str, str]] = []

    for paper in papers:
        combined_text = combine_title_and_summary(
            paper.get("title", ""),
            paper.get("summary", ""),
        )

        topic_labels = classify_by_rules(combined_text, topic_rules)
        sensitivity_labels = classify_by_rules(combined_text, sensitivity_rules)

        classified_rows.append(
            {
                **paper,
                "combined_text": combined_text,
                "topic_rule_label": format_labels(topic_labels),
                "sensitivity_rule_label": format_labels(sensitivity_labels),
            }
        )

    return classified_rows


if __name__ == "__main__":
    sample_papers = [
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

    results = classify_papers_by_rules(sample_papers)

    for row in results:
        print(f"paper_id: {row['paper_id']}")
        print(f"topic_rule_label: {row['topic_rule_label']}")
        print(f"sensitivity_rule_label: {row['sensitivity_rule_label']}")
        print("-" * 40)