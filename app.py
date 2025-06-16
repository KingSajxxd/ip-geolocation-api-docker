from flask import Flask, request, jsonify, render_template_string
import requests
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mysql'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'geouser'),
    'password': os.environ.get('DB_PASSWORD', 'geopassword'),
    'database': os.environ.get('DB_NAME', 'geolocation_db'),
    'charset': 'utf8mb4',
    'autocommit': True
}

# HTML Template for Frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌍 IP Geolocation Lookup</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 30px;
        }
        
        .search-section {
            margin-bottom: 30px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 15px 25px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        .my-location-btn {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            width: 100%;
            margin-bottom: 20px;
        }
        
        .result-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-top: 20px;
            display: none;
        }
        
        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .info-label {
            font-weight: bold;
            color: #495057;
            font-size: 14px;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 18px;
            color: #212529;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .history-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e9ecef;
        }
        
        .history-item {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .history-item:hover {
            transform: translateX(5px);
        }
        
        .history-ip {
            font-weight: bold;
            color: #212529;
        }
        
        .history-location {
            color: #6c757d;
            font-size: 14px;
        }
        
        .history-time {
            color: #adb5bd;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 IP Geolocation Lookup</h1>
            <p>Discover the location of any IP address instantly</p>
        </div>
        
        <div class="content">
            <div class="search-section">
                <button class="my-location-btn" onclick="getMyLocation()">
                    📍 Get My Location
                </button>
                
                <div class="input-group">
                    <input type="text" id="ipInput" placeholder="Enter IP address (e.g., 8.8.8.8)" 
                           onkeypress="handleKeyPress(event)">
                    <button onclick="lookupIP()">🔍 Lookup</button>
                </div>
            </div>
            
            <div id="loading" class="loading" style="display: none;">
                <h3>🔄 Looking up location...</h3>
            </div>
            
            <div id="error" class="error" style="display: none;"></div>
            
            <div id="result" class="result-card">
                <h3 style="margin-bottom: 20px; color: #495057;">📍 Location Details</h3>
                <div id="resultContent" class="result-grid"></div>
            </div>
            
            <div class="history-section">
                <h3 style="margin-bottom: 20px; color: #495057;">📚 Recent Lookups</h3>
                <div id="history"></div>
            </div>
        </div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        function showError(message) {
            hideLoading();
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            document.getElementById('result').style.display = 'none';
        }
        
        function showResult(data) {
            hideLoading();
            document.getElementById('error').style.display = 'none';
            
            const resultDiv = document.getElementById('result');
            const contentDiv = document.getElementById('resultContent');
            
            contentDiv.innerHTML = `
                <div class="info-item">
                    <div class="info-label">🖥️ IP Address</div>
                    <div class="info-value">${data.ip}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🏙️ City</div>
                    <div class="info-value">${data.city || 'N/A'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🏛️ Region</div>
                    <div class="info-value">${data.region || 'N/A'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🇺🇸 Country</div>
                    <div class="info-value">${data.country} (${data.country_code})</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📍 Coordinates</div>
                    <div class="info-value">${data.latitude}°, ${data.longitude}°</div>
                </div>
                <div class="info-item">
                    <div class="info-label">⏰ Timezone</div>
                    <div class="info-value">${data.timezone || 'N/A'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🌐 ISP</div>
                    <div class="info-value">${data.isp || 'N/A'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🏢 Organization</div>
                    <div class="info-value">${data.organization || 'N/A'}</div>
                </div>
            `;
            
            resultDiv.style.display = 'block';
            loadHistory();
        }
        
        async function getMyLocation() {
            showLoading();
            try {
                const response = await fetch('/geo');
                const data = await response.json();
                
                if (response.ok) {
                    showResult(data);
                } else {
                    showError(data.message || 'Failed to get location');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        }
        
        async function lookupIP() {
            const ip = document.getElementById('ipInput').value.trim();
            if (!ip) {
                showError('Please enter an IP address');
                return;
            }
            
            showLoading();
            try {
                const response = await fetch(`/geo/${ip}`);
                const data = await response.json();
                
                if (response.ok) {
                    showResult(data);
                    document.getElementById('ipInput').value = '';
                } else {
                    showError(data.message || 'Failed to lookup IP');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        }
        
        async function loadHistory() {
            try {
                const response = await fetch('/history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('history');
                if (data.length === 0) {
                    historyDiv.innerHTML = '<p style="color: #6c757d; text-align: center;">No recent lookups</p>';
                    return;
                }
                
                historyDiv.innerHTML = data.map(item => `
                    <div class="history-item" onclick="lookupFromHistory('${item.ip}')">
                        <div class="history-ip">${item.ip}</div>
                        <div class="history-location">${item.city}, ${item.country}</div>
                        <div class="history-time">${new Date(item.query_time).toLocaleString()}</div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Failed to load history:', error);
            }
        }
        
        function lookupFromHistory(ip) {
            document.getElementById('ipInput').value = ip;
            lookupIP();
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                lookupIP();
            }
        }
        
        // Load history on page load
        window.onload = loadHistory;
    </script>
</body>
</html>
"""

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database and create tables"""
    try:
        connection = get_db_connection()
        if not connection:
            return False
            
        cursor = connection.cursor()
        
        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ip_lookups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip VARCHAR(45) NOT NULL,
            country VARCHAR(100),
            country_code VARCHAR(10),
            region VARCHAR(100),
            region_code VARCHAR(10),
            city VARCHAR(100),
            zip_code VARCHAR(20),
            latitude DECIMAL(10, 7),
            longitude DECIMAL(10, 7),
            timezone VARCHAR(100),
            isp TEXT,
            organization TEXT,
            as_number VARCHAR(100),
            query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_ip (ip),
            INDEX idx_query_time (query_time)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        logger.info("Database initialized successfully")
        return True
        
    except Error as e:
        logger.error(f"Database initialization error: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def save_lookup_to_db(geo_data):
    """Save IP lookup data to database"""
    try:
        connection = get_db_connection()
        if not connection:
            return False
            
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO ip_lookups 
        (ip, country, country_code, region, region_code, city, zip_code, 
         latitude, longitude, timezone, isp, organization, as_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            geo_data.get('ip'),
            geo_data.get('country'),
            geo_data.get('country_code'),
            geo_data.get('region'),
            geo_data.get('region_code'),
            geo_data.get('city'),
            geo_data.get('zip_code'),
            geo_data.get('latitude'),
            geo_data.get('longitude'),
            geo_data.get('timezone'),
            geo_data.get('isp'),
            geo_data.get('organization'),
            geo_data.get('as_number')
        )
        
        cursor.execute(insert_query, values)
        connection.commit()
        return True
        
    except Error as e:
        logger.error(f"Database save error: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_lookup_history(limit=10):
    """Get recent IP lookup history from database"""
    try:
        connection = get_db_connection()
        if not connection:
            return []
            
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT ip, country, city, query_time 
        FROM ip_lookups 
        ORDER BY query_time DESC 
        LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        # Convert datetime to string for JSON serialization
        for result in results:
            if result['query_time']:
                result['query_time'] = result['query_time'].isoformat()
        
        return results
        
    except Error as e:
        logger.error(f"Database query error: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/', methods=['GET'])
def home():
    """Frontend interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'IP Geolocation API is running!',
        'endpoints': {
            '/': 'GET - Frontend interface',
            '/api': 'GET - API information',
            '/geo': 'GET - Get geolocation data for client IP',
            '/geo/<ip>': 'GET - Get geolocation data for specific IP',
            '/history': 'GET - Get recent lookup history'
        },
        'database': 'MySQL enabled' if get_db_connection() else 'MySQL not available'
    })

@app.route('/geo', methods=['GET'])
def geo_info():
    """Get geolocation info for client's IP"""
    try:
        # Get client's IP address
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
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

@app.route('/history', methods=['GET'])
def lookup_history():
    """Get recent IP lookup history"""
    limit = request.args.get('limit', 10, type=int)
    history = get_lookup_history(limit)
    return jsonify(history)

def get_location_data(ip):
    """Fetch geolocation data from external API and save to database"""
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
        
        # Save to database (don't fail the request if database save fails)
        if not save_lookup_to_db(geo_data):
            logger.warning(f"Failed to save lookup data for IP: {ip}")
        
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
        'message': 'Available endpoints: /, /api, /geo, /geo/<ip>, /history'
    }), 404

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)