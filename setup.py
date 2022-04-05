from setuptools import setup, find_packages

requires = [
    'sphinx',
]

setup(
    name='sphinx4md',
    version='0.1',
    license='Free',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sphinx4md = sphinx4md.sphinx4md:main',
        ],
    },
)