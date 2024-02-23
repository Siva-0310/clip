from setuptools import setup

setup(
    name='clip',
    version='1.0.0',
    py_modules=['clip'],
    entry_points={
        'console_scripts': [
            'clip = clip:main'
        ]
    }
)