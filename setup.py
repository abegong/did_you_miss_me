from setuptools import setup, find_packages

setup(
    name="did_you_miss_me",
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
        include=["did_you_miss_me", "did_you_miss_me.*"]
    ),
)
