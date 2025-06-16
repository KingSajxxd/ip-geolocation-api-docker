# 🌍 IP Geolocation API

A beautiful, full-featured IP geolocation service with a modern web interface, REST API, and MySQL database integration. Built with Flask and Docker for easy deployment.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![MySQL](https://img.shields.io/badge/mysql-v8.0+-orange.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🎨 Beautiful Web Interface** - Modern, responsive UI with gradient designs and animations
- **🚀 RESTful API** - Clean endpoints for programmatic access
- **💾 MySQL Database** - Persistent storage for lookup history
- **📊 Lookup History** - Track and display recent IP queries
- **🔍 Real-time Lookups** - Instant geolocation data retrieval
- **🐳 Docker Ready** - Complete containerization with docker-compose
- **📱 Mobile Responsive** - Works perfectly on all devices
- **🌐 Client IP Detection** - Automatic detection of visitor's location
- **⚡ Health Checks** - Built-in monitoring and status endpoints

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ip-geolocation-api
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Web Interface: http://localhost:5000
   - API Documentation: http://localhost:5000/api

### Manual Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL database**
   ```bash
   # Create database and run init.sql
   mysql -u root -p < init.sql
   ```

3. **Configure environment variables**
   ```bash
   export DB_HOST=localhost
   export DB_USER=geouser
   export DB_PASSWORD=geopassword
   export DB_NAME=geolocation_db
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 📖 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### `GET /`
Returns the beautiful web interface for interactive IP lookups.

#### `GET /api`
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "IP Geolocation API is running!",
  "endpoints": {
    "/": "GET - Frontend interface",
    "/api": "GET - API information",
    "/geo": "GET - Get geolocation data for client IP",
    "/geo/<ip>": "GET - Get geolocation data for specific IP",
    "/history": "GET - Get recent lookup history"
  },
  "database": "MySQL enabled"
}
```

#### `GET /geo`
Get geolocation data for the client's IP address.

**Response:**
```json
{
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "region": "California",
  "region_code": "CA",
  "city": "Mountain View",
  "zip_code": "94043",
  "latitude": 37.4056,
  "longitude": -122.0775,
  "timezone": "America/Los_Angeles",
  "isp": "Google LLC",
  "organization": "Google Public DNS",
  "as_number": "AS15169 Google LLC",
  "query_time": "2025-06-16T10:30:00.000Z"
}
```

#### `GET /geo/<ip>`
Get geolocation data for a specific IP address.

**Parameters:**
- `ip` (string): The IP address to lookup

**Example:**
```bash
curl http://localhost:5000/geo/1.1.1.1
```

#### `GET /history`
Get recent IP lookup history.

**Query Parameters:**
- `limit` (integer, optional): Number of records to return (default: 10)

**Response:**
```json
[
  {
    "ip": "8.8.8.8",
    "country": "United States",
    "city": "Mountain View",
    "query_time": "2025-06-16T10:30:00"
  }
]
```

## 🏗️ Architecture

### Components

- **Flask App** (`app.py`) - Main application with API endpoints and web interface
- **MySQL Database** - Stores lookup history and provides data persistence
- **Docker Compose** - Orchestrates the multi-container setup
- **Postman Collection** - Pre-configured API tests with beautiful visualizations

### Database Schema

```sql
CREATE TABLE ip_lookups (
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
);
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `mysql` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_USER` | `geouser` | MySQL username |
| `DB_PASSWORD` | `geopassword` | MySQL password |
| `DB_NAME` | `geolocation_db` | MySQL database name |
| `PORT` | `5000` | Application port |
| `FLASK_ENV` | `production` | Flask environment |

### Docker Services

- **mysql**: MySQL 8.0 database with persistent volume
- **ip-geo-api**: Flask application with health checks

## 🧪 Testing

### Using Postman

1. Import the `postman_collection.json` file
2. Set the `base_url` variable to `http://localhost:5000`
3. Run the collection to test all endpoints

The collection includes beautiful visualizations for the API responses!

### Manual Testing

```bash
# Test API status
curl http://localhost:5000/api

# Get your location
curl http://localhost:5000/geo

# Lookup specific IP
curl http://localhost:5000/geo/8.8.8.8

# Get history
curl http://localhost:5000/history
```

## 📁 Project Structure

```
ip-geolocation-api/
├── app.py                    # Main Flask application
├── docker-compose.yaml       # Docker services configuration
├── Dockerfile                # Application container
├── requirements.txt          # Python dependencies
├── init.sql                  # Database initialization
├── postman_collection.json   # API testing collection
└── README.md                 # This file
```

## 🎨 Web Interface Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Search** - Instant IP geolocation lookups
- **My Location Button** - One-click client IP detection
- **Search History** - Visual history of recent lookups
- **Modern UI** - Beautiful gradients, animations, and card layouts
- **Error Handling** - User-friendly error messages
- **Loading States** - Smooth loading animations

## 🚀 Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Use a reverse proxy** (nginx) for SSL termination
3. **Set up monitoring** and logging
4. **Configure backup** for MySQL data

### Docker Production

```bash
# Production build
docker-compose -f docker-compose.yaml up -d

# Check health
docker-compose ps
docker-compose logs
```