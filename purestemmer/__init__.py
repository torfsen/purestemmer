#!/usr/bin/env python
# vim:fileencoding=utf8

# Copyright (c) 2014 Florian Brucker, portions Copyright (c) 2006,
# Richard Boulton.
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
Pure-Python implementation of the Snowball stemming algorithms.

In most cases you are better off using the ``pystemmer`` module, which
provides a Python wrapper around the C implementation of the Snowball
stemmers. The ``purestemmer`` module is only for those situations where
you cannot use a C extension.
"""

# Note: Names violating PEP8 are taken from pystemmer and kept for
# compatibility.


import collections
import glob
import importlib
import os.path


__all__ = ['algorithms', 'Stemmer']
__version__ = '0.1.0'
__docformat__ = 'restructuredtext en'


def _load_algorithms():
    """
    Load all algorithm modules.

    Returns a dictionary that maps algorithm names to stemmer modules
    and a dictionary that maps aliases to algorithm names.
    """
    module_dir = os.path.abspath(os.path.dirname(__file__))
    algorithms_dir = os.path.join(module_dir, 'algorithms')
    filenames = glob.glob(os.path.join(algorithms_dir, '*.py*'))
    names = set(os.path.splitext(os.path.basename(f))[0] for f in filenames)
    algorithms = {}
    aliases = {}
    for name in names:
        if name.startswith('__'):
            continue
        parts = name.split('_')
        module_name = 'purestemmer.algorithms.' + name
        algorithms[unicode(parts[0])] = importlib.import_module(module_name)
        for part in parts[1:]:
            aliases[unicode(part)] = parts[0]
    return algorithms, aliases

_algorithms, _aliases = _load_algorithms()


class _Cache(collections.MutableMapping):
    """
    Cache with limited size.

    This cache works like a normal dict, but keeps only a limited number of
    entries. If the limit is reached then a fraction of the oldest entries
    is discarded. This purging is done automatically if necessary whenever
    an entry is stored.
    """

    def __init__(self, max_size=10000, keep_ratio=0.75):
        """
        Constructor.

        ``max_size`` is the maximum number of entries. Can also be set via the
        property of the same name.

        ``keep_ratio`` is the ratio of items that is kept when old items are
        purged. For example, if ``max_size = 100`` and ``keep_ratio = 0.25``
        then the 25 newest entries are kept when the cache is purged. Can also
        be set via the property of the same name.
        """
        self._cache = {}
        self._counter = 0
        self._max_size = max_size
        self.keep_ratio = keep_ratio

    def __getitem__(self, key):
        entry = self._cache[key]
        entry[1] = self._counter
        self._counter += 1
        return entry[0]

    def __setitem__(self, key, value):
        self._cache[key] = [value, self._counter]
        self._counter += 1
        self._purge()

    def __delitem__(self, key):
        del self._cache[key]

    def __iter__(self):
        return iter(self._cache)

    def __len__(self):
        return len(self._cache)

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, value):
        self._max_size = value
        if self._max_size == 0:
            self._cache = {}
            self._counter = 0
        else:
            self._purge()

    def _purge(self):
        """
        Make sure that the cache size is below its limit.

        If the cache is larger than the limit then old items are purged. Only
        the ``keep_ratio * max_size`` latest entries are kept.
        """
        if len(self._cache) <= self._max_size:
            return
        new_cache = {}
        limit = self._counter - self.keep_ratio * self._max_size
        for key, value in self._cache.iteritems():
            if value[1] > limit:
                new_cache[key] = value
        self._cache = new_cache


def version():
    """
    Get the version string of the stemming module.

    This version number is for the stemmer module as a whole (not for an
    individual stemming algorithm).

    Note: This function returns the ``pystemmer`` version to which this
    module is compatible. Use ``purestemmer.__version__`` to get the
    actual purestemmer module version.
    """
    return '1.3.0'


def algorithms(aliases=False):
    """
    Get a list of the names of the available stemming algorithms.
    Note that there are also aliases for these algorithm names, which are not
    included in this list by default. If the 'aliases' keyword parameter is
    False, this list is guaranteed to contain precisely one entry for each
    available stemming algorithm. Otherwise, all known aliases for algorithms
    will be included in the list.

    Note that the the classic Porter stemming algorithm for English is
    available by default: although this has been superceded by an improved
    algorithm, the original algorithm may be of interest to information
    retrieval researchers wishing to reproduce results of earlier
    experiments. Most users will want to use the "english" algorithm,
    instead of the "porter" algorithm.
    """
    # Note: It seems that the ``aliases`` keyword has no effect in
    # pystemmer 1.3.0.
    return sorted(_algorithms.keys())


class Stemmer(object):
    """
    An instance of a stemming algorithm.

    When creating a ``Stemmer`` object, there is one required argument: the
    name of the algorithm to use in the new stemmer. A list of the valid
    algorithm names may be obtained by calling the ``algorithms`` function
    in this module. In addition, the appropriate stemming algorithm for a
    given language may be obtained by using the 2 or 3 letter ISO 639
    language codes.

    A second optional argument to the constructor for ``Stemmer`` is the size
    of cache to use. The cache implemented in this module is not terribly
    efficient, but benchmarks show that it approximately doubles
    performance for typical text processing operations, without too much
    memory overhead. The cache may be disabled by passing a size of 0.
    The default size (10000 words) is probably appropriate in most
    situations. In pathological cases (for example, when no word is
    presented to the stemming algorithm more than once, so the cache is
    useless), the cache can severely damage performance.
    """

    def __init__(self, algorithm, maxCacheSize=10000):
        """
        Initialise a stemmer.

        See the class documentation for details.
        """
        try:
            self._module = _algorithms[algorithm]
        except KeyError:
            # Maybe an alias?
            try:
                self._module = _algorithms[_aliases[algorithm]]
            except KeyError:
                # Would prefer ``ValueError``, but pystemmer uses ``KeyError``.
                raise KeyError("Stemming algorithm '%s' not found" % algorithm)
        self._cache = _Cache(maxCacheSize)

    @property
    def maxCacheSize(self):
        return self._cache.max_size

    @maxCacheSize.setter
    def maxCacheSize(self, value):
        self._cache.max_size = value

    def stemWord(self, word):
        """
        Stem a single word.

        ``word`` must be either a ``str`` or ``unicode`` instance. The return
        value has the same type as the input. Please note that all strings are
        converted to Unicode internally for processing. It is assumed that
        they are encoded via UTF8.
        """
        if isinstance(word, unicode):
            was_unicode = True
        else:
            word = word.decode('utf8')
            was_unicode = False
        try:
            stem = self._cache[word]
        except KeyError:
            stem = self._module.stem(word)
            self._cache[word] = stem
        if not was_unicode:
            stem = stem.encode('utf8')
        return stem

    def stemWords(self, words):
        """
        Stem a list of words.

        ``words`` must be an iterable containing ``str`` and/or ``unicode``
        instances. Please note that ``str`` instances are internally converted
        to Unicode. It is assumed that they are encoded via UTF8.

        The return value is a list of the word stems.
        """
        return [self.stemWord(w) for w in words]
