from flask import Blueprint, jsonify, request
from scrapers.product_hunt_scraper import ProductHuntScraper
from cache import get_cached_trends, clear_platform_cache
import logging

logger = logging.getLogger(__name__)
producthunt_bp = Blueprint('producthunt', __name__)
producthunt_scraper = ProductHuntScraper()

@producthunt_bp.route('/trends')
def get_trends():
    try:
        logger.info("Fetching Product Hunt trends")
        trends = get_cached_trends('producthunt', producthunt_scraper.get_trends)
        return jsonify({
            'status': 'success',
            'data': trends
        })
    except Exception as e:
        logger.error(f"Error fetching Product Hunt trends: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': []
        })

@producthunt_bp.route('/trends/<category>')
def get_trends_by_category(category):
    try:
        logger.info(f"Fetching Product Hunt trends for category: {category}")
        trends = get_cached_trends('producthunt', producthunt_scraper.get_trends, category=category)
        return jsonify(trends)
    except Exception as e:
        logger.error(f"Error fetching Product Hunt trends for category {category}: {str(e)}")
        return jsonify([])

@producthunt_bp.route('/clear-cache')
def clear_cache():
    try:
        logger.info("Clearing Product Hunt cache")
        clear_platform_cache('producthunt')
        return jsonify({
            'status': 'success',
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        logger.error(f"Error clearing Product Hunt cache: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }) 