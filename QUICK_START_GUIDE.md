# 🚀 QUICK START GUIDE - Beast Mode Scanner

## Three Core Tasks

### 1️⃣ TEST THE SCANNER - Run Your First Scan
### 2️⃣ LAUNCH THE DASHBOARD - See the Web UI  
### 3️⃣ ADD CUSTOM GATEWAYS - Expand Coverage

---

## Task 1: Test the Scanner 🔍

### Step 1: Open Terminal and Navigate to Project

```bash
cd Gateway-Finder
```

### Step 2: Install Dependencies (if not already done)

```bash
pip install -r requirements.txt
```

### Step 3: Run the Beast Mode Scanner

```bash
python gateway_scanner_beast.py
```

### Expected Output:

```
🔥 GATE SCAN - BEAST MODE EDITION 🔥

📋 Scanning 25+ payment gateways...

✓ STRIPE found at https://example-store.com/checkout
✓ PAYPAL found at https://donate-site.org/payment
✓ BITPAY found at https://crypto-marketplace.xyz/pay
✓ ALIPAY found at https://china-store.com/checkout

📊 ANALYTICS DASHBOARD
────────────────────────────────────
Total Found: 47
URLs Checked: 1,203  
Blocked: 3
Average Response Time: 0.45s
```

### What's Happening:

✅ Scanner is running 25 concurrent requests  
✅ Results are being saved to `gateway_results.db`  
✅ Each found gateway is logged to separate files:  
  - `GoogleApiResult.txt` (API results)
  - `SearchEnginesResult.txt` (fallback engines)

### Configuration Options:

Edit `config.py` to customize:

```python
# Performance
MAX_CONCURRENT_REQUESTS = 25      # Increase for faster speed
REQUEST_TIMEOUT = 10              # Seconds before timeout
RATES_PER_SECOND = 2.0            # Requests per second

# Proxy (optional)
USE_PROXY_ROTATION = True
PROXY_LIST = ['http://proxy1.com:8080']
```

### Stop the Scanner:

Press `Ctrl+C` to stop gracefully

---

## Task 2: Launch the Dashboard 🎨

### Step 1: Open a NEW Terminal Window

```bash
cd Gateway-Finder
```

### Step 2: Start the Flask Web Server

```bash
python web_dashboard.py
```

### Expected Output:

```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### Step 3: Open in Browser

**Go to:** http://localhost:5000

### Dashboard Features:

**📊 Statistics Cards:**
- Total Results Found
- Results Today
- Unique Gateways
- Average Response Time

**📈 Charts:**
- Gateway Distribution (Bar Chart)
- 7-Day Timeline (Line Chart)
- Recent Results Table

**📥 Export:**
- Download results as JSON
- Click "Export Results" button

### API Endpoints (for development):

```
GET http://localhost:5000/api/stats       # Overall stats
GET http://localhost:5000/api/gateways    # Gateway breakdown
GET http://localhost:5000/api/results     # Recent results
GET http://localhost:5000/api/timeline    # 7-day data
GET http://localhost:5000/api/export      # Full export
```

### Stop the Dashboard:

Press `Ctrl+C` in the terminal

---

## Task 3: Add Custom Gateways 🎯

### Option A: Interactive Gateway Builder

```bash
python custom_gateways_manager.py
```

### Interactive Menu:

```
🎯 Custom Gateway Manager

Options:
1. Add gateway from template
2. Add custom gateway
3. List all gateways
4. Remove gateway
5. Export gateways
6. Import gateways
7. Exit
```

### Example: Add from Template

```
Select option (1-7): 1

Available Templates:
1. STRIPE
2. SHOPIFY_PAYMENTS
3. WOOCOMMERCE
4. SHOPWARE
5. PRESTASHOP
6. MAGENTO
7. SAGEPAY
...

Select template: 1
✓ Gateway 'stripe' added successfully!
```

### Example: Add Custom Gateway

```
Select option (1-7): 2

Gateway name: my_custom_payment
Keywords (comma-separated): custom_pay, payment_sdk
Dorks (comma-separated): inurl:checkout custom_pay, "custom_pay.js"
Category (default: custom): custom
Description: My custom payment processor

✓ Gateway 'my_custom_payment' added successfully!
```

### Option B: Manual Python Integration

```python
from custom_gateways_manager import CustomGatewayManager

manager = CustomGatewayManager()

# Add a gateway
manager.add_gateway(
    name='stripe_extended',
    keywords=['pk_live_', 'stripe_api'],
    dorks=['inurl:checkout stripe_api', '"pk_live_extended"'],
    category='payment_processor',
    description='Extended Stripe detection'
)

# List all
manager.list_gateways()

# Export
manager.export_gateways('my_gateways.json')
```

### Pre-configured Templates Available:

**Payment Processors:**
- Stripe, PayPal, Braintree, Square
- SagePay, WorldPay, CyberSource, OpenPay

**eCommerce Platforms:**
- Shopify Payments, WooCommerce
- Shopware, PrestaShop, Magento

**Regional Payments:**
- Trustly, Giropay, EPS, Przelewy24
- Bancontact, Sofort, Multibanco, MyBank, PostFinance

### View Custom Gateways:

```bash
python custom_gateways_manager.py
Select option (1-7): 3
```

---

## 🔄 Running All Three Together

### Terminal 1: Scanner

```bash
cd Gateway-Finder
python gateway_scanner_beast.py
```

### Terminal 2: Dashboard

```bash
cd Gateway-Finder
python web_dashboard.py
# Then open http://localhost:5000
```

### Terminal 3: Gateway Manager

```bash
cd Gateway-Finder
python custom_gateways_manager.py
# Add new gateways
```

---

## 📊 Output Files

After scanning, you'll have:

```
Gateway-Finder/
├── gateway_results.db              # SQLite database with results
├── GoogleApiResult.txt             # Google API findings
├── SearchEnginesResult.txt         # Fallback engine results
├── gateway_scanner.log             # Detailed logs
└── gateways_export.json            # Custom gateways (if exported)
```

---

## 🛠️ Troubleshooting

### Scanner Not Finding Results

**Solution:**
1. Check internet connection
2. Try without API (fallback engines will activate)
3. Check logs: `tail -f gateway_scanner.log`

### Dashboard Not Loading

**Solution:**
1. Ensure Flask is installed: `pip install Flask`
2. Check port 5000 is available
3. Try: `python web_dashboard.py --host 127.0.0.1 --port 8000`

### Custom Gateway Not Added

**Solution:**
1. Check JSON syntax in `custom_gateways.json`
2. Ensure file has write permissions
3. Verify gateway name isn't duplicate

---

## 📈 Performance Tips

1. **Faster Scanning**: Increase `MAX_CONCURRENT_REQUESTS` to 50
2. **Less Blocking**: Enable proxy rotation
3. **Better Results**: Add more dorks per gateway
4. **Database**: Regularly export and backup `gateway_results.db`

---

## 🎓 Next Steps

✅ Test Scanner  
✅ Launch Dashboard  
✅ Add Custom Gateways  

**Then:**
- 📚 Read `BEAST_MODE_DOCUMENTATION.md` for advanced features
- 🔧 Configure API keys in `config.py`
- 📊 Set up automated scanning with cron/scheduler
- 🚀 Deploy to production server

---

**You're ready! Start with Task 1 above! 🚀**
