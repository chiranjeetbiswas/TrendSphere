from datetime import datetime
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False

class YouTubeScraper:
    def __init__(self):
        load_dotenv()  # Load environment variables
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.region = os.getenv('YOUTUBE_REGION', 'US')  # Default to US if not specified
        if not self.api_key:
            logger.warning("YouTube API key not found in environment variables - using mock data")
            self.youtube = None
        else:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logger.info("YouTube API initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing YouTube API: {str(e)}")
                self.youtube = None

    def get_trends(self, region=None):
        try:
            if not self.youtube:
                logger.warning("YouTube API not initialized - using mock data")
                return self.get_mock_trends()

            logger.info(f"Fetching trending videos from YouTube for region: {region or self.region}")
            request = self.youtube.videos().list(
                part='snippet,statistics',
                chart='mostPopular',
                regionCode=region or self.region,
                maxResults=10
            )
            response = request.execute()

            if not response.get('items'):
                logger.warning("No videos found in YouTube API response")
                return self.get_mock_trends()

            trends = []
            for index, item in enumerate(response['items'], 1):
                try:
                    snippet = item['snippet']
                    statistics = item['statistics']
                    
                    # Get the best quality thumbnail available
                    thumbnails = snippet['thumbnails']
                    thumbnail_url = None
                    
                    # Try different thumbnail qualities in order of preference
                    for quality in ['maxres', 'high', 'medium', 'default']:
                        if quality in thumbnails and 'url' in thumbnails[quality]:
                            thumbnail_url = thumbnails[quality]['url']
                            break
                    
                    if not thumbnail_url:
                        logger.warning(f"No thumbnail found for video {item['id']}")
                        thumbnail_url = 'https://via.placeholder.com/1280x720?text=No+Thumbnail'

                    video_data = {
                        'title': snippet['title'],
                        'description': snippet['description'][:200] + '...' if len(snippet['description']) > 200 else snippet['description'],
                        'views': int(statistics.get('viewCount', 0)),
                        'likes': int(statistics.get('likeCount', 0)),
                        'comments': int(statistics.get('commentCount', 0)),
                        'thumbnail': thumbnail_url,
                        'video_id': item['id'],
                        'url': f"https://www.youtube.com/watch?v={item['id']}",
                        'channel_title': snippet['channelTitle'],
                        'published_at': snippet['publishedAt'],
                        'rank': index,
                        'platform': 'youtube',
                        'timestamp': datetime.now().isoformat()
                    }
                    trends.append(video_data)
                except Exception as e:
                    logger.error(f"Error processing video {item.get('id', 'unknown')}: {str(e)}")
                    continue

            return trends

        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return self.get_mock_trends()
        except Exception as e:
            logger.error(f"Error fetching YouTube trends: {str(e)}")
            return self.get_mock_trends()

    def get_mock_trends(self):
        logger.warning("Using mock YouTube data")
        return [
            {
                'title': 'Top 10 Tech Gadgets of 2024',
                'description': 'Check out the most innovative tech gadgets that are changing the game in 2024!',
                'views': 1250000,
                'likes': 50000,
                'comments': 2500,
                'thumbnail': 'https://i.ytimg.com/vi/sample1/maxresdefault.jpg',
                'video_id': 'sample1',
                'url': 'https://www.youtube.com/watch?v=sample1',
                'channel_title': 'Tech Reviews',
                'published_at': datetime.now().isoformat(),
                'rank': 1,
                'platform': 'youtube',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'How to Build a Website in 2024',
                'description': 'Learn how to create a modern website using the latest web technologies and best practices.',
                'views': 950000,
                'likes': 40000,
                'comments': 2000,
                'thumbnail': 'https://i.ytimg.com/vi/sample2/maxresdefault.jpg',
                'video_id': 'sample2',
                'url': 'https://www.youtube.com/watch?v=sample2',
                'channel_title': 'Web Development Tutorials',
                'published_at': datetime.now().isoformat(),
                'rank': 2,
                'platform': 'youtube',
                'timestamp': datetime.now().isoformat()
            },
            {
                'title': 'The Future of AI: What to Expect in 2024',
                'description': 'Exploring the latest developments in artificial intelligence and what they mean for our future.',
                'views': 800000,
                'likes': 35000,
                'comments': 1800,
                'thumbnail': 'https://i.ytimg.com/vi/sample3/maxresdefault.jpg',
                'video_id': 'sample3',
                'url': 'https://www.youtube.com/watch?v=sample3',
                'channel_title': 'AI Insights',
                'published_at': datetime.now().isoformat(),
                'rank': 3,
                'platform': 'youtube',
                'timestamp': datetime.now().isoformat()
            }
        ] 