__author__ = 'Andrew Hawker <andrew@appthwack.com>'

import appthwack

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=appthwack.__name__,
    version=appthwack.__version__,
    description='AppThwack python client',
    long_description=open('README.md').read(),
    author='Andrew Hawker',
    author_email='andrew@appthwack.com',
    url='https://github.com/appthwack/appthwack-python',
    license=open('LICENSE.md').read(),
    package_dir={'appthwack': 'appthwack'},
    packages=['appthwack'],
    test_suite='tests',
    install_requires=['requests'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    )
)
