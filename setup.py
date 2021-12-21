from setuptools import setup

requirements = []
"""
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
"""

readme = ""
with open('README.md', 'r') as f:
    readme = f.read()

packages = [
    "ugecko",
    "ugecko.enums",
    "ugecko.utils",
]

setup(
    name = "ugecko",
    author = "WiiuDev, VCoding",
    url = "https://github.com/vincent-coding/uGecko",
    project_urls = {
        "Source Code": "https://github.com/vincent-coding/uGecko",
        "Documentation": "https://github.com/vincent-coding/uGecko/tree/master/docs",
        "Issue Tracker": "https://github.com/vincent-coding/uGecko/issues"
    },
    version = "1.3.1",
    packages = packages,
    license = "MIT",
    description = "Python library for use with TCPGecko. Requires kernel exploit to use.",
    long_description = readme,
    long_description_content_type = "text/markdown",
    install_requires = requirements,
    python_requires = ">=3.8.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
