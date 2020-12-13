from setuptools import find_packages, setup
import io
from re import search
test_requirements = ["pytest>=3", ]

with io.open("src/{{project_name}}/__init__.py", "rt", encoding="utf8") as f:
    version = search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="{{ project_name }}",
    packages=find_packages("src"),
    version=version,
    description="{{ description }}",
    license="{{license_type}}",
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "{{ project_name }}={{ project_name }}.cli:main",
        ]
    },
    python_requires=">2.7, !=3.4.*",
    zip_safe=False,
)
