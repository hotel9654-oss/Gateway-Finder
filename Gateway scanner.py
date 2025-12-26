import asyncio
import aiohttp
import re
import random
import os
import time
import platform
import hashlib
import uuid
from datetime import datetime, timedelta
from urllib.parse import quote, urlparse, urljoin, parse_qs
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich import box
from rich.align import Align
console = Console()

class LicenseManager:

    def __init__(self):
        pass

    def check_license(self) -> dict:
        return {'status': 'active', 'discord_username': 'User', 'expires_at': None, 'last_used_at': None, 'license_key': 'FREE-LICENSE'}

    def _display_license_info(self, *args, **kwargs):
        pass

def print_banner():
    width = console.size.width
    console.print()
    if width >= 82:
        lines = [('╔══════════════════════════════════════════════════════════════════════════════╗', 'cyan'), ('║                                                                              ║', 'cyan'), ('║     ██████╗  █████╗ ████████╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗  ║', 'bold magenta'), ('║    ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║  ║', 'bold red'), ('║    ██║  ███╗███████║   ██║   █████╗      ███████╗██║     ███████║██╔██╗ ██║  ║', 'bold yellow'), ('║    ██║   ██║██╔══██║   ██║   ██╔══╝      ╚════██║██║     ██╔══██║██║╚██╗██║  ║', 'bold green'), ('║    ╚██████╔╝██║  ██║   ██║   ███████╗    ███████║╚██████╗██║  ██║██║ ╚████║  ║', 'bold cyan'), ('║     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ║', 'bold blue'), ('║                                                                              ║', 'cyan'), ('║  ════════════════════════════════════════════════════════════════════════    ║', 'dim'), ('║                  ⚡ PAYMENT GATEWAY RECONNAISSANCE TOOL ⚡                    ║', 'bold yellow'), ('║  ════════════════════════════════════════════════════════════════════════    ║', 'dim'), ('║                                                                              ║', 'cyan'), ('║       ▸ Stripe    ▸ PayPal    ▸ Braintree    ▸ Square    ▸ Shopify           ║', 'dim cyan'), ('║       ▸ WooCommerce    ▸ Coinbase    ▸ Crypto    ▸ Authorize.net             ║', 'dim cyan'), ('║                                                                              ║', 'cyan'), ('╚══════════════════════════════════════════════════════════════════════════════╝', 'cyan')]
        for line, style in lines:
            console.print(Align.center(Text(line, style=style)))
    elif width >= 50:
        lines = [('╔════════════════════════════════════════════╗', 'cyan'), ('║  ██████╗  █████╗ ████████╗███████╗         ║', 'bold magenta'), ('║ ██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝         ║', 'bold red'), ('║ ██║  ███╗███████║   ██║   █████╗           ║', 'bold yellow'), ('║ ██║   ██║██╔══██║   ██║   ██╔══╝           ║', 'bold green'), ('║ ╚██████╔╝██║  ██║   ██║   ███████╗         ║', 'bold cyan'), ('║  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝         ║', 'bold blue'), ('║ ███████╗ ██████╗ █████╗ ███╗   ██╗         ║', 'bold magenta'), ('║ ██╔════╝██╔════╝██╔══██╗████╗  ██║         ║', 'bold red'), ('║ ███████╗██║     ███████║██╔██╗ ██║         ║', 'bold yellow'), ('║ ╚════██║██║     ██╔══██║██║╚██╗██║         ║', 'bold green'), ('║ ███████║╚██████╗██║  ██║██║ ╚████║         ║', 'bold cyan'), ('║ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝         ║', 'bold blue'), ('╠════════════════════════════════════════════╣', 'dim'), ('║    ⚡ GATEWAY RECONNAISSANCE TOOL ⚡       ║', 'bold yellow'), ('╚════════════════════════════════════════════╝', 'cyan')]
        for line, style in lines:
            console.print(Align.center(Text(line, style=style)))
    else:
        border = '═' * (width - 2)
        console.print(Align.center(Text(f'╔{border}╗', style='cyan')))
        console.print(Align.center(Text('GATE SCAN', style='bold magenta')))
        console.print(Align.center(Text('⚡ Gateway Recon ⚡', style='bold yellow')))
        console.print(Align.center(Text(f'╚{border}╝', style='cyan')))
    console.print()
