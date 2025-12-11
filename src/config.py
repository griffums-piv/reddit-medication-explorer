import os
from dataclasses import dataclass
from datetime import timedelta

from dotenv import load_dotenv

# Load variables from a .env file if present
load_dotenv()


@dataclass
class Config:
    reddit_client_id: str
    reddit_client_secret: str
    reddit_username: str
    reddit_password: str
    reddit_user_agent: str

    subreddits: list[str]
    lookback_days: int
    max_posts_per_subreddit: int

    data_dir: str = "data/raw"

    @classmethod
    def from_env(cls) -> "Config":
        subreddits = os.getenv(
            "MED_EXPLORER_SUBREDDITS",
            "diabetes,Hypertension,ADHD,depression,AskDocs",
        )
        return cls(
            reddit_client_id=os.environ["REDDIT_CLIENT_ID"],
            reddit_client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            reddit_username=os.environ["REDDIT_USERNAME"],
            reddit_password=os.environ["REDDIT_PASSWORD"],
            reddit_user_agent=os.environ.get(
                "REDDIT_USER_AGENT",
                "med-explorer/0.1 by YOUR_USERNAME",
            ),
            subreddits=[s.strip() for s in subreddits.split(",") if s.strip()],
            lookback_days=int(os.getenv("MED_EXPLORER_LOOKBACK_DAYS", "30")),
            max_posts_per_subreddit=int(
                os.getenv("MED_EXPLORER_MAX_POSTS_PER_SUB", "200")
            ),
        )

    @property
    def lookback_timedelta(self) -> timedelta:
        return timedelta(days=self.lookback_days)
