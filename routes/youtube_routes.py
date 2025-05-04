from flask import Blueprint, jsonify, request
from scrapers.youtube_scraper import YouTubeScraper
from cache import get_cached_trends, clear_platform_cache

youtube_bp = Blueprint('youtube', __name__)
youtube_scraper = YouTubeScraper()

@youtube_bp.route('/trends')
def get_trends():
    try:
        region = request.args.get('region')
        trends = get_cached_trends('youtube', youtube_scraper.get_trends, region=region)
        return jsonify(trends)
    except Exception as e:
        return jsonify([])

@youtube_bp.route('/trends/<region>')
def get_trends_by_region(region):
    try:
        trends = get_cached_trends('youtube', youtube_scraper.get_trends, region=region)
        return jsonify(trends)
    except Exception as e:
        return jsonify([])

@youtube_bp.route('/clear-cache')
def clear_cache():
    try:
        region = request.args.get('region')
        clear_platform_cache('youtube', region)
        return jsonify({'status': 'success', 'message': f'Cache cleared for region {region}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})