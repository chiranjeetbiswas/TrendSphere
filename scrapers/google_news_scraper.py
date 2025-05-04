import feedparser
from datetime import datetime
import html
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False

class GoogleNewsScraper:
    def __init__(self):
        self.base_url = "https://news.google.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.valid_categories = {
            '': 'Top Stories',
            'WORLD': 'World',
            'NATION': 'Nation',
            'BUSINESS': 'Business',
            'TECHNOLOGY': 'Technology',
            'ENTERTAINMENT': 'Entertainment',
            'SPORTS': 'Sports',
            'SCIENCE': 'Science',
            'HEALTH': 'Health'
        }

    def clean_description(self, description):
        if not description:
            return ""
        # Remove HTML tags but keep the text
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text()
        # Limit description length
        return text[:200] + '...' if len(text) > 200 else text

    def get_source(self, entry):
        try:
            source = entry.get('source', {}).get('title', 'Unknown')
            if not source or source == 'Unknown':
                # Try to extract source from the URL
                parsed_url = urlparse(entry.link)
                source = parsed_url.netloc.replace('www.', '')
            return source
        except:
            return "Google News"

    def get_image_url(self, entry):
        try:
            # Try to get image from media_content if available
            if hasattr(entry, 'media_content') and entry.media_content:
                for media in entry.media_content:
                    if media.get('type', '').startswith('image/'):
                        return media.get('url', '')
            
            # Try to get image from description
            if hasattr(entry, 'description'):
                soup = BeautifulSoup(entry.description, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    return img['src']
            
            # Try to fetch image from the article URL
            response = requests.get(entry.link, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Look for Open Graph or Twitter card images
                og_image = soup.find('meta', property='og:image')
                if og_image:
                    return og_image.get('content', '')
                twitter_image = soup.find('meta', name='twitter:image')
                if twitter_image:
                    return twitter_image.get('content', '')
                # Fallback to first image in article
                img = soup.find('img')
                if img and img.get('src'):
                    return img['src']
        except:
            pass
        return 'https://via.placeholder.com/1280x720?text=No+Image'

    def get_trends(self, category=None):
        try:
            # If category is not specified or not valid, use default
            if category and category.upper() not in self.valid_categories:
                category = ''
                logger.warning(f"Invalid category '{category}', using default")

            # Construct URL based on category
            url = f"{self.base_url}/rss"
            if category:
                url = f"{self.base_url}/rss/headlines/section/topic/{category.upper()}"
            
            logger.info(f"Fetching Google News trends for category: {self.valid_categories.get(category.upper() if category else '', 'Top Stories')}")
            
            feed = feedparser.parse(url)
            
            if not feed.entries:
                logger.warning("No entries found in feed")
                return self.get_mock_trends(category)
            
            trends = []
            for index, entry in enumerate(feed.entries[:10], 1):
                try:
                    title = html.unescape(entry.title)
                    link = entry.link
                    description = self.clean_description(entry.get('description', ''))
                    source = self.get_source(entry)
                    image_url = self.get_image_url(entry)
                    pub_date = entry.published if hasattr(entry, 'published') else datetime.now().isoformat()
                    
                    trend = {
                        'title': title,
                        'url': link,
                        'description': description,
                        'source': source,
                        'image_url': image_url,
                        'category': self.valid_categories.get(category.upper() if category else '', 'Top Stories'),
                        'published_at': pub_date,
                        'rank': index,
                        'platform': 'googlenews',
                        'timestamp': datetime.now().isoformat()
                    }
                    trends.append(trend)
                except Exception as e:
                    logger.error(f"Error processing news item: {str(e)}")
                    continue
            
            return trends

        except Exception as e:
            logger.error(f"Error scraping Google News: {str(e)}")
            return self.get_mock_trends(category)

    def get_mock_trends(self, category=None):
        logger.warning(f"Using mock Google News data for category: {self.valid_categories.get(category.upper() if category else '', 'Top Stories')}")
        
        # Base mock data
        mock_data = [
            {
                'title': 'Major Tech Company Announces Revolutionary AI Breakthrough',
                'url': 'https://news.google.com/articles/sample1',
                'description': 'A leading tech company has unveiled a groundbreaking AI system that promises to revolutionize multiple industries.',
                'source': 'Tech News Daily',
                'image_url': 'https://via.placeholder.com/1280x720?text=AI+Breakthrough',
                'category': 'Technology',
                'published_at': datetime.now().isoformat(),
                'rank': 1,
                'platform': 'googlenews',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'Global Markets React to New Economic Policies',
                'url': 'https://news.google.com/articles/sample2',
                'description': 'Financial markets worldwide show mixed reactions to the latest economic policy announcements.',
                'source': 'Financial Times',
                'image_url': 'https://via.placeholder.com/1280x720?text=Markets',
                'category': 'Business',
                'published_at': datetime.now().isoformat(),
                'rank': 2,
                'platform': 'googlenews',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'Scientists Discover New Species in the Amazon Rainforest',
                'url': 'https://news.google.com/articles/sample3',
                'description': 'Researchers have identified a previously unknown species of amphibian in the Amazon rainforest.',
                'source': 'Science Daily',
                'image_url': 'https://via.placeholder.com/1280x720?text=New+Species',
                'category': 'Science',
                'published_at': datetime.now().isoformat(),
                'rank': 3,
                'platform': 'googlenews',
                'timestamp': datetime.now().isoformat()
            }
        ]

        # Filter by category if specified
        if category and category.upper() in self.valid_categories:
            category_name = self.valid_categories[category.upper()]
            return [news for news in mock_data if news['category'] == category_name]
        
        return mock_data 