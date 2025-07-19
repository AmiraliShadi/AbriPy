# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="abripy",
    version="0.1.0",
    author="AbriPy Framework Team",
    author_email="ashadi8448@gmail.com",
    description="A modern, secure Python web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmiraliShadi/abripy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "uvicorn[standard]>=0.24.0",
        "aiosqlite>=0.19.0",
        "PyJWT>=2.8.0",
        "click>=8.1.0",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "abripy=cli.commands:cli",
        ],
    },
)
