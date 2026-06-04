from setuptools import setup, find_packages

setup(
    name="sauron-monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Sauron Team",
    description="SDK for monitoring AI training with Sauron",
    python_requires=">=3.7",
)
