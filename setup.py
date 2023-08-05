from setuptools import setup, find_packages

setup(
    name="missing_data_generator",
    version="0.1.0",
    install_requires=[
        "faker",
        "pandas",
        "pydantic",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
    packages=find_packages(
        include=["missing_data_generator", "missing_data_generator.*"]
    ),
)
