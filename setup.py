import codecs
import glob
import os.path
import re
import sys

from setuptools import setup, find_packages

# We want the value of ``purestemmer.__version__``. However, we cannot
# simply ``import purestemmer`` since purestemmer might have
# dependencies which might not be installed. Hence we extract the
# version information "manually".
module_dir = os.path.dirname(__file__)
init_filename = os.path.join(module_dir, 'purestemmer', '__init__.py')
with codecs.open(init_filename, 'r' ,'utf8') as f:
    for line in f:
        m = re.match(r'\s*__version__\s*=\s*[\'"](.*)[\'"]\s*', line)
        if m:
            version = m.group(1)
            break
    else:
        raise Exception('Could not find version number.')

setup(
    name='purestemmer',
    version=version,
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
