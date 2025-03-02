setup.py

from setuptools import find_packages, setup

setup(
    name="quotesapi",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-caching",
        "flask-restful",
        "flask-sqlalchemy",
        "jsonschema",
        "rfc3339-validator",
        "SQLAlchemy",
    ]
)
