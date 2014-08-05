#!/usr/bin/env python
# vim:fileencoding=utf8

# Copyright (c) 2014 Florian Brucker
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tests for ``purestemmer``.

Intended to be run via nosetests.
"""


import codecs
import glob
import os.path
import sys

import Stemmer
from nose.plugins.attrib import attr

_module_dir = os.path.abspath(os.path.dirname(__file__))
_root_dir = os.path.abspath(os.path.join(_module_dir, '..'))
_snowball_dir = os.path.join(_root_dir, 'snowball')
sys.path.insert(0, _root_dir)
import purestemmer


def _get_variants(word):
    """
    Return ``str`` and ``unicode`` variants of a word.
    """
    variants = [word]
    if isinstance(word, unicode):
        variants.append(word.encode('utf8'))
    else:
        variants.append(word.decode('utf8'))
    return variants


def compare_stemmers(algorithm, words):
    """
    Make sure pystemmer and purestemmer return the same stems.

    ``algorithm`` is the name of the algorithm to be tested and
    ``words`` is a list of input words.
    """
    py = Stemmer.Stemmer(algorithm)
    pure = purestemmer.Stemmer(algorithm)
    for word in words:
        variants = _get_variants(word)
        for variant in variants:
            py_stem = py.stemWord(variant)
            pure_stem = pure.stemWord(variant)
            assert py_stem == pure_stem, (
                    'Different output for %r: pystemmer returned %r, ' +
                    'purestemmer returned %r.' % (variant, py_stem, pure_stem))
            assert type(py_stem) == type(pure_stem), (
                    'Different output types for %r: pystemmer returned %s, ' +
                    'purestemmer returned %s.' % (variant, type(py_stem),
                    type(pure_stem)))


@attr('slow')
def test_compare_stemmers():
    """
    Make sure that pystemmer and purestemmer return the same stems.
    """
    filenames = sorted(glob.glob(os.path.join(_module_dir, '*.txt')))
    for filename in filenames:
        algorithm = os.path.splitext(os.path.basename(filename))[0]
        with codecs.open(filename, 'r', 'utf8') as f:
            words = f.read().splitlines()
        test = lambda: compare_stemmers(algorithm, words)
        test.description = algorithm
        yield test


def test_aliases():
    """
    Make sure that the aliases work.
    """
    filenames = sorted(glob.glob(os.path.join(_snowball_dir, '*.sbl')))
    for filename in filenames:
        name = os.path.splitext(os.path.basename(filename))[0]
        aliases = name.split('_')
        for alias in aliases:
            purestemmer.Stemmer(alias)

