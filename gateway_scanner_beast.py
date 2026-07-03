#!/usr/bin/env python3
"""
GATE SCAN - Beast Mode Edition
Advanced Payment Gateway Reconnaissance Tool
With async optimization, expanded gateway coverage, and analytics
"""

import asyncio
import aiohttp
import json
import sqlite3
import hashlib
import time
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Set, Tuple
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn
from rich.live import Live
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging

# Initialize Rich console
console = Console()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gateway_scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BeastModeConfig:
    """Configuration for Beast Mode Scanner"""
    
    # Database
    DB_FILE = 'gateway_results.db'
    
    # Performance
    MAX_CONCURRENT_REQUESTS = 25
    REQUEST_TIMEOUT = 10
    RETRY_ATTEMPTS = 3
    RATE_LIMIT_DELAY = 0.5
    
    # Proxy rotation
    USE_PROXY_ROTATION = True
    PROXY_LIST = [
        # Add your proxies here
        # Format: 'http://ip:port'
    ]
    
    # Enhanced Gateway Coverage
    GATEWAYS = {
        # Payment Processors
        'stripe': {'keywords': ['pk_live_', 'stripe.com/checkout', 'stripejs'], 'dorks': [
            'inurl:checkout stripe -site:github.com',
            '"pk_live_" -site:stripe.com',
            'stripe.js inurl:checkout'
        ]},
        'paypal': {'keywords': ['paypal.com/sdk', 'paypal checkout'], 'dorks': [
            '"paypal.com/sdk/js" -site:github.com',
            'inurl:donate paypal',
            '"PayPal.checkout"'
        ]},
        'braintree': {'keywords': ['braintree', 'dropin.js'], 'dorks': [
            'braintree.dropin inurl:checkout',
            '"braintree-web" -site:github.com'
        ]},
        'square': {'keywords': ['squareup', 'SqPaymentForm'], 'dorks': [
            'squareup.com/payment inurl:checkout',
            'SqPaymentForm'
        ]},
        
        # Crypto Gateways (NEW)
        'bitpay': {'keywords': ['bitpay', 'bitcoin payment'], 'dorks': [
            'bitpay.com/checkout -site:github.com',
            'inurl:bitpay payment'
        ]},
        'coinbase': {'keywords': ['coinbase commerce', 'coinbase payment'], 'dorks': [
            'coinbase.com/commerce inurl:checkout',
            '"coinbase-commerce"'
        ]},
        'lightning': {'keywords': ['lightning network', 'lnurl'], 'dorks': [
            'lnurl:pay inurl:checkout',
            'lightning network payment'
        ]},
        
        # Regional Gateways (NEW)
        'alipay': {'keywords': ['alipay', '支付宝'], 'dorks': [
            'alipay.com inurl:checkout -site:github.com',
            '"alipay.js"'
        ]},
        'wechat_pay': {'keywords': ['weixin', 'wechat pay'], 'dorks': [
            'weixin.qq.com/pay -site:github.com',
            'wechat payment checkout'
        ]},
        'klarna': {'keywords': ['klarna', 'klarna.js'], 'dorks': [
            'klarna.com/checkout -site:github.com',
            '"klarna-payments"'
        ]},
        
        # Buy Now Pay Later (NEW)
        'afterpay': {'keywords': ['afterpay', 'clearpay'], 'dorks': [
            'afterpay.com.au inurl:checkout',
            '"afterpay-js"'
        ]},
        'affirm': {'keywords': ['affirm', 'affirm.js'], 'dorks': [
            'affirm.com checkout -site:github.com',
            '"affirm-js"'
        ]},
    }
    
    # Blocked domains for filtering
    BLOCKED_DOMAINS = [
        'github.com', 'stackoverflow.com', 'reddit.com', 'medium.com',
        'dev.to', 'hashnode.com', 'youtube.com', 'documentation',
        'docs.', 'api.', 'support.', 'help.', 'forum.', 'community.',
        'blog.', 'tutorial.', 'example.', 'demo.', 'test.'
    ]
    
    BLOCKED_KEYWORDS = [
        'tutorial', 'guide', 'documentation', 'how-to', 'example',
        'github', 'stackoverflow', 'demo', 'test', 'development'
    ]

