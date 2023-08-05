from setuptools import setup, find_packages

setup(
    name="missingness_data_generator",
    version="0.1.0",
    install_requires=[
        "faker",
        "pandas",
        "pydantic",
    ],
    extras_require={
        "dev": ["pytest", "black", "ruff", "tabulate"],
        "ai": ["langchain"],
    },
    packages=find_packages(
        include=["missingness_data_generator", "missingness_data_generator.*"]
    ),
)
