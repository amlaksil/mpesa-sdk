# `Auth` Module Documentation

The `Auth` module in the M-Pesa SDK handles authentication by retrieving access tokens from the M-Pesa API. This module is designed to simplify the process of authenticating API requests by managing the token lifecycle and handling errors gracefully.

---

## Table of Contents

1. [Installation](#installation)
2. [Prerequisites](#prerequisites)
3. [Usage](#usage)
4. [Error Handling](#error-handling)
5. [Testing](#testing)
6. [License](#license)

---

## Installation

Ensure you have Python 3.7+ installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Prerequisites

Before using the `Auth` module, ensure the following:
1. **M-Pesa API Base URL**: Obtain the base URL for the API (e.g., sandbox or production).
2. **API Credentials**: 
   - `client_key`: Your API key (username) provided by M-Pesa.
   - `client_secret`: Your API secret (password) provided by M-Pesa.

---

## Usage

Here’s how to use the `Auth` module:

### 1. Import the Module
```python
from mpesa.auth.auth import Auth
```

### 2. Initialize the `Auth` Instance
```python
base_url = "https://sandbox.safaricom.et"  # Replace with the production URL for live environments
client_key = "YOUR_CLIENT_KEY"
client_secret = "YOUR_CLIENT_SECRET"

auth_instance = Auth(base_url=base_url, client_key=client_key, client_secret=client_secret)
```

### 3. Retrieve an Access Token
Use the `get_token` method to fetch a valid token.

```python
try:
    token_response = auth_instance.get_token()
    print(f"Access Token: {token_response.access_token}")
    print(f"Expires In: {token_response.expires_in} seconds")
except Exception as e:
    print(f"Error: {str(e)}")
```

---

## Error Handling

The `Auth` module raises specific exceptions for various error scenarios:

- **`InvalidClientIDError`**: Raised when the `client_key` is invalid.
- **`InvalidAuthenticationError`**: Raised when the authentication type is not `Basic Auth`.
- **`InvalidAuthorizationHeaderError`**: Raised when the `client_secret` is invalid.
- **`APIError`**: Raised for generic API issues, such as network errors or unexpected responses.

### Example:
```python
try:
    token_response = auth_instance.get_token()
except InvalidClientIDError:
    print("Error: The client key is invalid.")
except InvalidAuthenticationError:
    print("Error: Invalid authentication type. Expected Basic Auth.")
except InvalidAuthorizationHeaderError:
    print("Error: Invalid client secret.")
except APIError as e:
    print(f"API Error: {str(e)}")
```

---

## Testing

The `Auth` module includes unit tests to ensure its functionality. To run the tests:

1. Ensure you have `unittest` installed (it comes with Python by default).
2. Run the tests:

```bash
python3 -m unittest discover tests
```

Tests cover:
- Successful token retrieval.
- Handling of invalid `client_key` or `client_secret`.
- Errors such as invalid authentication type or authorization header.
