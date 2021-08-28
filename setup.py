import re
from setuptools import setup, find_packages

setup(
    name='Mopidy-Nuvo',
    version="0.2.0",
    url='https://github.com/legusx/mopidy-nuvo',
    license='Apache License, Version 2.0',
    author='Logan Henrie',
    author_email='legusx@legusx.dev',
    description='Mopidy extension for using Nuvo control pads as a Mopidy frontend.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.14',
        'Pykka >= 1.1',
        'pyserial'
    ],
    entry_points={
        'mopidy.ext': [
            'Mopidy-Nuvo = mopidy_nuvo:Extension',
        ],
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)