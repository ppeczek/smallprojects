try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Lexicon',
    'author': 'Szymon',
    'url': '...',
    'download_url': '...',
    'author_email': 'adamiak.szymon@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'Lexicon'
}

setup(**config)