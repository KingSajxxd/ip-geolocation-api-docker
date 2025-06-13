# Ip-geolocation-api-docker
A simple, lightweight Flask-based IP Geolocation API that retrieves location details (country, city, ISP, timezone, coordinates) for any given IP address using the ip-api.com service. Supports client and custom IP lookup via REST endpoints. Dockerized for easy containerized deployment and portability.

# 🌍 IP Geolocation API

A simple, Dockerized Flask API that detects client IP addresses and returns geolocation data with beautiful Postman visualizations.

## 🚀 Features

- **Automatic IP Detection**: Detects client's real IP address
- **Specific IP Lookup**: Query any IP address directly
- **Rich Geolocation Data**: Country, region, city, coordinates, ISP info
- **Beautiful Postman Visualizations**: Eye-catching cards and layouts
- **Production Ready**: Dockerized with Gunicorn and health checks
- **Error Handling**: Comprehensive error responses
- **Free API**: Uses ip-api.com (no API key required)

## 📋 Prerequisites

- Docker & Docker Compose
- Postman (for testing & visualization)
- Basic knowledge of REST APIs

## 🏗️ Project Structure

```
ip-geo-api/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── postman_collection.json  # Postman collection with visualizations
└── README.md                # This file
```

## ⚡ Quick Start

### 1. Clone/Create the Project

Create a new directory and add all the provided files:

```bash
mkdir ip-geo-api
cd ip-geo-api
# Add all the files (app.py, requirements.txt, Dockerfile, etc.)
```

### 2. Build and Run with Docker

```bash
# Build the Docker image
docker build -t ip-geo-api .

# Run the container
docker run -p 5000:5000 ip-geo-api
```

**Or use Docker Compose:**

```bash
# Run with docker-compose
docker-compose up --build
```

### 3. Test the API

The API will be available at `http://localhost:5000`

**Available Endpoints:**

- `GET /` - Health check
- `GET /geo` - Get your IP's geolocation
- `GET /geo/<ip>` - Get specific IP's geolocation

**Example requests:**

```bash
# Check if API is running
curl http://localhost:5000/

# Get your location
curl http://localhost:5000/geo

# Get location for specific IP
curl http://localhost:5000/geo/8.8.8.8
```

## 🎨 Postman Setup & Visualization

### 1. Import the Collection

1. Open Postman
2. Click **Import**
3. Upload the `postman_collection.json` file
4. The collection will include 3 requests with beautiful visualizations

### 2. Set Environment Variable

1. Create a new environment in Postman
2. Add variable: `base_url` = `http://localhost:5000`
3. Select this environment

### 3. Test the Requests

1. **Health Check**: Verify API is running
2. **Get My Location**: See your IP's location with rich visualization
3. **Get Location by IP**: Test with specific IP (default: 8.8.8.8)

### 4. Enjoy the Visualizations! 🎉

The Postman visualizer will show:
- 🌍 Beautiful gradient cards
- 📍 Organized location data
- 🌐 Network information
- 📊 Color-coded sections
- ⏰ Query timestamps

## 🐳 Docker Commands

```bash
# Build image
docker build -t ip-geo-api .

# Run container
docker run -p 5000:5000 ip-geo-api

# Run in background
docker run -d -p 5000:5000 --name geo-api ip-geo-api

# View logs
docker logs geo-api

# Stop container
docker stop geo-api

# Remove container
docker rm geo-api
```

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python app.py
```

## 📊 Sample Response

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
  "query_time": "2025-06-13T10:30:45Z"
}
```

## 🌟 Bonus Features to Add

- **Rate Limiting**: Add Flask-Limiter
- **Database Storage**: Store IP lookups in SQLite
- **Frontend Interface**: Simple HTML page
- **API Authentication**: Add API keys
- **Multiple Providers**: Fallback to different IP APIs
- **Caching**: Cache results with Redis

## 🛠️ Troubleshooting

### Local IP Issues
- When running locally, `127.0.0.1` is used as fallback
- Test with `/geo/8.8.8.8` for real geolocation data

### Docker Issues
```bash
# Check if container is running
docker ps

# Check container logs
docker logs <container-id>

# Rebuild if needed
docker build --no-cache -t ip-geo-api .
```

### Postman Visualization Not Showing
- Make sure you're in the **Tests** tab for visualization scripts
- Check if the response is valid JSON
- Look for JavaScript errors in Postman console

## 📚 Learning Outcomes

After completing this project, you'll understand:

- ✅ **Flask API Development**: Building REST endpoints
- ✅ **Docker Containerization**: Creating production-ready containers
- ✅ **External API Integration**: Calling third-party services
- ✅ **Error Handling**: Robust API error responses
- ✅ **Postman Advanced Features**: Visualizations and testing
- ✅ **IP Address Handling**: Understanding client IP detection
- ✅ **JSON Data Processing**: Working with structured data

## 🎯 Next Steps

1. **Add a Database**: Store IP lookup history
2. **Create a Frontend**: Build a simple web interface
3. **Add Authentication**: Secure your API
4. **Deploy to Cloud**: AWS, Heroku, or DigitalOcean
5. **Add Monitoring**: Health checks and logging
