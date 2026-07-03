#!/usr/bin/env python3
"""
Configuration Example for Beast Mode Scanner
Copy to config.py and update with your credentials
"""

# Google Custom Search API
GOOGLE_API_KEY = 'your-google-api-key-here'
GOOGLE_SEARCH_ENGINE_ID = 'your-search-engine-id-here'

# Proxy Configuration
USE_PROXY_ROTATION = True
PROXY_LIST = [
    # Add your proxies here
    # Format: 'http://ip:port' or 'http://user:pass@ip:port'
]

# Performance Settings
MAX_CONCURRENT_REQUESTS = 25
REQUEST_TIMEOUT = 10
RATES_PER_SECOND = 2.0

# Database
DB_FILE = 'gateway_results.db'

# Output Settings
LOG_FILE = 'gateway_scanner.log'
EXPORT_FORMAT = 'json'  # json, csv, pdf

# Security
ENCRYPT_CREDENTIALS = True
VERIFY_SSL = True

# Notification Settings (optional)
SLACK_WEBHOOK = None  # Set to enable Slack notifications
EMAIL_NOTIFICATIONS = False
EMAIL_RECIPIENTS = []
