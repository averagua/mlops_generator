#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["click>=7.0", "marshmallow==3.9.1", "jinja2==2.11"]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Alejandro Veragua Albornoz",
    author_email="veragua.alb@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="CLI for MLOps code generator",
    entry_points={
        "console_scripts": [
            "mlops_generator=mlops_generator.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="mlops_generator",
    name="mlops_generator",
    packages=find_packages(include=["mlops_generator", "mlops_generator.*"]),
    setup_requires=setup_requirements,
    package_data={"templates": ["*/*.py"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/averagua/mlops_generator",
    version="1.0.1",
    zip_safe=False,
)
