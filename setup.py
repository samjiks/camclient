

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
      'name' : 'CameraClient',
      'version': '1.0',
      'description': 'Camera Client setup',
      'author': 'Samuel Thampy',
      'author_email': 'samjiks@hotmail.com',
      'install_requires': ['urllib3', 'pyyaml', 'boto'],
     }

setup(**config)

