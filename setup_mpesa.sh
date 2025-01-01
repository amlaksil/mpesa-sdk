#!/bin/bash

mkdir -p mpesa_sdk/auth mpesa_sdk/payments mpesa_sdk/utils tests

# Create the __init__.py files in relevant directories
for dir in mpesa_sdk mpesa_sdk/auth mpesa_sdk/payments mpesa_sdk/utils tests; do
	touch "$dir/__init__.py"
done

mkdir -p .github/workflows
