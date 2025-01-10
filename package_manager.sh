#!/bin/bash

# Set the package version
PACKAGE_NAME="mpesa_client"
PACKAGE_VERSION="1.0.0"

build_package() {
    echo "Building the package..."
    pip install setuptools wheel || { echo "Failed to install setuptools and wheel"; exit 1; }
    python3 setup.py sdist bdist_wheel || { echo "Package build failed"; exit 1; }
}

test_package() {
    echo "Testing the package locally..."
    pip install dist/${PACKAGE_NAME}-${PACKAGE_VERSION}-py3-none-any.whl || { echo "Local test installation failed"; exit 1; }
}

upload_to_testpypi() {
    echo "Uploading the package to TestPyPI..."
    pip install twine || { echo "Failed to install twine"; exit 1; }
    twine upload --repository-url https://test.pypi.org/legacy/ dist/* || { echo "Upload to TestPyPI failed"; exit 1; }
}

upload_to_pypi() {
    echo "Uploading the package to PyPI..."
    pip install twine || { echo "Failed to install twine"; exit 1; }
    twine upload dist/* || { echo "Upload to PyPI failed"; exit 1; }
}

# Main menu
echo "Choose an option:"
echo "1. Build and Test Locally"
echo "2. Upload to TestPyPI"
echo "3. Upload to PyPI"
echo "4. Exit"

read -p "Enter your choice (1/2/3/4): " choice

case $choice in
    1)
        build_package
        test_package
        ;;
    2)
        upload_to_testpypi
        ;;
    3)
        upload_to_pypi
        ;;
    4)
        echo "Exiting..."
        ;;
    *)
        echo "Invalid choice. Exiting..."
        ;;
esac
