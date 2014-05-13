"""
    appthwack
    ~~~~~~~~~

    The official AppThwack python client.
"""
__name__ = 'appthwack'
__author__ = 'Andrew Hawker <andrew@appthwack.com>'
__version__ = '1.0.0'

try:
    from appthwack import AppThwackApi, AppThwackApiError
except ImportError:
    # this can occur before package is installed as requets dependency is not
    # yet resolved -- setup.py could never install the package because of this
    pass
