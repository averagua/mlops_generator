from setuptools import find_packages, setup

setup(
    name='{{ package_name }}',
    packages=find_packages(),
    version='{{ version }}',
    description='{{ description }}',
    license='{% if license_type == 'MIT' %}MIT{% elif license_type == 'BSD-3-Clause' %}BSD-3{% endif %}',
)