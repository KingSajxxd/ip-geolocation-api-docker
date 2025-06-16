
-- Initialize the geolocation database
USE geolocation_db;

-- Create the ip_lookups table
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

-- Insert some sample data for testing
INSERT INTO ip_lookups (ip, country, country_code, region, city, latitude, longitude, timezone, isp) VALUES
('8.8.8.8', 'United States', 'US', 'California', 'Mountain View', 37.4056, -122.0775, 'America/Los_Angeles', 'Google LLC'),
('1.1.1.1', 'Australia', 'AU', 'New South Wales', 'Sydney', -33.8688, 151.2093, 'Australia/Sydney', 'Cloudflare, Inc.');

-- Create a view for recent lookups
CREATE OR REPLACE VIEW recent_lookups AS
SELECT 
    ip,
    CONCAT(city, ', ', region, ', ', country) as location,
    country_code,
    query_time
FROM ip_lookups 
ORDER BY query_time DESC 
LIMIT 50;