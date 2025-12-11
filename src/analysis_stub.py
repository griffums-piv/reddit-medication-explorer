from typing import Iterable, Dict, Any


def analyse_comments(comments: Iterable[Dict[str, Any]]) -> None:
    """
    Placeholder for offline NLP / ML analysis.

    In the exploratory phase this might:
    - Identify medication mentions in comment text.
    - Classify comments into categories (effectiveness, side effects, etc.).
    - Produce aggregate statistics stored in a separate file or database.

    This stub is intentionally minimal and does not perform heavy computation yet.
    """
    # For now, just count the comments
    count = 0
    for _ in comments:
        count += 1

    print(f"[analysis_stub] Received {count} comments for analysis.")
