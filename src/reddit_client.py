import praw

from .config import Config


def make_reddit_client(config: Config) -> praw.Reddit:
    """Create an authenticated PRAW Reddit client."""
    reddit = praw.Reddit(
        client_id=config.reddit_client_id,
        client_secret=config.reddit_client_secret,
        username=config.reddit_username,
        password=config.reddit_password,
        user_agent=config.reddit_user_agent,
    )
    return reddit
