from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'message': 'IP Geolocation API is running!',
        'endpoints': {
            '/geo': 'GET - Get geolocation data for client IP',
            '/geo/<ip>': 'GET - Get geolocation data for specific IP'
        }
    })

@app.route('/geo', methods=['GET'])
def geo_info():
    """Get geolocation info for client's IP"""
    try:
        # Get client's IP address
        # Check for forwarded IPs first (common in production)
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            # Take the first IP if there are multiple
            client_ip = client_ip.split(',')[0].strip()
        
        # For local development, use a public IP for testing
        if client_ip in ['127.0.0.1', 'localhost', '::1']:
            client_ip = '8.8.8.8'  # Google's DNS for testing
        
        return get_location_data(client_ip)
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to get geolocation data',
            'message': str(e)
        }), 500

@app.route('/geo/<ip>', methods=['GET'])
def geo_info_by_ip(ip):
    """Get geolocation info for a specific IP"""
    try:
        return get_location_data(ip)
    except Exception as e:
        return jsonify({
            'error': 'Failed to get geolocation data',
            'message': str(e)
        }), 500

def get_location_data(ip):
    """Fetch geolocation data from external API"""
    try:
        # Using ip-api.com (free, no API key required)
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'fail':
            return jsonify({
                'error': 'Invalid IP address',
                'ip': ip,
                'message': data.get('message', 'Unknown error')
            }), 400
        
        # Format the response
        geo_data = {
            'ip': ip,
            'country': data.get('country'),
            'country_code': data.get('countryCode'),
            'region': data.get('regionName'),
            'region_code': data.get('region'),
            'city': data.get('city'),
            'zip_code': data.get('zip'),
            'latitude': data.get('lat'),
            'longitude': data.get('lon'),
            'timezone': data.get('timezone'),
            'isp': data.get('isp'),
            'organization': data.get('org'),
            'as_number': data.get('as'),
            'query_time': datetime.utcnow().isoformat() + 'Z'
        }
        
        return jsonify(geo_data)
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to fetch geolocation data',
            'ip': ip,
            'message': str(e)
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'ip': ip,
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Available endpoints: /, /geo, /geo/<ip>'
    }), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)