DORKS = ['inurl:donate paypal -site:github.com -site:stackoverflow.com -site:reddit.com -site:docs.paypal.com', 'inurl:donate braintree -site:github.com -site:stackoverflow.com', 'inurl:donate square -site:github.com', 'inurl:donate venmo -site:github.com', 'inurl:checkout paypal -site:github.com -site:paypal.com', 'inurl:checkout braintree -site:github.com', 'inurl:checkout square -site:github.com', 'inurl:donate stripe -site:github.com -site:stackoverflow.com -site:docs.stripe.com -site:support.stripe.com', 'inurl:add-payment-method stripe -site:github.com', 'inurl:checkout stripe -site:github.com', 'inurl:donate coinbase -site:github.com', 'inurl:donate crypto -site:github.com', 'inurl:payment stripe -site:github.com -site:stackoverflow.com', 'inurl:payment paypal -site:github.com -site:paypal.com', 'inurl:give stripe -site:github.com', 'inurl:give paypal -site:github.com', 'inurl:support-us stripe -site:github.com', 'inurl:support-us paypal -site:github.com', 'inurl:contribute stripe -site:github.com', 'inurl:contribute paypal -site:github.com', 'inurl:tip stripe -site:github.com', 'inurl:sponsor stripe -site:github.com', 'inurl:membership stripe -site:github.com', 'inurl:subscribe stripe -site:github.com', 'title:"Donate Now" paypal OR braintree OR square OR stripe OR coinbase', 'title:"Support Us" stripe OR paypal', 'title:"Make a Donation" stripe OR paypal', 'title:"Give Now" stripe OR paypal', 'inurl:checkout woocommerce -site:github.com -site:wordpress.org -site:woocommerce.com', 'inurl:cart woocommerce stripe OR paypal -site:github.com -site:wordpress.org', 'inurl:order-pay woocommerce -site:github.com -site:wordpress.org', '"woocommerce-checkout" "Place order" stripe -site:github.com -site:wordpress.org', 'site:myshopify.com inurl:checkout', 'site:myshopify.com inurl:cart', '"Powered by Shopify" checkout stripe -site:github.com -site:shopify.com', '"Powered by Shopify" "add to cart" -site:github.com -site:shopify.com', 'inurl:/checkouts/ "credit card" -site:github.com -site:shopify.com', 'inurl:shop checkout stripe OR paypal -site:github.com', 'inurl:store checkout stripe OR paypal -site:github.com', 'inurl:products "add to cart" stripe -site:github.com -site:shopify.com', 'inurl:my-account woocommerce -site:github.com -site:wordpress.org -site:woocommerce.com', 'inurl:my-account/payment-methods -site:github.com -site:wordpress.org -site:woocommerce.com', 'inurl:my-account/add-payment-method -site:github.com -site:wordpress.org -site:woocommerce.com', 'inurl:my-account/orders woocommerce -site:github.com -site:wordpress.org', '"woocommerce-MyAccount" stripe OR paypal -site:github.com -site:wordpress.org', 'inurl:/my-account/ "payment methods" stripe -site:github.com -site:wordpress.org', 'inurl:/my-account/ "Add payment method" -site:github.com -site:wordpress.org', '"Save payment method" woocommerce -site:github.com -site:wordpress.org', 'inurl:my-account "saved cards" -site:github.com -site:wordpress.org', 'inurl:/checkout/order-pay/ woocommerce -site:github.com -site:wordpress.org', 'inurl:/checkout/order-received/ woocommerce -site:github.com -site:wordpress.org', '"wc-stripe-elements" -site:github.com -site:wordpress.org', '"woocommerce-account" "Payment methods" -site:github.com -site:wordpress.org']
GATEWAY_PATTERNS = {'STRIPE': [re.compile('pk_live_[0-9A-Za-z]{20,}'), re.compile('pk_test_[0-9A-Za-z]{20,}'), re.compile('js\\.stripe\\.com', re.I), re.compile('stripe\\.com/v3', re.I), re.compile('Stripe\\s*[\\(\\.]', re.I), re.compile('stripe-js', re.I), re.compile('data-stripe', re.I), re.compile('StripeCheckout', re.I), re.compile('stripe\\.createToken', re.I), re.compile('stripe\\.elements', re.I), re.compile('stripe-button', re.I), re.compile('checkout\\.stripe\\.com', re.I), re.compile('stripe-payment', re.I)], 'PAYPAL': [re.compile('paypal\\.com/sdk', re.I), re.compile('paypal-button', re.I), re.compile('PayPal\\.Buttons', re.I), re.compile('paypal\\.com/cgi-bin', re.I), re.compile('paypalobjects\\.com', re.I), re.compile('paypal-checkout', re.I), re.compile('data-paypal', re.I), re.compile('paypal\\.com/donate', re.I), re.compile('paypal\\.me/', re.I), re.compile('hosted_button_id', re.I), re.compile('paypal-smart', re.I)], 'BRAINTREE': [re.compile('braintree.*\\.js', re.I), re.compile('braintreegateway', re.I), re.compile('braintree\\.client', re.I), re.compile('braintree-web', re.I)], 'SQUARE': [re.compile('sq-payment', re.I), re.compile('squareup\\.com', re.I), re.compile('squarecdn\\.com', re.I), re.compile('square-payment', re.I)], 'VENMO': [re.compile('venmo\\.com', re.I), re.compile('venmo-button', re.I)], 'COINBASE': [re.compile('commerce\\.coinbase', re.I), re.compile('coinbase-commerce', re.I)], 'CRYPTO': [re.compile('bitcoin:[13][a-km-zA-HJ-NP-Z1-9]{25,34}'), re.compile('ethereum:0x[a-fA-F0-9]{40}'), re.compile('metamask', re.I), re.compile('web3modal', re.I)], 'AUTHORIZE_NET': [re.compile('authorize\\.net', re.I), re.compile('Accept\\.js', re.I)], 'ADYEN': [re.compile('adyen\\.com', re.I), re.compile('adyen-checkout', re.I)], 'RAZORPAY': [re.compile('razorpay\\.com', re.I), re.compile('Razorpay\\(', re.I)], 'GOCARDLESS': [re.compile('gocardless', re.I)], 'WOOCOMMERCE': [re.compile('woocommerce-checkout', re.I), re.compile('woocommerce-billing', re.I), re.compile('woocommerce-payment', re.I), re.compile('wc-block-checkout', re.I), re.compile('id=["\\\']billing_first_name', re.I), re.compile('id=["\\\']payment_method_', re.I), re.compile('wc-gateway', re.I), re.compile('wc-stripe', re.I), re.compile('wc-braintree', re.I), re.compile('wc-paypal', re.I), re.compile('woocommerce-checkout-payment', re.I), re.compile('woocommerce-checkout-review-order', re.I), re.compile('name=["\\\']woocommerce-process-checkout', re.I), re.compile('/wp-content/plugins/woocommerce.*checkout', re.I), re.compile('wc-credit-card-form', re.I), re.compile('/my-account/?$', re.I), re.compile('/my-account/payment-methods', re.I), re.compile('/my-account/add-payment-method', re.I), re.compile('/my-account/orders', re.I), re.compile('/my-account/edit-address', re.I), re.compile('/my-account/edit-account', re.I), re.compile('/my-account/subscriptions', re.I), re.compile('woocommerce-MyAccount', re.I), re.compile('woocommerce-account', re.I), re.compile('woocommerce-MyAccount-navigation', re.I), re.compile('woocommerce-MyAccount-content', re.I), re.compile('woocommerce-MyAccount-payment-methods', re.I), re.compile('wc-saved-payment-methods', re.I), re.compile('add_payment_method', re.I), re.compile('wc-add-payment-method', re.I), re.compile('wc-stripe-elements', re.I), re.compile('wc-stripe-payment-request', re.I), re.compile('woocommerce-orders', re.I), re.compile('woocommerce-address', re.I), re.compile('woocommerce-message', re.I), re.compile('class=["\\\']woocommerce["\\\']', re.I), re.compile('/checkout/order-pay/', re.I), re.compile('/checkout/order-received/', re.I), re.compile('wc-order-pay', re.I), re.compile('payment-method-saved', re.I), re.compile('wc-saved-cards', re.I), re.compile('saved-payment-methods', re.I), re.compile('wc-payment-token', re.I), re.compile('/wc-api/', re.I), re.compile('\\?wc-ajax=', re.I), re.compile('woocommerce_checkout', re.I), re.compile('woocommerce-cart', re.I), re.compile('woocommerce-shipping', re.I), re.compile('woocommerce-info', re.I), re.compile('woocommerce-form-login', re.I), re.compile('woocommerce-form-register', re.I), re.compile('woocommerce-ResetPassword', re.I), re.compile('woocommerce-LostPassword', re.I)], 'SHOPIFY': [re.compile('cdn\\.shopify\\.com', re.I), re.compile('\\.myshopify\\.com', re.I), re.compile('Shopify\\.Checkout', re.I), re.compile('shopify\\.com/checkouts', re.I), re.compile('/checkouts/[a-z0-9]+', re.I), re.compile('data-shopify', re.I), re.compile('Shopify\\.PaymentButton', re.I), re.compile('shopify-payment-button', re.I), re.compile('shop_pay', re.I), re.compile('ShopifyBuy', re.I), re.compile('shopify-buy-button', re.I), re.compile('checkout__content', re.I), re.compile('field__input--credit-card', re.I), re.compile('card-fields-container', re.I), re.compile('shopify-cleanslate', re.I), re.compile('data-shopify-buttoncontainer', re.I)]}
CARD_PATTERNS = [re.compile('card.?number', re.I), re.compile('cc-number', re.I), re.compile('card-element', re.I), re.compile('payment-element', re.I), re.compile('cvv|cvc', re.I), re.compile('expir', re.I), re.compile('cardholder', re.I), re.compile('credit.?card', re.I), re.compile('billing_first_name', re.I), re.compile('billing_address', re.I), re.compile('wc-credit-card-form', re.I), re.compile('wc-card-number', re.I), re.compile('stripe-card-element', re.I), re.compile('field__input--credit-card', re.I), re.compile('card-fields-container', re.I), re.compile('wc-stripe-elements-field', re.I), re.compile('wc-stripe-card-number', re.I), re.compile('wc-stripe-card-expiry', re.I), re.compile('wc-stripe-card-cvc', re.I), re.compile('wc-saved-payment-methods', re.I), re.compile('wc-payment-form', re.I)]
CHECKOUT_KEYWORDS = ['checkout', 'donate', 'payment', 'billing', 'subscribe', 'give', 'contribution', 'support', 'pay', 'purchase', 'tip', 'fund', 'cart', 'order-pay', 'checkouts', 'add-payment-method', 'shop', 'store', 'products', 'my-account', 'payment-methods', 'add-payment-method', 'orders', 'edit-address', 'subscriptions', 'order-received', 'order-pay', 'saved-cards', 'saved-payment', 'wc-api']
BLOCKED_DOMAINS = ['github.com', 'stackoverflow.com', 'reddit.com', 'docs.stripe.com', 'support.stripe.com', 'docs.paypal.com', 'square.site', 'developer.paypal.com', 'npmjs.com', 'medium.com', 'youtube.com', 'twitter.com', 'facebook.com', 'linkedin.com', 'wikipedia.org', 'w3schools.com', 'codepen.io', 'stripe.com', 'paypal.com', 'braintreepayments.com', 'squareup.com', 'google.com', 'bing.com', 'yahoo.com', 'duckduckgo.com', 'brave.com', 'amazon.com', 'ebay.com', 'pinterest.com', 'instagram.com', 'tiktok.com', 'quora.com', 'shopify.com', 'community.shopify.com', 'wordpress.org', 'prestashop.com', 'bigcommerce.com', 'woocommerce.com', 'magento.com', 'stackexchange.com', 'money.stackexchange.com', 'superuser.com', 'webtoffee.com', 'klinkode.com', 'discoplugin.com', 'formswrite.com', 'community.fly.io', 'community.openai.com', 'community.make.com', 'experienceleague.adobe.com', 'forum.squarespace.com', 'builtwith.com', 'trends.builtwith.com', 'paypal-community.com', 'newsroom.paypal-corp.com', 'braintree.github.io', 'coinbase.com', 'learn.coinbase.com', 'jetformbuilder.com', 'developer.woocommerce.com', 'developer.wordpress.org', 'developer.shopify.com', 'apps.shopify.com', 'themes.shopify.com', 'wpforms.com', 'wpmudev.com', 'developer.squarespace.com', 'developer.bigcommerce.com', 'developer.prestashop.com', 'developer.magento.com', 'developer.adobe.com', 'developer.authorize.net', 'developer.squareup.com', 'developer.braintreepayments.com', 'developer.adyen.com', 'developer.razorpay.com', 'developer.gocardless.com', 'developers.coinbase.com', 'docs.coinbase.com', 'developer.mozilla.org', 'developer.chrome.com', 'developer.apple.com', 'crocoblock.com', 'developer.android.com', 'developer.microsoft.com', 'businessbloomer.com', 'developer.envato.com', 'developer.wordpress.com', 'developer.google.com', 'developer.amazon.com', 'developer.facebook.com', 'developer.twitter.com', 'developer.paypal.com', 'docs.woocommerce.com', 'developer.wordpress.org', 'developer.woocommerce.com', 'developer.checkout.com']
BLOCKED_URL_KEYWORDS = ['how-to', 'howto', 'tutorial', 'guide', 'blog', 'article', 'learn', 'documentation', 'docs', 'faq', 'help', 'support', 'forum', 'community', 'question', 'answer', 'topic', 'thread', 'discussion', 'review', '/t/', '/s/', '/question/', '/topic/', '/blog/', '/learn/', '/docs/', 'what-is', 'whatis', 'explained', 'basics', 'introduction', 'getting-started', '/addons/', '/addon/', '/plugins/', '/plugin/', '/extensions/', '/extension/', '/themes/', '/theme/', '/templates/', '/template/', '/snippets/', '/snippet/', '/integrations/', '/integration/', '/apps/', '/app/', '/modules/', '/module/', 'developer', 'developers', 'api-reference', 'api-docs', 'sdk', 'changelog', 'release-notes', 'roadmap', 'feature-request', 'bug-report', 'setup-guide', 'user-guide', 'admin-guide', 'dev-guide', 'quick-start', 'best-practices', 'case-study', 'case-studies', 'comparison', 'vs', 'alternative', 'alternatives', 'pricing', 'plans', 'demo', 'demos', 'example', 'examples', 'sample', 'samples', 'test', 'tests', 'sandbox']
LIVE_KEY_PATTERNS = {'STRIPE_LIVE': re.compile('pk_live_[0-9A-Za-z]{24,}'), 'PAYPAL_LIVE': re.compile('client-id=([A-Za-z0-9\\-_]{50,})|paypal\\.com/sdk/js\\?client-id=([A-Za-z0-9\\-_]{50,})'), 'BRAINTREE_LIVE': re.compile('(production_[a-z0-9]{16}_[a-z0-9]{32})|authorizationFingerprint')}
CAPTCHA_PATTERNS = [re.compile('captcha', re.I), re.compile('recaptcha', re.I), re.compile('hcaptcha', re.I), re.compile('cf-turnstile', re.I), re.compile('unusual.*traffic', re.I), re.compile('automated.*queries', re.I), re.compile('rate.?limit', re.I), re.compile('too.*many.*requests', re.I), re.compile('please.*verify', re.I), re.compile('human.*verification', re.I)]
WC_URL_PATTERNS = [re.compile('/my-account/?$', re.I), re.compile('/my-account/payment-methods/?', re.I), re.compile('/my-account/add-payment-method/?', re.I), re.compile('/my-account/orders/?', re.I), re.compile('/my-account/edit-address/?', re.I), re.compile('/my-account/edit-account/?', re.I), re.compile('/my-account/subscriptions/?', re.I), re.compile('/my-account/view-order/', re.I), re.compile('/my-account/downloads/?', re.I), re.compile('/checkout/?$', re.I), re.compile('/checkout/order-pay/', re.I), re.compile('/checkout/order-received/', re.I), re.compile('/cart/?$', re.I), re.compile('/shop/?', re.I), re.compile('/product/', re.I), re.compile('/product-category/', re.I), re.compile('\\?add-to-cart=', re.I), re.compile('\\?wc-ajax=', re.I), re.compile('/wc-api/', re.I)]
USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0']
REFERERS = ['https://www.google.com/', 'https://www.bing.com/', 'https://duckduckgo.com/', 'https://search.yahoo.com/', 'https://www.ecosia.org/', '']

