#!/usr/bin/env python3
"""
Security Module for Beast Mode Scanner
Proxy rotation, encryption, and advanced security features
"""

import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
from typing import List, Optional
import aiohttp
import asyncio
import random

class ProxyRotator:
    """Manage proxy rotation for anonymous scanning"""
    
    def __init__(self, proxy_list: List[str] = None):
        self.proxy_list = proxy_list or self._load_proxies()
        self.current_index = 0
    
    def _load_proxies(self) -> List[str]:
        """Load proxies from file or environment"""
        proxy_file = 'proxies.txt'
        
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        
        return []
    
    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy in rotation"""
        if not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxy_list)
        return proxy
    
    def get_random_proxy(self) -> Optional[str]:
        """Get random proxy from list"""
        if not self.proxy_list:
            return None
        return random.choice(self.proxy_list)
    
    def add_proxy(self, proxy: str):
        """Add proxy to rotation list"""
        if proxy not in self.proxy_list:
            self.proxy_list.append(proxy)
    
    def remove_proxy(self, proxy: str):
        """Remove proxy from rotation list"""
        if proxy in self.proxy_list:
            self.proxy_list.remove(proxy)

class ConfigEncryption:
    """Encrypt and decrypt sensitive configuration"""
    
    def __init__(self, key: Optional[str] = None):
        self.key = key or self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self) -> bytes:
        """Get encryption key from file or create new one"""
        key_file = '.gate_scan_key'
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        
        # Create new key
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        
        # Secure the key file
        os.chmod(key_file, 0o600)
        
        return key
    
    def encrypt_config(self, config: dict) -> str:
        """Encrypt configuration dictionary"""
        config_json = json.dumps(config).encode()
        encrypted = self.cipher.encrypt(config_json)
        return base64.b64encode(encrypted).decode()
    
    def decrypt_config(self, encrypted_config: str) -> dict:
        """Decrypt configuration"""
        try:
            encrypted = base64.b64decode(encrypted_config)
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception as e:
            raise ValueError(f"Failed to decrypt config: {e}")
    
    def hash_sensitive_data(self, data: str) -> str:
        """Create hash of sensitive data for verification"""
        return hashlib.sha256(data.encode()).hexdigest()

class CAPTCHADetector:
    """Detect and handle CAPTCHA challenges"""
    
    CAPTCHA_INDICATORS = [
        'recaptcha',
        'captcha',
        'robot',
        'verify',
        'challenge',
        'unusual traffic',
        'blocked',
        'forbidden'
    ]
    
    @staticmethod
    def detect_captcha(response_text: str, status_code: int) -> bool:
        """Detect if response contains CAPTCHA"""
        if status_code in [403, 429]:
            return True
        
        response_lower = response_text.lower()
        return any(indicator in response_lower for indicator in CAPTCHADetector.CAPTCHA_INDICATORS)
    
    @staticmethod
    def handle_captcha(url: str) -> dict:
        """Handle CAPTCHA detection"""
        return {
            'status': 'captcha_detected',
            'url': url,
            'action': 'pause_and_retry',
            'retry_after': 300  # 5 minutes
        }

class RateLimiter:
    """Intelligent rate limiting to avoid blocking"""
    
    def __init__(self, requests_per_second: float = 1.0):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
    
    async def wait_if_needed(self):
        """Wait if necessary to maintain rate limit"""
        current_time = asyncio.get_event_loop().time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            await asyncio.sleep(self.min_interval - time_since_last)
        
        self.last_request_time = asyncio.get_event_loop().time()

class RequestSigner:
    """Sign and verify requests for API authentication"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def sign_request(self, data: dict) -> str:
        """Sign request data"""
        data_str = json.dumps(data, sort_keys=True)
        signature = hashlib.hmac.new(
            self.secret_key.encode(),
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify_signature(self, data: dict, signature: str) -> bool:
        """Verify request signature"""
        expected_signature = self.sign_request(data)
        return signature == expected_signature

if __name__ == '__main__':
    # Example usage
    print("[*] Security Module Loaded")
    
    # Test proxy rotation
    rotator = ProxyRotator(['http://proxy1.com:8080', 'http://proxy2.com:8080'])
    print(f"[+] Next proxy: {rotator.get_next_proxy()}")
    print(f"[+] Random proxy: {rotator.get_random_proxy()}")
    
    # Test encryption
    encryptor = ConfigEncryption()
    config = {'api_key': 'secret123', 'user': 'test'}
    encrypted = encryptor.encrypt_config(config)
    print(f"[+] Encrypted config: {encrypted[:50]}...")
    
    decrypted = encryptor.decrypt_config(encrypted)
    print(f"[+] Decrypted config: {decrypted}")
