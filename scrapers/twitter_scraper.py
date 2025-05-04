from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False

class TwitterScraper:
    def __init__(self):
        self.base_url = "https://trends24.in/india/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.categories = {
            'all': 'All Trends',
            'entertainment': 'Entertainment',
            'sports': 'Sports',
            'politics': 'Politics',
            'technology': 'Technology',
            'business': 'Business'
        }

    def get_trends(self, category='all'):
        try:
            url = self.base_url
            if category != 'all':
                url = f"{self.base_url}{category}/"
            logger.info(f"Fetching trends from: {url}")
            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'  # Ensure correct decoding
            soup = BeautifulSoup(response.text, 'html.parser')
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            trends = []
            trend_elements = soup.select('.trend-card__list li')[:20]  # Limit to top 20 trends
            
            for idx, element in enumerate(trend_elements, 1):
                try:
                    title = element.select_one('a')
                    title_text = title.text.strip() if title else "Unknown Title"
                    
                    # Get tweet volume if available
                    volume_elem = element.select_one('.trend-card__meta')
                    tweet_volume = None
                    if volume_elem:
                        volume_text = volume_elem.text.strip()
                        if 'K' in volume_text:
                            tweet_volume = int(float(volume_text.replace('K', '')) * 1000)
                        elif 'M' in volume_text:
                            tweet_volume = int(float(volume_text.replace('M', '')) * 1000000)
                        else:
                            tweet_volume = int(volume_text.replace(',', ''))
                    
                    # Get related hashtags
                    hashtags = []
                    hashtag_elements = element.select('.trend-card__hashtags a')
                    for tag in hashtag_elements:
                        hashtags.append(tag.text.strip())
                    
                    # Get trend URL
                    trend_url = title['href'] if title and 'href' in title.attrs else None
                    
                    # Calculate growth based on rank
                    growth = f"+{10 - idx}%" if idx <= 10 else "0%"
                    
                    trend = {
                        'title': title_text,
                        'rank': idx,
                        'platform': 'twitter',
                        'growth': growth,
                        'tweet_volume': tweet_volume,
                        'hashtags': hashtags,
                        'trend_url': trend_url,
                        'category': self.categories.get(category, 'All Trends'),
                        'timestamp': datetime.now().isoformat()
                    }
                    trends.append(trend)
                except Exception as e:
                    logger.error(f"Error processing trend element: {str(e)}")
                    continue
            
            if not trends:
                logger.warning("No trends were found in the HTML")
                return self.get_mock_trends()
            
            return trends

        except requests.RequestException as e:
            logger.error(f"Network error while fetching trends: {str(e)}")
            return self.get_mock_trends()
        except Exception as e:
            logger.error(f"Unexpected error while scraping Twitter trends: {str(e)}")
            return self.get_mock_trends()

    def get_statistics(self, trend_title):
        """Get detailed statistics for a specific trend"""
        try:
            # Generate mock statistics for demonstration
            tweets = []
            for i in range(5):  # Generate 5 sample tweets
                tweet = {
                    'text': f'Sample tweet about {trend_title} #{i+1}',
                    'author': f'User{i+1}',
                    'stats': {
                        'replies': random.randint(10, 1000),
                        'retweets': random.randint(100, 5000),
                        'likes': random.randint(500, 10000),
                        'views': random.randint(1000, 50000)
                    },
                    'timestamp': datetime.now().isoformat()
                }
                tweets.append(tweet)

            return {
                'trend_title': trend_title,
                'tweets': tweets,
                'total_tweets': len(tweets),
                'timestamp': datetime.now().isoformat(),
                'platform': 'twitter'
            }
        except Exception as e:
            logger.error(f"Error getting tweet statistics: {e}")
            return {
                'trend_title': trend_title,
                'tweets': [],
                'total_tweets': 0,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'platform': 'twitter'
            }

    def get_mock_trends(self):
        return [
            {
                'title': 'Sample Twitter Trend 1',
                'rank': 1,
                'platform': 'twitter',
                'growth': '+9%',
                'tweet_volume': 150000,
                'hashtags': ['#trend1', '#trending'],
                'trend_url': 'https://twitter.com/search?q=Sample%20Trend%201',
                'category': 'All Trends',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'Sample Twitter Trend 2',
                'rank': 2,
                'platform': 'twitter',
                'growth': '+8%',
                'tweet_volume': 120000,
                'hashtags': ['#trend2', '#viral'],
                'trend_url': 'https://twitter.com/search?q=Sample%20Trend%202',
                'category': 'All Trends',
                'timestamp': datetime.now().isoformat()
            }
        ]
    

    def get_mock_trend_details(self, trend_title):
        return {
            'title': trend_title,
            'tweet_volume': 125000,
            'tweets': [
                {
                    'text': f'Sample tweet about {trend_title} #1',
                    'likes': 1500,
                    'retweets': 500
                },
                {
                    'text': f'Sample tweet about {trend_title} #2',
                    'likes': 1200,
                    'retweets': 300
                }
            ]
        }