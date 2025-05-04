import feedparser
from datetime import datetime
import time
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False

class HackerNewsScraper:
    def __init__(self):
        self.feed_url = "https://news.ycombinator.com/rss"

    def get_trends(self):
        try:
            feed = feedparser.parse(self.feed_url)
            trends = []

            for index, entry in enumerate(feed.entries[:20], 1):
                # Parse the points and comments from the title if available
                points = 0
                comments = 0
                
                trend = {
                    'title': entry.title,
                    'url': entry.link,
                    'author': entry.get('author', 'Unknown'),
                    'points': points,
                    'comments': comments,
                    'published': entry.published,
                    'rank': index,
                    'timestamp': datetime.now().isoformat(),
                    'platform': 'hackernews'
                }
                trends.append(trend)

            return trends

        except Exception as e:
            logger.error(f"Error scraping HackerNews trends: {str(e)}")
            raise 