#!/usr/bin/env python3
"""
Unit tests for Beast Mode Scanner
"""

import unittest
import asyncio
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import modules to test
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gateway_scanner_beast import (
    BeastModeConfig,
    GatewayDatabase,
    BeastModeScanner
)
from security_module import (
    ProxyRotator,
    ConfigEncryption,
    CAPTCHADetector,
    RateLimiter
)

class TestBeastModeConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_gateway_count(self):
        """Test that all gateways are configured"""
        self.assertGreater(len(BeastModeConfig.GATEWAYS), 10)
    
    def test_gateway_structure(self):
        """Test gateway configuration structure"""
        for gateway, config in BeastModeConfig.GATEWAYS.items():
            self.assertIn('keywords', config)
            self.assertIn('dorks', config)
            self.assertIsInstance(config['dorks'], list)

class TestGatewayDatabase(unittest.TestCase):
    """Test database functionality"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = GatewayDatabase(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        os.unlink(self.temp_db.name)
    
    def test_insert_result(self):
        """Test inserting a result"""
        self.db.insert_result(
            'https://example.com/checkout',
            'stripe',
            'inurl:checkout stripe',
            'google',
            200,
            0.5
        )
        
        analytics = self.db.get_analytics('stripe')
        self.assertEqual(len(analytics), 1)
        self.assertEqual(analytics[0]['total'], 1)
    
    def test_duplicate_prevention(self):
        """Test that duplicates are prevented"""
        url = 'https://example.com/checkout'
        
        self.db.insert_result(url, 'stripe', 'dork1', 'google', 200, 0.5)
        self.db.insert_result(url, 'stripe', 'dork2', 'google', 200, 0.5)
        
        analytics = self.db.get_analytics('stripe')
        self.assertEqual(analytics[0]['total'], 1)  # Should be 1, not 2

class TestProxyRotator(unittest.TestCase):
    """Test proxy rotation"""
    
    def setUp(self):
        self.proxies = ['http://proxy1.com:8080', 'http://proxy2.com:8080']
        self.rotator = ProxyRotator(self.proxies)
    
    def test_get_next_proxy(self):
        """Test sequential proxy rotation"""
        proxy1 = self.rotator.get_next_proxy()
        proxy2 = self.rotator.get_next_proxy()
        proxy3 = self.rotator.get_next_proxy()
        
        self.assertEqual(proxy1, self.proxies[0])
        self.assertEqual(proxy2, self.proxies[1])
        self.assertEqual(proxy3, self.proxies[0])  # Should cycle
    
    def test_get_random_proxy(self):
        """Test random proxy selection"""
        proxy = self.rotator.get_random_proxy()
        self.assertIn(proxy, self.proxies)
    
    def test_add_proxy(self):
        """Test adding proxy"""
        self.rotator.add_proxy('http://proxy3.com:8080')
        self.assertEqual(len(self.rotator.proxy_list), 3)
    
    def test_remove_proxy(self):
        """Test removing proxy"""
        self.rotator.remove_proxy(self.proxies[0])
        self.assertEqual(len(self.rotator.proxy_list), 1)

class TestConfigEncryption(unittest.TestCase):
    """Test configuration encryption"""
    
    def setUp(self):
        from cryptography.fernet import Fernet
        self.key = Fernet.generate_key()
        self.encryptor = ConfigEncryption(self.key)
    
    def test_encrypt_decrypt(self):
        """Test encrypt and decrypt roundtrip"""
        config = {'api_key': 'secret123', 'user': 'testuser'}
        
        encrypted = self.encryptor.encrypt_config(config)
        decrypted = self.encryptor.decrypt_config(encrypted)
        
        self.assertEqual(config, decrypted)
    
    def test_hash_sensitive_data(self):
        """Test hashing sensitive data"""
        data = 'sensitive_password'
        hash1 = self.encryptor.hash_sensitive_data(data)
        hash2 = self.encryptor.hash_sensitive_data(data)
        
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)  # SHA256 hex length

class TestCAPTCHADetector(unittest.TestCase):
    """Test CAPTCHA detection"""
    
    def test_detect_recaptcha(self):
        """Test reCAPTCHA detection"""
        response = '<html>Please verify with reCAPTCHA</html>'
        self.assertTrue(CAPTCHADetector.detect_captcha(response, 200))
    
    def test_detect_status_code(self):
        """Test CAPTCHA detection via status code"""
        self.assertTrue(CAPTCHADetector.detect_captcha('', 429))
        self.assertTrue(CAPTCHADetector.detect_captcha('', 403))
    
    def test_no_captcha(self):
        """Test normal response"""
        response = '<html>Normal page content</html>'
        self.assertFalse(CAPTCHADetector.detect_captcha(response, 200))

class TestBeastModeScanner(unittest.TestCase):
    """Test Beast Mode Scanner"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        # Patch DB file location
        with patch.object(BeastModeConfig, 'DB_FILE', self.temp_db.name):
            self.scanner = BeastModeScanner()
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_is_valid_url(self):
        """Test URL validation"""
        self.assertFalse(self.scanner.is_valid_url('https://github.com/example'))
        self.assertFalse(self.scanner.is_valid_url('https://stackoverflow.com/tutorial'))
        self.assertTrue(self.scanner.is_valid_url('https://example-store.com/checkout'))

if __name__ == '__main__':
    unittest.main()
