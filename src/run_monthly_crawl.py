from src.config import Config
from src.reddit_client import make_reddit_client
from src.crawler import crawl_subreddits


def main() -> None:
    config = Config.from_env()
    reddit = make_reddit_client(config)
    crawl_subreddits(reddit, config)


if __name__ == "__main__":
    main()