class GatewayDatabase:
    """SQLite database for storing and analyzing results"""
    
    def __init__(self, db_file=BeastModeConfig.DB_FILE):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    gateway TEXT,
                    dork TEXT,
                    search_engine TEXT,
                    found_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status_code INTEGER,
                    response_time REAL,
                    location TEXT,
                    risk_score INTEGER DEFAULT 0
                )
            ''')
            
            # Analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gateway TEXT,
                    total_found INTEGER,
                    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    avg_response_time REAL,
                    avg_risk_score REAL
                )
            ''')
            
            conn.commit()
    
    def insert_result(self, url: str, gateway: str, dork: str, engine: str, 
                     status_code: int = None, response_time: float = None):
        """Insert a scan result"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO results 
                    (url, gateway, dork, search_engine, status_code, response_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (url, gateway, dork, engine, status_code, response_time))
                conn.commit()
        except sqlite3.IntegrityError:
            pass  # Duplicate URL
    
    def get_analytics(self, gateway: str = None) -> List[Dict]:
        """Get analytics for a gateway or all gateways"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            if gateway:
                cursor.execute('''
                    SELECT gateway, COUNT(*) as total, 
                           AVG(response_time) as avg_response_time,
                           AVG(risk_score) as avg_risk
                    FROM results WHERE gateway = ?
                    GROUP BY gateway
                ''', (gateway,))
            else:
                cursor.execute('''
                    SELECT gateway, COUNT(*) as total,
                           AVG(response_time) as avg_response_time,
                           AVG(risk_score) as avg_risk
                    FROM results
                    GROUP BY gateway
                    ORDER BY total DESC
                ''')
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_results_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get results within a date range"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM results
                WHERE found_date BETWEEN ? AND ?
                ORDER BY found_date DESC
            ''', (start_date, end_date))
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

class BeastModeScanner:
    """Beast Mode Payment Gateway Scanner with async optimization"""
    
    def __init__(self):
        self.db = GatewayDatabase()
        self.ua = UserAgent()
        self.session = None
        self.found_urls: Set[str] = set()
        self.stats = {
            'checked': 0,
            'found': 0,
            'blocked': 0,
            'errors': 0
        }
        self.semaphore = asyncio.Semaphore(BeastModeConfig.MAX_CONCURRENT_REQUESTS)
    
    async def init_session(self):
        """Initialize aiohttp session with connection pooling"""
        connector = aiohttp.TCPConnector(
            limit=BeastModeConfig.MAX_CONCURRENT_REQUESTS,
            limit_per_host=5,
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )
        timeout = aiohttp.ClientTimeout(total=BeastModeConfig.REQUEST_TIMEOUT)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def is_valid_url(self, url: str) -> bool:
        """Validate URL against blacklist and filters"""
        url_lower = url.lower()
        
        # Check blocked domains
        for domain in BeastModeConfig.BLOCKED_DOMAINS:
            if domain.lower() in url_lower:
                return False
        
        # Check blocked keywords
        for keyword in BeastModeConfig.BLOCKED_KEYWORDS:
            if keyword.lower() in url_lower:
                return False
        
        return True
    
    async def check_url_async(self, url: str) -> Tuple[int, float]:
        """Check URL asynchronously and get status code and response time"""
        async with self.semaphore:
            try:
                headers = {'User-Agent': self.ua.random}
                start_time = time.time()
                
                async with self.session.head(url, headers=headers, allow_redirects=True) as resp:
                    response_time = time.time() - start_time
                    return resp.status, response_time
            except asyncio.TimeoutError:
                return None, None
            except Exception as e:
                logger.debug(f"Error checking {url}: {e}")
                return None, None
    
    async def scan_dorks_async(self, gateway: str, dorks: List[str]) -> List[str]:
        """Scan multiple dorks concurrently (stub - requires API integration)"""
        # In production, integrate with Google Custom Search API, Bing, etc.
        # This is a placeholder that shows the async structure
        return []
    
    async def process_results(self, gateway: str, results: List[str], dork: str, engine: str):
        """Process and validate scan results asynchronously"""
        tasks = []
        
        for url in results:
            if self.is_valid_url(url) and url not in self.found_urls:
                self.found_urls.add(url)
                tasks.append(self._process_single_url(url, gateway, dork, engine))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _process_single_url(self, url: str, gateway: str, dork: str, engine: str):
        """Process a single URL"""
        status_code, response_time = await self.check_url_async(url)
        
        if status_code:
            self.db.insert_result(url, gateway, dork, engine, status_code, response_time)
            self.stats['found'] += 1
            
            console.print(
                f"[green]✓[/green] [bold]{gateway.upper()}[/bold] found at {url}",
                style="bright_green"
            )
    
    async def run_scan(self):
        """Main async scanning function"""
        await self.init_session()
        
        try:
            console.print(
                Panel(
                    "[bold cyan]🔥 GATE SCAN - BEAST MODE EDITION 🔥[/bold cyan]",
                    expand=False,
                    border_style="bold green"
                )
            )
            
            console.print(
                f"[cyan]📊 Scanning {len(BeastModeConfig.GATEWAYS)} payment gateways[/cyan]\n"
            )
            
            # Create tasks for all gateways
            tasks = []
            for gateway, config in BeastModeConfig.GATEWAYS.items():
                for dork in config['dorks']:
                    tasks.append(self.scan_dorks_async(gateway, [dork]))
            
            # Run all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Display results
            self.display_results()
            self.display_analytics()
        
        finally:
            await self.close_session()
    
    def display_results(self):
        """Display scan results in a table"""
        table = Table(title="[bold cyan]Scan Results[/bold cyan]", show_header=True)
        table.add_column("Gateway", style="cyan")
        table.add_column("Total Found", style="magenta")
        table.add_column("Status", style="green")
        
        analytics = self.db.get_analytics()
        for result in analytics:
            table.add_row(
                result['gateway'].upper(),
                str(result['total']),
                "✓ Complete"
            )
        
        console.print(table)
    
    def display_analytics(self):
        """Display analytics dashboard"""
        console.print(
            Panel(
                f"[bold]📊 ANALYTICS DASHBOARD[/bold]\n"
                f"Total Found: {self.stats['found']}\n"
                f"URLs Checked: {self.stats['checked']}\n"
                f"Blocked: {self.stats['blocked']}",
                expand=False,
                border_style="bold yellow"
            )
        )

if __name__ == "__main__":
    scanner = BeastModeScanner()
    asyncio.run(scanner.run_scan())
