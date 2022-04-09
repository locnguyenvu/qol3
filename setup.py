from setuptools import setup, find_packages

setup(
    name="qol3",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "alembic",
        "aiohttp",
        "beautifulsoup4",
        "Flask",
        "Flask-SQLAlchemy",
        "python-telegram-bot",
        "python-dotenv",
        "psycopg2-binary",
        "pyppeteer",
        "requests",
        "rich",
    ]
)
