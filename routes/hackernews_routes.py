from flask import Blueprint, jsonify
from scrapers.hackernews_scraper import HackerNewsScraper
from cache import get_cached_trends

hackernews_bp = Blueprint('hackernews', __name__)
hackernews_scraper = HackerNewsScraper()

@hackernews_bp.route('/trends')
def get_trends():
    try:
        trends = get_cached_trends('hackernews', hackernews_scraper.get_trends)
        return jsonify(trends)
    except Exception as e:
        return jsonify([])

@hackernews_bp.route('/trends/<category>')
def get_trends_by_category(category):
    try:
        trends = get_cached_trends('hackernews', hackernews_scraper.get_trends, category)
        return jsonify(trends)
    except Exception as e:
        return jsonify([]) 