class SearchEngine:

    def __init__(self, name):
        self.name = name
        self.blocked = False
        self.last_used = 0
        self.request_count = 0

    def get_delay(self):
        base = random.uniform(3, 6)
        if self.request_count > 5:
            base += random.uniform(2, 4)
        return base

class ProxyManager:

    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.enabled = False
        self.failed_proxies = set()
        self.proxy_stats = {'success': 0, 'failed': 0}

    def parse_proxy(self, proxy_line: str) -> dict:
        proxy_line = proxy_line.strip()
        if not proxy_line:
            return None
        parts = proxy_line.split(':')
        if len(parts) == 2:
            return {'host': parts[0], 'port': parts[1], 'user': None, 'pass': None}
        elif len(parts) == 4:
            return {'host': parts[0], 'port': parts[1], 'user': parts[2], 'pass': parts[3]}
        elif len(parts) == 3:
            return {'host': parts[0], 'port': parts[1], 'user': parts[2], 'pass': None}
        return None

    def load_from_file(self, file_path: str) -> int:
        try:
            if not os.path.exists(file_path):
                console.print(f'[red]Proxy file not found: {file_path}[/]')
                return 0
            with open(file_path, 'r') as f:
                lines = f.readlines()
            count = 0
            for line in lines:
                proxy = self.parse_proxy(line)
                if proxy:
                    self.proxies.append(proxy)
                    count += 1
            if count > 0:
                self.enabled = True
            return count
        except Exception as e:
            console.print(f'[red]Error loading proxies: {e}[/]')
            return 0

    def load_from_input(self, proxy_text: str) -> int:
        lines = proxy_text.strip().split('\n')
        count = 0
        for line in lines:
            proxy = self.parse_proxy(line)
            if proxy:
                self.proxies.append(proxy)
                count += 1
        if count > 0:
            self.enabled = True
        return count

    def get_next_proxy(self) -> dict:
        if not self.proxies:
            return None
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_index]
            proxy_key = f"{proxy['host']}:{proxy['port']}"
            self.current_index = (self.current_index + 1) % len(self.proxies)
            if proxy_key not in self.failed_proxies:
                return proxy
            attempts += 1
        self.failed_proxies.clear()
        return self.proxies[0] if self.proxies else None

    def get_proxy_url(self, proxy: dict) -> str:
        if not proxy:
            return None
        if proxy['user'] and proxy['pass']:
            return f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
        return f"http://{proxy['host']}:{proxy['port']}"

    def get_proxy_auth(self, proxy: dict):
        if proxy and proxy['user'] and proxy['pass']:
            return aiohttp.BasicAuth(proxy['user'], proxy['pass'])
        return None

    def mark_failed(self, proxy: dict, reason: str=''):
        if proxy:
            proxy_key = f"{proxy['host']}:{proxy['port']}"
            self.failed_proxies.add(proxy_key)
            self.proxy_stats['failed'] += 1
            if reason:
                console.print(f"[red]Proxy {proxy['host']}:{proxy['port']} failed: {reason}[/]")

    def mark_success(self, proxy: dict):
        self.proxy_stats['success'] += 1

    def get_status(self) -> str:
        if not self.enabled:
            return 'Disabled'
        active = len(self.proxies) - len(self.failed_proxies)
        return f'{active}/{len(self.proxies)} active'
