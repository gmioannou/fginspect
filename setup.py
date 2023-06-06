try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'fginspect'
VERSION = __import__(PACKAGE).__version__

config = {
    'description': 'Inspect ESRI File Geodatabase',
    'author': 'George Ioannou',
    'url': 'http://github.com/gmioannou/fginspect',
    'download_url': 'http://github.com/gmioannou/fginspect',
    'author_email': 'gmioannou@gmail.com',
    'version': VERSION,
    'install_requires': [
        'ConfigParser>=3.5.0',
        'pyyaml>=3.12'
    ],
    'packages': ['fginspect'],
    'scripts': [],
    'name': 'fginspect',
    'entry_points': {
            'console_scripts': [
                'fginspect = fginspect.fginspect:main'
            ]
    },
}

setup(**config)
