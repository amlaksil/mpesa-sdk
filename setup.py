from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="mpesa_client",
    version="1.0.0",
    author="Silamlak Desye",
    author_email="lamlak.lamlak19@gmail.com",
    description="A Python SDK for seamless integration with the M-Pesa API, supporting STK Push payments, C2B, B2C payouts, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amlaksil/mpesa-sdk",
    packages=find_packages(),
    keywords="mpesa sdk M‑PESA API Safaricom integration python payments library mobile money STK Push C2B B2C financial transactions developer tools",
    install_requires=[
        "pydantic>=2.10.0,<3.0.0",
        "requests>=2.31.0,<3.0.0",
        "python-dotenv>=1.0.1,<2.0.0",
        "requests-oauthlib>=2.0.0,<3.0.0",
        "requests-toolbelt>=1.0.0,<2.0.0"
        ],
    extras_require={
        "dev": [
            "build",
            "pycodestyle==2.11.1",
            "requests-unixsocket==0.2.0",
            "typing-extensions==4.12.2"
            ]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
