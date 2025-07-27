"""
Setup script for FitTrackAI
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fittrackai",
    version="1.0.0",
    author="FitTrackAI Team",
    author_email="contact@fittrackai.com",
    description="AI-Powered Health Data Chat & Analysis Platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/FitTrackAI",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/FitTrackAI/issues",
        "Documentation": "https://github.com/yourusername/FitTrackAI#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Database :: Database Engines/Servers",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fittrackai=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.css", "*.js", "*.json"],
    },
    keywords=[
        "health",
        "fitness",
        "data-analysis",
        "ai",
        "chat",
        "visualization",
        "apple-health",
        "flask",
        "plotly",
        "machine-learning",
    ],
) 