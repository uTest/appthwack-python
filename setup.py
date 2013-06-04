__author__ = 'Andrew Hawker <andrew@appthwack.com>'

import thwacky

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=thwacky.__name__,
    version=thwacky.__version__,
    description='Python client for AppThwack REST API.',
    long_description=open('README.md').read(),
    author='Andrew Hawker',
    author_email='andrew@appthwack.com',
    url='https://github.com/ahawker/thwacky',
    license=open('LICENSE.md').read(),
    package_dir={'thwacky': 'thwacky'},
    packages=['thwacky'],
    test_suite='tests',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    )
)
