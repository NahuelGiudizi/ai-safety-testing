"""Setup configuration for AI Safety Testing framework"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ai-safety-tester",
    version="1.0.6",
    author="Nahuel Giudizi",
    author_email="your.email@example.com",
    description="LLM security testing framework with severity scoring and multi-model benchmarking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NahuelGiudizi/ai-safety-testing",
    project_urls={
        "Bug Tracker": "https://github.com/NahuelGiudizi/ai-safety-testing/issues",
        "Documentation": "https://github.com/NahuelGiudizi/ai-safety-testing/blob/master/docs/EXAMPLES.md",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.11",
    install_requires=[
        "ollama",
        "pytest>=8.0.0",
        "pytest-cov>=4.1.0",
    ],
    extras_require={
        "dev": [
            "ruff>=0.1.0",
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-safety-test=scripts.run_tests:main",
        ],
    },
)
