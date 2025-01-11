# M-Pesa Python SDK

## Overview

The M-Pesa Python SDK simplifies the integration of your Python applications with the M-Pesa API, enabling seamless access to mobile money services such as payments, payouts, and transaction management. This SDK is designed to accelerate your development by providing a robust interface for M-Pesa’s STK Push, C2B, B2C, and authentication APIs.

## Features

- **Authentication**: Retrieve OAuth2 access tokens.
- **STK Push**: Initiate mobile money payments from customers.
- **Customer to Business (C2B)**: Process customer payments with validation and confirmation callbacks.
- **Business to Customer (B2C)**: Payouts for salaries, rewards, or refunds.
- **Error Handling**: Comprehensive exception management.
- **Logging**: Built-in logging for debugging and monitoring.

## Requirements
- Python 3.7 or higher
- An M-Pesa API developer account
- Consumer Key and Consumer Secret from the M-Pesa API portal
- Publicly accessible callback URLs (for C2B and B2C)

## Installation

Install the SDK using pip:

```bash
pip install mpesa_client
```

## Configuration Guide

### Option 1: Using Environment Variables

This is the recommended approach to keep your credentials and configuration secure and centralized.

1. **Create a `.env` File**

Place a `.env` file in your project root with the following content:

```dotenv
# API Base URL and Endpoints
BASE_URL=https://sandbox.safaricom.et
TOKEN_GENERATE_ENDPOINT=/v1/token/generate
STK_PUSH_ENDPOINT=/mpesa/stkpush/v1/processrequest
C2B_REGISTER_URL_ENDPOINT=/mpesa/c2b/v1/registerurl
C2B_PAYMENTS_ENDPOINT=/mpesa/c2b/v1/simulate
B2C_PAYMENT_REQUEST_ENDPOINT=/mpesa/b2c/v1/paymentrequest

# Authentication
CLIENT_KEY=your_client_key
CLIENT_SECRET=your_client_secret

# Logging and Environment
TIMEOUT=30
MPESA_LOG_DIR=./logs
LOG_LEVEL=DEBUG
ENVIRONMENT=DEV  # Set to TEST to disable console logging
```

2. **Access Configuration in Code**

The SDK automatically loads these variables using the `dotenv` package:

```python
from mpesa import Config

# Access configuration
print("Base URL:", Config.BASE_URL)
print("Client Key:", Config.CLIENT_KEY)
```

### Option 2: Overriding Configuration Directly

If you don’t want to use environment variables or need to change settings dynamically, you can override the configuration directly in your application.

#### Example:

```python
# Override configuration
Config.BASE_URL = "https://production.safaricom.et"
Config.CLIENT_KEY = "your_production_client_key"
Config.CLIENT_SECRET = "your_production_client_secret"
Config.ENVIRONMENT = "TEST"  # Disable console logs in production

print("Base URL:", Config.BASE_URL)
```

### Handling Changes in Endpoints

If M-Pesa updates its endpoints or you need to switch between environments (sandbox/production), you can easily update the relevant endpoints:

#### Example:

```python
# Set custom endpoint
Config.STK_PUSH_ENDPOINT = "/custom/stkpush/v1/processrequest"
print("Updated STK Push Endpoint:", Config.STK_PUSH_ENDPOINT)
```

## Usage

### Step 1: Authentication

Authenticate with the M-Pesa API to retrieve the access token.

```python
from mpesa import Auth

auth = Auth(
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret",
    base_url="https://sandbox.safaricom.et"
)

response = auth.get_access_token()
print("Access Token:", response.get("access_token"))
```

### Step 2: STK Push Integration

Send an STK Push request to initiate a payment from a customer.

```python
from mpesa import STKPush

stk_push = STKPush(
    base_url="https://sandbox.safaricom.et",
    access_token=access_token
)

payload = stk_push.create_payload(
    short_code="174379",
    pass_key="your_pass_key",
    BusinessShortCode="174379",
    Amount="1000",
    PartyA="254712345678",
    PartyB="174379",
    PhoneNumber="254712345678",
    CallBackURL="https://example.com/callback",
    AccountReference="INV123456",
    TransactionDesc="Payment for Invoice #123456"
)

response = stk_push.send_stk_push(payload)
print("STK Push Response:", response)
```

### Step 3: C2B Payment

Register URLs and process customer payments.

```python
from mpesa import C2B

c2b = C2B(base_url="https://sandbox.safaricom.et", access_token=access_token)

# Register validation and confirmation URLs
registration_response = c2b.register_url(payload={
    "ShortCode": "123456",
    "ResponseType": "Completed",
    "CommandID": "RegisterURL",
    "ConfirmationURL": "https://example.com/confirmation",
    "ValidationURL": "https://example.com/validation"
})

# Process a payment
payment_response = c2b.make_payment(payload={
    "ShortCode": "123456",
    "CommandID": "CustomerPayBillOnline",
    "Amount": "500",
    "Msisdn": "254700000000",
    "BillRefNumber": "INV12345"
})

print("Payment Response:", payment_response)
```

### Step 4: B2C Payout

Send payments to customers.

```python
from mpesa import B2C

b2c = B2C(
    base_url="https://api.safaricom.et",
    access_token=access_token
)

payload = {
    "amount": 5000,
    "partyA": "600000",
    "partyB": "254712345678",
    "remarks": "Loan Disbursement",
    "queueTimeoutURL": "https://yourcallback.url/timeout",
    "resultURL": "https://yourcallback.url/result"
}

response = b2c.make_payment(payload)
print(response)
```

## Logging Guide

The SDK includes a flexible logging system to capture debug and runtime information. 

### Default Behavior

- Logs are saved to the directory specified by `MPESA_LOG_DIR` (e.g., `./logs`).
- Logs are displayed in the terminal (unless `ENVIRONMENT` is set to `TEST`).

### Customizing Logging

1. **Environment Variables**

Control logging behavior via your `.env` file:

```dotenv
MPESA_LOG_DIR=./custom_logs
LOG_LEVEL=INFO
ENVIRONMENT=TEST  # Disable console logs
```

2. **Disable Console Logs Programmatically**

You can also set the environment programmatically to `TEST`:

```python
from mpesa import Config

Config.ENVIRONMENT = "TEST"  # Disables console logging
```

3. **Using the Logger**

Set up and use a logger in your application:

```python
from mpesa import get_logger

# Initialize logger
logger = get_logger(__name__)

# Log messages
logger.info("Starting the M-Pesa payment process.")
logger.debug("Debugging transaction payload.")
```

## Error Handling

The SDK includes custom exceptions for better debugging:

- **ValidationError**: Raised for invalid payloads.
- **APIError**: Raised for API-level errors.

Example:

```python
from mpesa import APIError, ValidationError

try:
    response = stk_push.send_stk_push(payload)
except ValidationError as e:
    print("Payload validation failed:", e)
except APIError as e:
    print("API error occurred:", e)
except Exception as e:
    print("An unexpected error occurred:", e)
```

## Contributing

Contributions are welcome! If you’d like to improve the SDK, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](https://mit-license.org/amlaksil). See the [LICENSE](LICENSE) file for more details.

---
*Happy coding with M-Pesa Python SDK!*
