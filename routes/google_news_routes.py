from flask import Blueprint, jsonify, request
from scrapers.google_news_scraper import GoogleNewsScraper
from cache import get_cached_trends, clear_platform_cache
import logging

logger = logging.getLogger(__name__)
googlenews_bp = Blueprint('googlenews', __name__)
googlenews_scraper = GoogleNewsScraper()

@googlenews_bp.route('/trends')
def get_trends():
    try:
        category = request.args.get('category', '')
        logger.info(f"Fetching Google News trends for category: {category}")
        trends = get_cached_trends('googlenews', googlenews_scraper.get_trends, category=category)
        return jsonify(trends)
    except Exception as e:
        logger.error(f"Error fetching Google News trends: {str(e)}")
        return jsonify([])

@googlenews_bp.route('/trends/<category>')
def get_trends_by_category(category):
    try:
        logger.info(f"Fetching Google News trends for category: {category}")
        trends = get_cached_trends('googlenews', googlenews_scraper.get_trends, category=category)
        return jsonify(trends)
    except Exception as e:
        logger.error(f"Error fetching Google News trends for category {category}: {str(e)}")
        return jsonify([])

@googlenews_bp.route('/clear-cache')
def clear_cache():
    try:
        category = request.args.get('category', '')
        logger.info(f"Clearing cache for Google News category: {category}")
        clear_platform_cache('googlenews', category)
        return jsonify({'status': 'success', 'message': f'Cache cleared for category {category}'})
    except Exception as e:
        logger.error(f"Error clearing Google News cache: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}) 