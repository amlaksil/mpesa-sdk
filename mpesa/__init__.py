#!/usr/bin/python3
"""
M-Pesa Python SDK
=================

Overview
--------
The M-Pesa Python SDK simplifies integration with the M-Pesa
API, enabling developers to interact with M-Pesa services such
as authentication, STK Push payments, Customer-to-Business
(C2B) integrations, and Business-to-Customer (B2C) payouts.

This SDK is designed for businesses and developers seeking to
integrate M-Pesa's mobile money capabilities into their applications
for payments, disbursements, and other financial services.

Key Features
------------
1. **Authentication**:
   - Retrieve OAuth2 access tokens securely.
2. **STK Push**:
   - Initiate mobile money payments directly to a customer's phone.
3. **C2B (Customer to Business)**:
   - Handle customer payments and notifications via M-Pesa.
   - Register callback URLs for validation and confirmation.
4. **B2C (Business to Customer)**:
   - Make payments from businesses to individual customers, including
salaries, loans, and rewards.
5. **Utilities**:
   - Built-in error handling, validation, and logging for better debugging.

Requirements
------------
- Python 3.7 or higher
- An M-Pesa API developer account
- Consumer Key and Consumer Secret from the M-Pesa API portal
- Publicly accessible callback URLs (for C2B and B2C)

Installation
------------
To install the SDK, clone the repository and install dependencies:

```bash
git clone https://github.com/amlaksil/mpesa-sdk.git
cd mpesa-sdk
pip install -r requirements.txt
```

Quick Start
-----------
1. Import the SDK and authenticate:
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

2. Send an STK Push request:
    ```python
    from mpesa import STKPush, Config

    stk_push = STKPush(base_url=Config.BASE_URL, access_token=access_token)
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

3. Register callback URLs for C2B:
    ```python
    from mpesa import C2B

    c2b = C2B(
        base_url="https://sandbox.safaricom.et",
        access_token=access_token
    )
    registration_response = c2b.register_url(payload={
        "ShortCode": "123456",
        "ResponseType": "Completed",
        "CommandID": "RegisterURL",
        "ConfirmationURL": "https://example.com/confirmation",
        "ValidationURL": "https://example.com/validation"
    })
    print("C2B Registration Response:", registration_response)
    ```

License
-------
This SDK is licensed under the MIT License. See the LICENSE file for details.

Support
-------
For questions, issues, or contributions, visit my GitHub repository at:
https://github.com/amlaksil/mpesa-sdk
"""

__version__ = "1.0.0"

from .auth.auth import Auth
from .config import Config
from .payments.stk_push import STKPush
from .payments.c2b import C2B
from .payments.b2c import B2C
from .utils.exceptions import (
        APIError, AuthenticationError,
        TimeoutError, NetworkError, HTTPError,
        TooManyRedirects, ValidationError
        )
from .utils.logger import get_logger
