import praw
from datetime import datetime
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False

class RedditScraper:
    def __init__(self):
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent='TrendSphere/1.0'
            )
            logger.info("Reddit API initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Reddit client: {str(e)}")
            # Use mock data if API credentials are not available
            self.use_mock_data = True

    def get_trends(self, subreddit=None):
        try:
            # If API credentials are not available, return mock data
            if hasattr(self, 'use_mock_data'):
                return self.get_mock_trends(subreddit)

            trends = []
            if subreddit == 'memes':
                logger.info("Fetching memes from r/memes")
                posts = self.reddit.subreddit('memes').hot(limit=20)
            elif subreddit:
                logger.info(f"Fetching trends from subreddit: {subreddit}")
                posts = self.reddit.subreddit(subreddit).hot(limit=20)
            else:
                logger.info("Fetching trends from r/all")
                posts = self.reddit.subreddit('all').hot(limit=20)

            for index, post in enumerate(posts, 1):
                try:
                    # Get image URL if available
                    image_url = None
                    if hasattr(post, 'url') and post.url:
                        # Check if the URL is an image
                        if any(post.url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                            image_url = post.url
                        # Check if it's an imgur link
                        elif 'imgur.com' in post.url:
                            image_url = post.url + '.jpg' if not post.url.endswith('.jpg') else post.url

                    trend = {
                        'title': post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'subreddit': post.subreddit.display_name,
                        'created_at': post.created_utc,
                        'rank': index,
                        'platform': 'reddit',
                        'timestamp': datetime.now().isoformat(),
                        'image_url': image_url
                    }
                    logger.info(f"Successfully processed post: {trend['title']}")
                    trends.append(trend)
                except Exception as e:
                    logger.error(f"Error processing post {post.id}: {str(e)}")
                    continue

            return trends

        except Exception as e:
            logger.error(f"Error scraping Reddit trends: {str(e)}")
            return self.get_mock_trends(subreddit)

    def get_memes(self, limit=10):
        """Get trending memes from r/memes subreddit"""
        try:
            if hasattr(self, 'use_mock_data'):
                return self.get_mock_memes(limit)

            logger.info("Fetching memes from r/memes")
            memes = []
            posts = self.reddit.subreddit('memes').hot(limit=limit)

            for index, post in enumerate(posts, 1):
                try:
                    # Get image URL if available
                    image_url = None
                    if hasattr(post, 'url') and post.url:
                        # Check if the URL is an image
                        if any(post.url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                            image_url = post.url
                        # Check if it's an imgur link
                        elif 'imgur.com' in post.url:
                            image_url = post.url + '.jpg' if not post.url.endswith('.jpg') else post.url

                    meme = {
                        'title': post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'created_at': post.created_utc,
                        'rank': index,
                        'platform': 'reddit',
                        'timestamp': datetime.now().isoformat(),
                        'image_url': image_url
                    }
                    logger.info(f"Successfully processed meme: {meme['title']}")
                    memes.append(meme)
                except Exception as e:
                    logger.error(f"Error processing meme {post.id}: {str(e)}")
                    continue

            return memes

        except Exception as e:
            logger.error(f"Error scraping Reddit memes: {str(e)}")
            return self.get_mock_memes(limit)

    def get_mock_trends(self, subreddit=None):
        logger.warning(f"Using mock Reddit data for subreddit: {subreddit or 'all'}")
        
        # Base mock data
        mock_data = [
            {
                'title': 'The Future of AI: What to Expect in 2024',
                'url': 'https://reddit.com/r/technology/comments/sample1',
                'score': 15000,
                'comments': 2300,
                'subreddit': 'technology',
                'created_at': datetime.now().timestamp(),
                'rank': 1,
                'platform': 'reddit',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'Scientists Discover New Species in the Amazon',
                'url': 'https://reddit.com/r/science/comments/sample2',
                'score': 12000,
                'comments': 1800,
                'subreddit': 'science',
                'created_at': datetime.now().timestamp(),
                'rank': 2,
                'platform': 'reddit',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'Breaking: Major Tech Company Announces Revolutionary Product',
                'url': 'https://reddit.com/r/technology/comments/sample3',
                'score': 10000,
                'comments': 1500,
                'subreddit': 'technology',
                'created_at': datetime.now().timestamp(),
                'rank': 3,
                'platform': 'reddit',
                'timestamp': datetime.now().isoformat()
            }
        ]

        # Filter by subreddit if specified
        if subreddit:
            return [post for post in mock_data if post['subreddit'].lower() == subreddit.lower()]
        
        return mock_data

    def get_mock_memes(self, limit=10):
        """Return mock meme data for testing"""
        logger.warning("Using mock Reddit meme data")
        return [
            {
                'title': 'When you finally fix that bug',
                'url': 'https://reddit.com/r/memes/comments/sample1',
                'score': 15000,
                'comments': 2300,
                'created_at': datetime.now().timestamp(),
                'rank': 1,
                'platform': 'reddit',
                'timestamp': datetime.now().isoformat(),
                'image_url': 'https://via.placeholder.com/500x500?text=Mock+Meme+1'
            },
            {
                'title': 'Me explaining my code to the rubber duck',
                'url': 'https://reddit.com/r/memes/comments/sample2',
                'score': 12000,
                'comments': 1800,
                'created_at': datetime.now().timestamp(),
                'rank': 2,
                'platform': 'reddit',
                'timestamp': datetime.now().isoformat(),
                'image_url': 'https://via.placeholder.com/500x500?text=Mock+Meme+2'
            }
        ] 