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
Script to convert the Snowball stemmers to Python modules.
"""

import codecs
import glob
import os.path

import sbl2py

_module_dir = os.path.abspath(os.path.dirname(__file__))
_snowball_dir = os.path.join(_module_dir, 'snowball')
_algorithms_dir = os.path.join(_module_dir, 'purestemmer', 'algorithms')


def make_algorithm(filename):
    """
    Create Python algorithm module from Snowball source file.
    """
    base = os.path.splitext(os.path.basename(filename))[0]
    module_filename = os.path.join(_algorithms_dir, base + '.py')
    with codecs.open(filename, 'r', 'utf8') as f:
        with codecs.open(module_filename, 'w', 'utf8') as g:
            g.write(sbl2py.translate_file(f))

def find_snowball_sources():
    """
    Find Snowball source files.
    """
    return sorted(glob.glob(os.path.join(_snowball_dir, '*.sbl')))


def main():
    """
    Create Python algorith modules for all Snowball source files.
    """
    for filename in find_snowball_sources():
        print filename
        make_algorithm(filename)


if __name__ == '__main__':
    main()
