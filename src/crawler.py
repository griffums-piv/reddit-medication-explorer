from datetime import datetime, timezone
from typing import Dict, Any, Iterable, List

import praw

from .config import Config
from .storage import append_jsonl, ensure_dir
from .analysis_stub import analyse_comments


def _iter_new_submissions(
    reddit: praw.Reddit, subreddit_name: str, config: Config
) -> Iterable[praw.models.Submission]:
    """Yield recent submissions from a subreddit within the lookback window."""
    subreddit = reddit.subreddit(subreddit_name)
    cutoff = datetime.now(timezone.utc) - config.lookback_timedelta

    count = 0
    for submission in subreddit.new(limit=config.max_posts_per_subreddit):
        created = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
        if created < cutoff:
            # Once we've stepped outside the lookback window we can stop
            break
        count += 1
        yield submission

    print(
        f"[crawler] {subreddit_name}: fetched {count} submissions "
        f"newer than {cutoff.isoformat()}"
    )


def _submission_to_dict(submission: praw.models.Submission) -> Dict[str, Any]:
    return {
        "id": submission.id,
        "subreddit": str(submission.subreddit),
        "title": submission.title,
        "selftext": submission.selftext,
        "created_utc": submission.created_utc,
        "score": submission.score,
        "num_comments": submission.num_comments,
        "author": str(submission.author) if submission.author else None,
        "permalink": submission.permalink,
        "url": submission.url,
    }


def _comment_to_dict(comment: praw.models.Comment) -> Dict[str, Any]:
    return {
        "id": comment.id,
        "submission_id": comment.submission.id,
        "subreddit": str(comment.subreddit),
        "body": comment.body,
        "created_utc": comment.created_utc,
        "score": comment.score,
        "author": str(comment.author) if comment.author else None,
        "parent_id": comment.parent_id,
        "permalink": comment.permalink,
    }


def crawl_subreddits(reddit: praw.Reddit, config: Config) -> None:
    """Fetch recent submissions + comments for each configured subreddit."""
    base_dir = ensure_dir(config.data_dir)

    for sub in config.subreddits:
        print(f"[crawler] Processing r/{sub}")
        submission_path = base_dir / f"{sub}_submissions.jsonl"
        comment_path = base_dir / f"{sub}_comments.jsonl"

        collected_comments: List[Dict[str, Any]] = []

        for submission in _iter_new_submissions(reddit, sub, config):
            # Store the submission itself
            append_jsonl(submission_path, _submission_to_dict(submission))

            # Fetch comments (simple, single pass)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                record = _comment_to_dict(comment)
                append_jsonl(comment_path, record)
                collected_comments.append(record)

        # Pass comments to analysis stub
        analyse_comments(collected_comments)
