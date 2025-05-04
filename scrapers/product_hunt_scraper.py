import feedparser
from datetime import datetime
import html
import requests
from bs4 import BeautifulSoup
import re
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False

class ProductHuntScraper:
    def __init__(self):
        self.feed_url = "https://www.producthunt.com/feed"
        self.base_url = "https://www.producthunt.com"
        # Use the local product_hunt.png file from the static directory
        self.default_image = "/static/platforms/product_hunt.png"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_product_image_url(self, product_url):
        try:
            response = requests.get(product_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            og_image = soup.find('meta', property='og:image')
            if og_image:
                return og_image['content']
            return self.default_image
        except Exception as e:
            logger.error(f"Error fetching product image: {str(e)}")
            return self.default_image

    def extract_image_url(self, entry):
        # Try to get image from media content
        if 'media_content' in entry:
            for media in entry.get('media_content', []):
                if media.get('url'):
                    return media['url']
        
        # Try to get image from content
        if 'content' in entry:
            content = entry.get('content', [{}])[0].get('value', '')
            img_match = re.search(r'<img[^>]+src="([^">]+)"', content)
            if img_match:
                return img_match.group(1)
        
        # Try to get image from summary
        if 'summary' in entry:
            img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.summary)
            if img_match:
                return img_match.group(1)
        
        return self.default_image

    def get_trends(self):
        try:
            feed = feedparser.parse(self.feed_url)
            trends = []

            for index, entry in enumerate(feed.entries[:20], 1):
                # Get product URL
                product_url = entry.link
                
                # Get image URL using the new method
                thumbnail_url = self.get_product_image_url(product_url)
                
                # If the new method fails, fall back to the old method
                if thumbnail_url == self.default_image:
                    thumbnail_url = self.extract_image_url(entry)
                
                try:
                    response = requests.get(product_url, headers=self.headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract votes and comments
                    votes_count = 0
                    comments_count = 0
                    maker_name = entry.get('author', 'Unknown')
                    
                    # Try to get votes
                    votes_elem = soup.select_one('[data-test="vote-button"]')
                    if votes_elem:
                        votes_text = votes_elem.text.strip()
                        votes_count = int(''.join(filter(str.isdigit, votes_text)) or 0)
                    
                    # Try to get comments
                    comments_elem = soup.select_one('[data-test="comment-count"]')
                    if comments_elem:
                        comments_text = comments_elem.text.strip()
                        comments_count = int(''.join(filter(str.isdigit, comments_text)) or 0)
                    
                except Exception as e:
                    logger.error(f"Error fetching product details: {str(e)}")
                
                # Clean up the description
                description = entry.get('description', '')
                if description:
                    # Remove HTML tags
                    description = re.sub(r'<[^>]+>', '', description)
                    # Unescape HTML entities
                    description = html.unescape(description)
                    # Truncate if too long
                    description = description[:200] + '...' if len(description) > 200 else description
                
                trend = {
                    'name': html.unescape(entry.title),
                    'tagline': description,
                    'url': entry.link,
                    'thumbnail_url': thumbnail_url,
                    'maker_name': maker_name,
                    'votes_count': votes_count,
                    'comments_count': comments_count,
                    'created_at': entry.published,
                    'rank': index,
                    'platform': 'producthunt'
                }
                trends.append(trend)

            return trends

        except Exception as e:
            logger.error(f"Error scraping Product Hunt trends: {str(e)}")
            raise 