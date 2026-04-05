# 🇳🇬 NaijaStack — Nigerian Business API Toolkit

> A Python toolkit for integrating Paystack, Flutterwave, and Termii into your Nigerian business application.

---

## 📦 What's Inside

| File | Purpose |
|------|---------|
| `nigerian_business_api_toolkit.py` | Core library — all API clients |
| `main.py` | Interactive CLI menu |
| `.env` | Your secret API keys |

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install requests python-dotenv
```

### 2. Create your `.env` file
```
PAYSTACK_SECRET_KEY=sk_test_your_key_here
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-your_key_here
TERMII_API_KEY=your_termii_key_here
```

### 3. Run the toolkit
```bash
python main.py
```

---

## 🏦 Paystack

**What it does:** Accept payments, verify transactions, resolve bank accounts, send transfers.

### Features
- Initialize a payment and get a checkout link
- Verify a transaction by reference
- Resolve any Nigerian bank account name
- List all Nigerian banks and codes
- Create recurring payment plans
- Transfer money to any bank account
- Verify webhooks

### Usage
```python
from nigerian_business_api_toolkit import PaystackClient, naira_to_kobo

client = PaystackClient()

# Initialize payment
result = client.initialize_transaction("customer@email.com", naira_to_kobo(5000))
print(result["data"]["authorization_url"])

# Verify transaction
result = client.verify_transaction("your-reference")
print(result["data"]["status"])

# Resolve bank account
result = client.resolve_account("0123456789", "058")
print(result["data"]["account_name"])
```

---

## 🦋 Flutterwave

**What it does:** Accept multi-currency payments, create virtual accounts, send transfers across Africa.

### Features
- Create a hosted payment link
- Verify a transaction by ID
- Resolve a Nigerian bank account
- List Nigerian banks
- Send bank transfers
- Create virtual bank accounts for customers

### Usage
```python
from nigerian_business_api_toolkit import FlutterwaveClient, generate_tx_ref

client = FlutterwaveClient()

# Create payment link
result = client.create_payment_link(
    amount=5000,
    currency="NGN",
    redirect_url="https://yoursite.com/callback",
    customer={"email": "user@email.com", "name": "John Doe", "phonenumber": "+2348012345678"},
    tx_ref=generate_tx_ref("FW")
)
print(result["data"]["link"])
```

---

## 📱 Termii

**What it does:** Send SMS, OTP, and WhatsApp messages to Nigerian phone numbers.

### Features
- Send SMS to any Nigerian number
- Send a 6-digit OTP for phone verification
- Verify an OTP entered by a user
- Send WhatsApp messages
- Check your SMS balance

### Usage
```python
from nigerian_business_api_toolkit import TermiiClient, validate_nigerian_phone

client = TermiiClient()

# Send OTP
result = client.send_otp(validate_nigerian_phone("08012345678"))
pin_id = result["pinId"]

# Verify OTP
result = client.verify_otp(pin_id, "123456")
print(result["verified"])  # True or False

# Send SMS
client.send_sms("+2348012345678", "Your order has been confirmed!")
```

---

## 🛠️ Utility Functions

```python
from nigerian_business_api_toolkit import (
    naira_to_kobo,        # 5000 -> 500000
    kobo_to_naira,        # 500000 -> 5000.0
    format_naira,         # 5000.0 -> "₦5,000.00"
    validate_nigerian_phone,  # "08012345678" -> "+2348012345678"
    generate_tx_ref,      # "NS-1234567890-ABC123"
    load_nigerian_banks_json, # list of 24 banks with codes
)
```

---

## 🚀 NaijaStack Facade (Single Entry Point)

```python
from nigerian_business_api_toolkit import NaijaStack

ns = NaijaStack()

# Paystack
ns.paystack.initialize_transaction("user@email.com", 500000)

# Flutterwave
ns.flutterwave.create_payment_link(...)

# Termii
ns.sms.send_otp("+2348012345678")

# Shortcuts
ns.charge("user@email.com", 5000)       # Paystack payment
ns.send_otp("08012345678")              # Termii OTP
ns.ngn_usd_rate()                       # Live exchange rate
```

---

## 🏗️ What You Can Build

| Business | Paystack | Flutterwave | Termii |
|----------|----------|-------------|--------|
| E-commerce Store | Checkout payments | Multi-currency | Order SMS |
| School Portal | Fee collection | — | Result alerts |
| Freelance Platform | Client payments | Cross-border payouts | — |
| Fintech App | Transfers | Virtual accounts | OTP login |
| Logistics App | Delivery fees | — | Delivery SMS |
| SaaS Product | Subscriptions | USD payments | — |

---

## 🔄 How It Works

```
You (menu choice)
    → main.py reads your input
        → nigerian_business_api_toolkit.py builds the HTTP request
            → API Server (Paystack / Flutterwave / Termii)
                → returns JSON response
        → toolkit formats and prints the result
    → menu appears again
```

---

## 🔐 Test vs Live Mode

| Mode | Key Format | Effect |
|------|-----------|--------|
| Test | `sk_test_...` | No real money, safe for development |
| Live | `sk_live_...` | Real transactions, use when ready to launch |

To go live, replace your test keys in `.env` with live keys from each dashboard.

---

## 🏦 Nigerian Banks Reference

| Bank | Code |
|------|------|
| Access Bank | 044 |
| GTBank | 058 |
| Zenith Bank | 057 |
| UBA | 033 |
| First Bank | 011 |
| Kuda Bank | 090267 |
| OPay | 999992 |
| PalmPay | 999991 |
| Moniepoint | 50515 |

> Full list available via `load_nigerian_banks_json()` or `ns.paystack.list_banks()`

---

## 🔑 API Key Sources

| Variable | Dashboard |
|----------|-----------|
| `PAYSTACK_SECRET_KEY` | dashboard.paystack.com → Settings → API Keys |
| `FLUTTERWAVE_SECRET_KEY` | dashboard.flutterwave.com → Settings → API Keys |
| `TERMII_API_KEY` | app.termii.com → Settings → API Key |

---

## ⚠️ Security

- Never commit your `.env` file to GitHub
- Add `.env` to your `.gitignore`
- Never share your secret keys (`sk_test_...`, `sk_live_...`)
- Public keys (`pk_test_...`) are safe to use on the frontend

---

## 📄 License

MIT — free to use for personal and commercial projects.

---

> Built for Nigerian developers 🇳🇬
