from flask import Blueprint, jsonify, request
from scrapers.reddit_scraper import RedditScraper
from cache import get_cached_trends, clear_platform_cache
import logging

logger = logging.getLogger(__name__)
reddit_bp = Blueprint('reddit', __name__)
reddit_scraper = RedditScraper()

@reddit_bp.route('/trends')
def get_trends():
    try:
        subreddit = request.args.get('subreddit', 'all')
        logger.info(f"Fetching Reddit trends for subreddit: {subreddit}")
        trends = get_cached_trends('reddit', reddit_scraper.get_trends, subreddit=subreddit)
        return jsonify(trends)
    except Exception as e:
        logger.error(f"Error fetching Reddit trends: {str(e)}")
        return jsonify([])

@reddit_bp.route('/trends/<subreddit>')
def get_trends_by_subreddit(subreddit):
    try:
        logger.info(f"Fetching Reddit trends for subreddit: {subreddit}")
        trends = get_cached_trends('reddit', reddit_scraper.get_trends, subreddit=subreddit)
        return jsonify(trends)
    except Exception as e:
        logger.error(f"Error fetching Reddit trends for subreddit {subreddit}: {str(e)}")
        return jsonify([])

@reddit_bp.route('/memes')
def get_memes():
    try:
        logger.info("Fetching trending memes from r/memes")
        limit = request.args.get('limit', 10, type=int)
        memes = get_cached_trends('reddit_memes', reddit_scraper.get_memes, limit=limit)
        return jsonify(memes)
    except Exception as e:
        logger.error(f"Error fetching Reddit memes: {str(e)}")
        return jsonify([])

@reddit_bp.route('/clear-cache')
def clear_cache():
    try:
        subreddit = request.args.get('subreddit', 'all')
        logger.info(f"Clearing cache for Reddit subreddit: {subreddit}")
        clear_platform_cache('reddit', subreddit=subreddit)
        return jsonify({'status': 'success', 'message': f'Cache cleared for subreddit {subreddit}'})
    except Exception as e:
        logger.error(f"Error clearing Reddit cache: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}) 