"""PyProteum Setup
Based on setuptools sample

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyproteum',
    version='1.0.0-alpha',

    description='ProteumIM 2.0 Adapter for Python Programming Language',
    long_description=long_description,

    url='https://github.com/glandre/pyproteum',

    author='Geraldo B. Landre',
    author_email='geraldo.landre@gmail.com',

    license='GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: GPL License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='mutation testing ProteumIM',
    packages=find_packages(['pycparser']),
)