CONFIG_FILE = 'gate_config.txt'

class GateScanner:

    def __init__(self, license_data=None):
        self.found_gates = []
        self.checked_count = 0
        self.scanned_urls = set()
        self.output_file = 'realgates.txt'
        self.stats = {'stripe': 0, 'paypal': 0, 'braintree': 0, 'square': 0, 'woocommerce': 0, 'shopify': 0, 'other': 0}
        self.captcha_count = 0
        self.api_exhausted = False
        self.api_requests_made = 0
        self.search_engines = {'duckduckgo': SearchEngine('DuckDuckGo'), 'brave': SearchEngine('Brave'), 'bing': SearchEngine('Bing'), 'yahoo': SearchEngine('Yahoo'), 'ecosia': SearchEngine('Ecosia'), 'qwant': SearchEngine('Qwant')}
        self.current_ua = random.choice(USER_AGENTS)
        self.session_cookies = {}
        self.api_key = None
        self.cx = None
        self.license_data = license_data
        self.proxy_manager = ProxyManager()
        self.load_config()

    def setup_proxies(self) -> bool:
        console.print('\n[bold cyan]Proxy Configuration[/]')
        console.print('[dim]Proxies help avoid rate limiting and IP blocks[/]\n')
        try:
            use_proxy = input('  Use proxies? (y/n): ').strip().lower()
        except KeyboardInterrupt:
            console.print('\n[dim]Cancelled.[/]')
            return False
        if use_proxy != 'y':
            console.print('[dim]  Proxies disabled.[/]\n')
            return False
        console.print('\n  [cyan]1[/] - Load from file (txt)')
        console.print('  [cyan]2[/] - Paste proxies manually')
        console.print('\n[dim]  Supported formats: ip:port or ip:port:user:pass[/]\n')
        try:
            method = input('  Select method [1-2]: ').strip()
        except KeyboardInterrupt:
            console.print('\n[dim]Cancelled.[/]')
            return False
        if method == '1':
            try:
                file_path = input('  Enter proxy file path: ').strip()
            except KeyboardInterrupt:
                console.print('\n[dim]Cancelled.[/]')
                return False
            if not file_path:
                console.print('[red]  No file path provided.[/]')
                return False
            count = self.proxy_manager.load_from_file(file_path)
            if count > 0:
                console.print(f'[green]  Loaded {count} proxies from file.[/]\n')
                return True
            else:
                console.print('[red]  No valid proxies found in file.[/]')
                return False
        elif method == '2':
            console.print('\n[dim]  Paste proxies (one per line). Enter empty line when done:[/]')
            lines = []
            try:
                while True:
                    line = input('  ').strip()
                    if not line:
                        break
                    lines.append(line)
            except KeyboardInterrupt:
                console.print('\n[dim]Cancelled.[/]')
                return False
            if not lines:
                console.print('[red]  No proxies provided.[/]')
                return False
            proxy_text = '\n'.join(lines)
            count = self.proxy_manager.load_from_input(proxy_text)
            if count > 0:
                console.print(f'[green]  Loaded {count} proxies.[/]\n')
                return True
            else:
                console.print('[red]  No valid proxies found.[/]')
                return False
        return False

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line.startswith('API_KEY='):
                            self.api_key = line.split('=', 1)[1]
                        elif line.startswith('CX='):
                            self.cx = line.split('=', 1)[1]
        except Exception:
            pass

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                if self.api_key:
                    f.write(f'API_KEY={self.api_key}\n')
                if self.cx:
                    f.write(f'CX={self.cx}\n')
        except Exception:
            pass

    def show_api_status(self):
        if self.api_key and self.cx:
            masked_key = self.api_key[:8] + '...' + self.api_key[-4:] if len(self.api_key) > 12 else '****'
            masked_cx = self.cx[:6] + '...' + self.cx[-4:] if len(self.cx) > 10 else '****'
            console.print(f'[dim]API Key:[/] [green]{masked_key}[/]  [dim]CX:[/] [green]{masked_cx}[/]')
        else:
            console.print('[dim]API Keys:[/] [yellow]Not configured[/]')
        console.print()

    def rotate_identity(self):
        self.current_ua = random.choice(USER_AGENTS)
        self.session_cookies = {}

    def get_headers(self, referer=None):
        return {'User-Agent': self.current_ua, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none' if not referer else 'cross-site', 'Sec-Fetch-User': '?1', 'Cache-Control': 'max-age=0', 'Referer': referer or random.choice(REFERERS), 'DNT': '1'}

    def detect_captcha(self, text, source=''):
        for pattern in CAPTCHA_PATTERNS:
            if pattern.search(text):
                self.captcha_count += 1
                captcha_type = pattern.pattern.replace('.*', ' ').replace('.?', '').replace('\\', '').strip()
                console.print(f"\n[bold red]{'━' * 50}[/]")
                console.print(f'[bold red]⚠ CAPTCHA DETECTED[/] [dim]#{self.captcha_count}[/]')
                if source:
                    console.print(f'  [dim]Source:[/] [yellow]{source[:45]}...[/]')
                console.print(f'  [dim]Type:[/] [red]{captcha_type.upper()}[/]')
                console.print(f'  [dim]Action:[/] Rotating identity & switching engine...')
                console.print(f"[bold red]{'━' * 50}[/]\n")
                self.rotate_identity()
                return True
        return False

    def detect_block(self, status_code, source=''):
        if status_code in [403, 429, 503, 401, 406, 451, 202]:
            self.captcha_count += 1
            status_msgs = {403: 'FORBIDDEN', 429: 'RATE LIMITED', 503: 'SERVICE UNAVAILABLE', 401: 'UNAUTHORIZED', 406: 'NOT ACCEPTABLE', 451: 'BLOCKED', 202: 'CAPTCHA CHALLENGE'}
            console.print(f"\n[bold red]{'━' * 50}[/]")
            console.print(f'[bold red]⚠ BLOCKED[/] [dim]#{self.captcha_count}[/]')
            if source:
                console.print(f'  [dim]Engine:[/] [yellow]{source}[/]')
            console.print(f"  [dim]Status:[/] [red]{status_code} - {status_msgs.get(status_code, 'ERROR')}[/]")
            console.print(f'  [dim]Action:[/] Rotating identity & adding delay...')
            console.print(f"[bold red]{'━' * 50}[/]\n")
            self.rotate_identity()
            return True
        return False

    def show_banner(self):
        console.clear()
        print_banner()
        console.print(Align.center(Text('Payment Gateway Discovery Tool v1.0', style='dim white')))
        console.print(Align.center(Text('WooCommerce + Shopify + Direct Search', style='dim green')))
        console.print()
        self.show_license_info()
        self.show_api_status()

    def show_license_info(self):
        if not self.license_data:
            return
        data = self.license_data
        discord_user = data.get('discord_username', 'Unknown')
        status = data.get('status', 'unknown').upper()
        status_color = 'green' if status == 'ACTIVE' else 'red'
        hwid = data.get('hwid', '')
        masked_hwid = f"{hwid[:4]}{'*' * 8}{hwid[-4:]}" if hwid and len(hwid) > 8 else 'N/A'
        license_key = data.get('license_key', '')
        masked_key = f"{license_key[:4]}{'*' * 8}{license_key[-4:]}" if license_key and len(license_key) > 8 else 'N/A'
        expires_text = 'Lifetime'
        expires_color = 'green'
        if data.get('expires_at'):
            try:
                expires = datetime.fromisoformat(data['expires_at'])
                remaining = expires - datetime.utcnow()
                days = max(remaining.days, 0)
                expires_text = f"{expires.strftime('%Y-%m-%d')} ({days} days)"
                if days <= 7:
                    expires_color = 'red'
                elif days <= 30:
                    expires_color = 'yellow'
            except:
                expires_text = 'Unknown'
        table = Table.grid(padding=(0, 2))
        table.add_column(style='dim', justify='right', width=12)
        table.add_column(style='white')
        table.add_row('Status', Text(f' {status} ', style=f'bold {status_color} reverse'))
        table.add_row('User', Text(discord_user, style='bold magenta'))
        table.add_row('Device', Text(masked_hwid, style='cyan'))
        table.add_row('Expires', Text(expires_text, style=f'bold {expires_color}'))
        table.add_row('License', Text(masked_key, style='dim cyan'))
        panel = Panel(Align.center(table), title='[bold cyan]LICENSE INFO[/]', border_style='dim cyan', box=box.ROUNDED, padding=(0, 2))
        console.print(Align.center(panel))
        console.print()

    def show_menu(self):
        table = Table(box=box.ROUNDED, border_style='dim cyan', show_header=False, padding=(0, 2))
        table.add_column('Option', style='bold white', width=8)
        table.add_column('Description', style='dim white')
        table.add_row('[cyan]1[/]', 'Google Custom Search API (100 queries/day limit)')
        table.add_row('[cyan]2[/]', 'Multi-Engine Search (DuckDuckGo, Brave, Bing...)')
        table.add_row('[cyan]3[/]', 'Update API Keys')
        table.add_row('[cyan]4[/]', 'Exit')
        console.print()
        console.print(Panel(table, title='[bold white]Select Search Mode[/]', border_style='cyan', box=box.ROUNDED))
        console.print()

    def save_result(self, url, gateway_type, has_card_form, live_keys=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'CHARGEABLE' if has_card_form else 'DETECTED'
        keys_str = ''
        if live_keys:
            keys_str = ' | KEYS: ' + ', '.join([f'{k}={v}' for k, v in live_keys.items()])
        result_line = f'[{timestamp}] {url} | {gateway_type} | {status}{keys_str}\n'
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(result_line)
        self.found_gates.append({'url': url, 'gateway': gateway_type, 'status': status, 'time': timestamp, 'keys': live_keys})
        gate_lower = gateway_type.lower()
        if 'stripe' in gate_lower:
            self.stats['stripe'] += 1
        elif 'paypal' in gate_lower:
            self.stats['paypal'] += 1
        elif 'braintree' in gate_lower:
            self.stats['braintree'] += 1
        elif 'square' in gate_lower:
            self.stats['square'] += 1
        elif 'woocommerce' in gate_lower:
            self.stats['woocommerce'] += 1
        elif 'shopify' in gate_lower:
            self.stats['shopify'] += 1
        else:
            self.stats['other'] += 1

    def detect_gateway(self, html):
        detected = []
        for gateway_name, patterns in GATEWAY_PATTERNS.items():
            for pattern in patterns:
                if pattern.search(html):
                    detected.append(gateway_name)
                    break
        return detected

    def detect_wc_endpoints(self, url, html):
        endpoints_found = []
        url_lower = url.lower()
        for pattern in WC_URL_PATTERNS:
            if pattern.search(url_lower):
                match = pattern.pattern.replace('\\', '').replace('/?$', '').replace('/?', '').replace('re.I', '').strip()
                if match not in endpoints_found:
                    endpoints_found.append(match)
        wc_link_patterns = [('href=["\\\'][^"\\\']*(/my-account/?)["\\\']', '/my-account'), ('href=["\\\'][^"\\\']*(/my-account/payment-methods/?)["\\\']', '/my-account/payment-methods'), ('href=["\\\'][^"\\\']*(/my-account/add-payment-method/?)["\\\']', '/my-account/add-payment-method'), ('href=["\\\'][^"\\\']*(/my-account/orders/?)["\\\']', '/my-account/orders'), ('href=["\\\'][^"\\\']*(/checkout/?)["\\\']', '/checkout'), ('href=["\\\'][^"\\\']*(/cart/?)["\\\']', '/cart')]
        for pattern, endpoint in wc_link_patterns:
            if re.search(pattern, html, re.I):
                if endpoint not in endpoints_found:
                    endpoints_found.append(endpoint)
        return endpoints_found

    def has_card_form(self, html):
        for pattern in CARD_PATTERNS:
            if pattern.search(html):
                return True
        return False

    def is_blocked(self, url):
        if not url:
            return True
        url_lower = url.lower()
        parsed = urlparse(url_lower)
        domain = parsed.netloc
        if any((blocked in domain for blocked in BLOCKED_DOMAINS)):
            return True
        if any((kw in url_lower for kw in BLOCKED_URL_KEYWORDS)):
            return True
        return False

    def has_checkout_keyword(self, url):
        url_lower = url.lower()
        return any((kw in url_lower for kw in CHECKOUT_KEYWORDS))

    def has_wc_endpoint(self, url):
        url_lower = url.lower()
        for pattern in WC_URL_PATTERNS:
            if pattern.search(url_lower):
                return True
        return False

    def extract_live_keys(self, html):
        keys_found = {}
        stripe_match = re.search('(pk_live_[0-9A-Za-z]{24,})', html)
        if stripe_match:
            key = stripe_match.group(1)
            if len(key) >= 32:
                keys_found['STRIPE_LIVE'] = key
        paypal_match = re.search('client-id[=:][\\"\\\']?([A-Za-z0-9\\-_]{50,})', html)
        if paypal_match:
            keys_found['PAYPAL_LIVE'] = paypal_match.group(1)
        braintree_match = re.search('(production_[a-z0-9]{16}_[a-z0-9]{32})', html)
        if braintree_match:
            keys_found['BRAINTREE_LIVE'] = braintree_match.group(1)
        return keys_found

    async def scan_url(self, url, session):
        if not url or url in self.scanned_urls or self.is_blocked(url):
            return None
        self.scanned_urls.add(url)
        self.checked_count += 1
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        proxy_display = f"[dim cyan]({proxy['ip']}:{proxy['port']})[/]" if proxy else ''
        console.print(f'[dim]  Scanning [{self.checked_count}]:[/] {url[:55]}... {proxy_display}', end='\r')
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with session.get(url, headers=self.get_headers(), allow_redirects=True, ssl=False, timeout=timeout, proxy=proxy_url) as response:
                if self.detect_block(response.status, url):
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'HTTP {response.status}')
                    return None
                if response.status != 200:
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'HTTP {response.status}')
                    return None
                html = await response.text()
                if self.detect_captcha(html, url):
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'Captcha detected')
                    return None
                if len(html) < 500:
                    return None
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                live_keys = self.extract_live_keys(html)
                gateways = self.detect_gateway(html)
                wc_endpoints = self.detect_wc_endpoints(url, html)
                if not gateways:
                    return None
                has_card = self.has_card_form(html)
                has_checkout_kw = self.has_checkout_keyword(url)
                has_wc_url = self.has_wc_endpoint(url)
                is_real_gate = False
                if live_keys:
                    is_real_gate = True
                elif has_card and has_checkout_kw:
                    is_real_gate = True
                elif has_card and any((g in ['STRIPE', 'PAYPAL', 'BRAINTREE', 'SQUARE', 'WOOCOMMERCE', 'SHOPIFY'] for g in gateways)):
                    is_real_gate = True
                elif has_wc_url and 'WOOCOMMERCE' in gateways:
                    is_real_gate = True
                elif wc_endpoints and 'WOOCOMMERCE' in gateways:
                    is_real_gate = True
                if not is_real_gate:
                    return None
                gateway_str = ' + '.join(gateways)
                self.save_result(url, gateway_str, has_card, live_keys if live_keys else None)
                status_icon = '[green]●[/]' if has_card else '[yellow]○[/]'
                status_text = 'CHARGEABLE' if has_card else 'DETECTED'
                console.print(f'\n{status_icon} [bold green]FOUND[/] #{len(self.found_gates)}')
                console.print(f"  [dim]URL:[/] [cyan]{url[:70]}{('...' if len(url) > 70 else '')}[/]")
                console.print(f'  [dim]Gateway:[/] [bold magenta]{gateway_str}[/]')
                console.print(f"  [dim]Status:[/] [{('green' if has_card else 'yellow')}]{status_text}[/]")
                if live_keys:
                    for key_type, key_val in live_keys.items():
                        console.print(f'  [dim]{key_type}:[/] [bold green]{key_val}[/]')
                return {'url': url, 'gateway': gateway_str, 'status': status_text, 'keys': live_keys}
        except asyncio.TimeoutError:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Request timed out')
            return None
        except aiohttp.ClientProxyConnectionError:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy connection failed')
            return None
        except aiohttp.ClientHttpProxyError as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, f'Proxy auth failed: {e.status}')
            return None
        except aiohttp.ClientConnectorError:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Connection refused')
            return None
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:30])
            return None

    async def search_duckduckgo(self, dork, session):
        engine = self.search_engines['duckduckgo']
        if engine.blocked:
            return []
        urls = []
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        try:
            await asyncio.sleep(engine.get_delay())
            engine.request_count += 1
            search_url = f'https://html.duckduckgo.com/html/?q={quote(dork)}'
            async with session.get(search_url, headers=self.get_headers('https://duckduckgo.com/'), allow_redirects=True, ssl=False, proxy=proxy_url) as response:
                if self.detect_block(response.status, 'DuckDuckGo'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'DuckDuckGo blocked ({response.status})')
                    return []
                html = await response.text()
                if self.detect_captcha(html, 'DuckDuckGo'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'DuckDuckGo captcha')
                    return []
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.select('a.result__a'):
                    href = link.get('href', '')
                    if href and 'http' in href:
                        if '//duckduckgo.com/l/?uddg=' in href:
                            try:
                                parsed = parse_qs(urlparse(href).query)
                                if 'uddg' in parsed:
                                    actual_url = parsed['uddg'][0]
                                    if not self.is_blocked(actual_url):
                                        urls.append(actual_url)
                            except:
                                pass
                        elif not self.is_blocked(href):
                            urls.append(href)
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy error')
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:20])
        return urls[:15]

    async def search_brave(self, dork, session):
        engine = self.search_engines['brave']
        if engine.blocked:
            return []
        urls = []
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        try:
            await asyncio.sleep(engine.get_delay())
            engine.request_count += 1
            search_url = f'https://search.brave.com/search?q={quote(dork)}'
            async with session.get(search_url, headers=self.get_headers('https://search.brave.com/'), allow_redirects=True, ssl=False, proxy=proxy_url) as response:
                if self.detect_block(response.status, 'Brave'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'Brave blocked ({response.status})')
                    return []
                html = await response.text()
                if self.detect_captcha(html, 'Brave'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'Brave captcha')
                    return []
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.select('a[href]'):
                    href = link.get('href', '')
                    if href.startswith('http') and (not 'brave.com' in href):
                        if not self.is_blocked(href):
                            urls.append(href)
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy error')
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:20])
        return urls[:15]

    async def search_bing(self, dork, session):
        engine = self.search_engines['bing']
        if engine.blocked:
            return []
        urls = []
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        try:
            await asyncio.sleep(engine.get_delay())
            engine.request_count += 1
            search_url = f'https://www.bing.com/search?q={quote(dork)}'
            async with session.get(search_url, headers=self.get_headers('https://www.bing.com/'), allow_redirects=True, ssl=False, proxy=proxy_url) as response:
                if self.detect_block(response.status, 'Bing'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'Bing blocked ({response.status})')
                    return []
                html = await response.text()
                if self.detect_captcha(html, 'Bing'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'Bing captcha')
                    return []
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.select('li.b_algo h2 a'):
                    href = link.get('href', '')
                    if href and href.startswith('http'):
                        if not self.is_blocked(href):
                            urls.append(href)
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy error')
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:20])
        return urls[:15]

    async def search_yahoo(self, dork, session):
        engine = self.search_engines['yahoo']
        if engine.blocked:
            return []
        urls = []
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        try:
            await asyncio.sleep(engine.get_delay())
            engine.request_count += 1
            search_url = f'https://search.yahoo.com/search?p={quote(dork)}'
            async with session.get(search_url, headers=self.get_headers('https://search.yahoo.com/'), allow_redirects=True, ssl=False, proxy=proxy_url) as response:
                if self.detect_block(response.status, 'Yahoo'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'Yahoo blocked ({response.status})')
                    return []
                html = await response.text()
                if self.detect_captcha(html, 'Yahoo'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'Yahoo captcha')
                    return []
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.select('div.algo-sr a'):
                    href = link.get('href', '')
                    if href and 'http' in href:
                        if not self.is_blocked(href):
                            urls.append(href)
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy error')
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:20])
        return urls[:15]

    async def search_ecosia(self, dork, session):
        engine = self.search_engines['ecosia']
        if engine.blocked:
            return []
        urls = []
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        try:
            await asyncio.sleep(engine.get_delay())
            engine.request_count += 1
            search_url = f'https://www.ecosia.org/search?q={quote(dork)}'
            async with session.get(search_url, headers=self.get_headers('https://www.ecosia.org/'), allow_redirects=True, ssl=False, proxy=proxy_url) as response:
                if self.detect_block(response.status, 'Ecosia'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'Ecosia blocked ({response.status})')
                    return []
                html = await response.text()
                if self.detect_captcha(html, 'Ecosia'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'Ecosia captcha')
                    return []
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.select('a.result__link'):
                    href = link.get('href', '')
                    if href and href.startswith('http'):
                        if not self.is_blocked(href):
                            urls.append(href)
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy error')
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:20])
        return urls[:15]

    async def search_qwant(self, dork, session):
        engine = self.search_engines['qwant']
        if engine.blocked:
            return []
        urls = []
        proxy = self.proxy_manager.get_next_proxy()
        proxy_url = self.proxy_manager.get_proxy_url(proxy) if proxy else None
        try:
            await asyncio.sleep(engine.get_delay())
            engine.request_count += 1
            search_url = f'https://www.qwant.com/?q={quote(dork)}&t=web'
            async with session.get(search_url, headers=self.get_headers('https://www.qwant.com/'), allow_redirects=True, ssl=False, proxy=proxy_url) as response:
                if self.detect_block(response.status, 'Qwant'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, f'Qwant blocked ({response.status})')
                    return []
                html = await response.text()
                if self.detect_captcha(html, 'Qwant'):
                    engine.blocked = True
                    if proxy:
                        self.proxy_manager.mark_failed(proxy, 'Qwant captcha')
                    return []
                if proxy:
                    self.proxy_manager.mark_success(proxy)
                url_pattern = re.compile('https?://[^\\s<>"\\\']+')
                matches = url_pattern.findall(html)
                for url in matches:
                    if not self.is_blocked(url) and 'qwant' not in url.lower():
                        urls.append(url)
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, 'Proxy error')
        except Exception as e:
            if proxy:
                self.proxy_manager.mark_failed(proxy, str(e)[:20])
        return urls[:15]

    async def search_google_api(self, dork, session, api_key, cx):
        if self.api_exhausted:
            return []
        urls = []
        try:
            self.api_requests_made += 1
            if self.api_requests_made > 100:
                self.api_exhausted = True
                console.print('\n[bold yellow]⚠ Google API daily limit reached (100 queries)[/]\n')
                return []
            search_url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={quote(dork)}&num=10'
            async with session.get(search_url, ssl=False) as response:
                if response.status == 429:
                    self.api_exhausted = True
                    console.print('\n[bold yellow]⚠ Google API rate limited[/]\n')
                    return []
                if response.status == 403:
                    self.api_exhausted = True
                    console.print('\n[bold red]⚠ Google API access denied - check your API key[/]\n')
                    return []
                if response.status != 200:
                    return []
                data = await response.json()
                for item in data.get('items', []):
                    url = item.get('link', '')
                    if url and (not self.is_blocked(url)):
                        urls.append(url)
        except Exception as e:
            pass
        return urls

    async def run_multi_engine_search(self):
        self.setup_proxies()
        proxy_status = self.proxy_manager.get_status()
        console.print(f'\n[bold cyan]Starting Multi-Engine Search...[/]')
        console.print(f'[dim]Proxy Status: {proxy_status}[/]\n')
        connector = aiohttp.TCPConnector(limit=5, force_close=True)
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            total_dorks = len(DORKS)
            with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), BarColumn(), TaskProgressColumn(), console=console) as progress:
                task = progress.add_task('[cyan]Searching...', total=total_dorks)
                for i, dork in enumerate(DORKS):
                    progress.update(task, description=f'[cyan]Dork {i + 1}/{total_dorks}')
                    active_engines = [e for e in self.search_engines.values() if not e.blocked]
                    if not active_engines:
                        console.print('\n[bold red]All search engines blocked! Waiting 60s...[/]\n')
                        await asyncio.sleep(60)
                        for engine in self.search_engines.values():
                            engine.blocked = False
                            engine.request_count = 0
                        self.rotate_identity()
                    all_urls = set()
                    search_tasks = []
                    if not self.search_engines['duckduckgo'].blocked:
                        search_tasks.append(self.search_duckduckgo(dork, session))
                    if not self.search_engines['brave'].blocked:
                        search_tasks.append(self.search_brave(dork, session))
                    if not self.search_engines['bing'].blocked:
                        search_tasks.append(self.search_bing(dork, session))
                    if search_tasks:
                        results = await asyncio.gather(*search_tasks, return_exceptions=True)
                        for result in results:
                            if isinstance(result, list):
                                all_urls.update(result)
                    await asyncio.sleep(random.uniform(1, 2))
                    search_tasks2 = []
                    if not self.search_engines['yahoo'].blocked:
                        search_tasks2.append(self.search_yahoo(dork, session))
                    if not self.search_engines['ecosia'].blocked:
                        search_tasks2.append(self.search_ecosia(dork, session))
                    if not self.search_engines['qwant'].blocked:
                        search_tasks2.append(self.search_qwant(dork, session))
                    if search_tasks2:
                        results2 = await asyncio.gather(*search_tasks2, return_exceptions=True)
                        for result in results2:
                            if isinstance(result, list):
                                all_urls.update(result)
                    if all_urls:
                        scan_tasks = [self.scan_url(url, session) for url in list(all_urls)[:20]]
                        await asyncio.gather(*scan_tasks, return_exceptions=True)
                    progress.update(task, advance=1)
                    if (i + 1) % 5 == 0:
                        self.rotate_identity()
                        await asyncio.sleep(random.uniform(3, 5))
        self.show_summary()

    async def run_google_api_search(self, api_key, cx):
        console.print('\n[bold cyan]Starting Google Custom Search API...[/]\n')
        console.print(f'[dim]API Limit: 100 queries/day | Using {len(DORKS)} dorks[/]\n')
        connector = aiohttp.TCPConnector(limit=5, force_close=True)
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            total_dorks = len(DORKS)
            with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), BarColumn(), TaskProgressColumn(), console=console) as progress:
                task = progress.add_task('[cyan]Searching...', total=total_dorks)
                for i, dork in enumerate(DORKS):
                    if self.api_exhausted:
                        console.print('\n[yellow]API limit reached. Stopping.[/]\n')
                        break
                    progress.update(task, description=f'[cyan]Dork {i + 1}/{total_dorks} | API: {self.api_requests_made}/100')
                    urls = await self.search_google_api(dork, session, api_key, cx)
                    if urls:
                        scan_tasks = [self.scan_url(url, session) for url in urls]
                        await asyncio.gather(*scan_tasks, return_exceptions=True)
                    progress.update(task, advance=1)
                    await asyncio.sleep(0.5)
        self.show_summary()

    def show_summary(self):
        console.print('\n')
        console.print(Panel.fit(f"[bold white]Scan Complete[/]\n\n[cyan]URLs Checked:[/] {self.checked_count}\n[green]Gates Found:[/] {len(self.found_gates)}\n[yellow]Captchas Hit:[/] {self.captcha_count}\n\n[bold]By Gateway:[/]\n  Stripe: {self.stats['stripe']}\n  PayPal: {self.stats['paypal']}\n  Braintree: {self.stats['braintree']}\n  Square: {self.stats['square']}\n  WooCommerce: {self.stats['woocommerce']}\n  Shopify: {self.stats['shopify']}\n  Other: {self.stats['other']}\n\n[dim]Results saved to: {self.output_file}[/]", title='[bold green]Summary[/]', border_style='green'))

    def update_api_keys(self):
        console.print('\n[bold white]Update Google API Keys[/]')
        console.print('[dim]Get your API key from: https://developers.google.com/custom-search/v1/overview[/]')
        console.print('[dim]Create Custom Search Engine: https://programmablesearchengine.google.com/[/]\n')
        if self.api_key:
            console.print(f'[dim]Current API Key:[/] {self.api_key[:8]}...{self.api_key[-4:]}')
        if self.cx:
            console.print(f'[dim]Current CX:[/] {self.cx[:6]}...{self.cx[-4:]}')
        console.print()
        try:
            new_key = input('  Enter new API Key (or press Enter to keep current): ').strip()
            new_cx = input('  Enter new Search Engine ID (cx) (or press Enter to keep current): ').strip()
        except KeyboardInterrupt:
            console.print('\n[dim]Cancelled.[/]')
            return
        if new_key:
            self.api_key = new_key
        if new_cx:
            self.cx = new_cx
        if self.api_key and self.cx:
            self.save_config()
            console.print('\n[bold green]API keys saved successfully![/]')
        else:
            console.print('\n[yellow]API keys not complete. Both API Key and CX are required.[/]')

    async def main(self):
        print_banner()
        self.show_menu()
        try:
            choice = input('  Select option [1-4]: ').strip()
        except KeyboardInterrupt:
            console.print('\n[dim]Exiting...[/]')
            return
        if choice == '1':
            if self.api_key and self.cx:
                console.print(f'\n[dim]Using saved API credentials...[/]')
                await self.run_google_api_search(self.api_key, self.cx)
            else:
                console.print('\n[bold white]Google Custom Search API Setup[/]')
                console.print('[dim]Get your API key from: https://developers.google.com/custom-search/v1/overview[/]')
                console.print('[dim]Create Custom Search Engine: https://programmablesearchengine.google.com/[/]\n')
                try:
                    api_key = input('  Enter API Key: ').strip()
                    cx = input('  Enter Search Engine ID (cx): ').strip()
                except KeyboardInterrupt:
                    console.print('\n[dim]Cancelled.[/]')
                    return
                if api_key and cx:
                    self.api_key = api_key
                    self.cx = cx
                    self.save_config()
                    console.print('[dim]API keys saved for future use.[/]\n')
                    await self.run_google_api_search(api_key, cx)
                else:
                    console.print('[red]Invalid API credentials.[/]')
        elif choice == '2':
            await self.run_multi_engine_search()
        elif choice == '3':
            self.update_api_keys()
            await self.main()
        elif choice == '4':
            console.print('\n[dim]Goodbye![/]')
        else:
            console.print('[red]Invalid option.[/]')
if __name__ == '__main__':
    license_data = {'status': 'active', 'discord_username': 'User', 'expires_at': None, 'last_used_at': None, 'license_key': 'FREE-LICENSE'}
    scanner = GateScanner(license_data)
    asyncio.run(scanner.main())