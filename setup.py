import glob
import os.path
import sys

from setuptools import setup, find_packages

setup(
    name='purestemmer',
    version='0.1.0',
    description='Pure-Python implementations of the Snowball stemmers',
    url='https://github.com/torfuspolymorphus/purestemmer',
    author='Florian Brucker',
    author_email='mail@florianbrucker.de',
    license=['MIT', 'BSD'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Danish',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: Finnish',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Italian',
        'Natural Language :: Norwegian',
        'Natural Language :: Portuguese',
        'Natural Language :: Russian',
        'Natural Language :: Spanish',
        'Natural Language :: Swedish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords=[
        'python',
        'information retrieval',
        'language processing',
        'morphological analysis',
        'stemming algorithms',
        'stemmers',
    ],
    packages=find_packages(exclude='test'),
    platforms=['any'],
)
