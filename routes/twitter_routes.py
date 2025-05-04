from flask import Blueprint, jsonify, request
from scrapers.twitter_scraper import TwitterScraper
from cache import get_cached_trends

twitter_bp = Blueprint('twitter', __name__)
twitter_scraper = TwitterScraper()

@twitter_bp.route('/trends')
def get_trends():
    try:
        category = request.args.get('category', 'all')
        trends = get_cached_trends('twitter', twitter_scraper.get_trends, category)
        return jsonify(trends)
    except Exception as e:
        return jsonify([])

@twitter_bp.route('/categories')
def get_categories():
    try:
        return jsonify({
            'status': 'success',
            'categories': twitter_scraper.categories
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@twitter_bp.route('/trends/<woeid>')
def get_trends_by_location(woeid):
    try:
        trends = get_cached_trends('twitter', twitter_scraper.get_trends_by_location, woeid)
        return jsonify(trends)  # Return just the trends array
    except Exception as e:
        return jsonify([])  # Return empty array on error

@twitter_bp.route('/trend/<trend_title>')
def get_trend_details(trend_title):
    try:
        details = twitter_scraper.get_statistics(trend_title)
        return jsonify({
            'status': 'success',
            'data': details,
            'message': 'Trend details retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 