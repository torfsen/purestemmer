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
Script to benchmark pystemmer and purestemmer.
"""

import codecs
import glob
import os.path
import timeit

import Stemmer

import purestemmer

def mean(numbers):
    return sum(numbers) / float(len(numbers))


def benchmark(stemmer, words, repeat=1):
    """
    Measure how long a stemmer takes to stem a list of words.

    Returns the time in seconds.
    """
    timings = []
    for x in range(repeat):
        start = timeit.default_timer()
        stemmer.stemWords(words)
        stop = timeit.default_timer()
        timings.append(stop - start)
    return mean(timings)


def compare(algorithm, words, repeat=1):
    """
    Compare the pystemmer and purestemmer variants of an algorithm.

    ``algorithm`` is the name of the algorithm and ``words`` is a list
    of input words to be stemmed.

    Returns the elapsed times of the variants.
    """
    py_algo = Stemmer.Stemmer(algorithm)
    py_time = benchmark(py_algo, words, repeat)
    pure_algo = purestemmer.Stemmer(algorithm)
    pure_time = benchmark(pure_algo, words, repeat)
    return (py_time, pure_time)


if __name__ == '__main__':
    module_dir = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.join(module_dir, 'test')
    filenames = sorted(glob.glob(os.path.join(test_dir, '*.txt')))
    py_times = []
    pure_times = []
    delim = '+-----------------+-------------+-------------+--------+'
    line_format = '| %-15s | %11.2f | %11.2f | %6.2f |'

    print delim
    print '| Algorithm       | pystemmer   | purestemmer | Factor |'
    print '+=================+=============+=============+========+'
    for filename in filenames:
        algorithm = os.path.splitext(os.path.basename(filename))[0]
        with codecs.open(filename, 'r', 'utf8') as f:
            words = f.read().splitlines()
        py_time, pure_time = compare(algorithm, words)
        py_times.append(py_time)
        pure_times.append(pure_time)
        factor = pure_time / float(py_time)
        print line_format % (algorithm, py_time, pure_time, factor)
        print delim
    py_total = sum(py_times)
    pure_total = sum(pure_times)
    total_factor = pure_total / float(py_total)
    print line_format % ('TOTAL', py_total, pure_total, total_factor)
    print delim
