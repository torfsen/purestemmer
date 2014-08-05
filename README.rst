*purestemmer* - A pure-Python implementation of the Snowball stemmers
#####################################################################
The traditional way of using the `Snowball stemmers`_ in Python is via
the pystemmer_ package, which provides a Python wrapper around the
Snowball C library. However, Python C extensions are problematic in
some environments. Therefore, this package provides pure-Python
implementations of the Snowball stemming algorithms.

The implementations of the stemming algorithms is translated from the
Snowball language to Python via sbl2py_.

.. _`Snowball stemmers`: http://snowball.tartarus.org/
.. _pystemmer: https://pypi.python.org/pypi/PyStemmer
.. _sbl2py: https://pypi.python.org/pypi/sbl2py


Usage
=====
Usually, you'll prefer to use the *pystemmer* module whenever that is
possible, because it's much faster than *purestemmer*::

    try:
        import Stemmer
    except ImportError:
        # pystemmer is not available, use purestemmer instead
        import purestemmer as Stemmer

Since *purestemmer* has the same public API and provides the same
algorithms as *pystemmer*, there should be no need to change any code
when switching between *pystemmer* and *purestemmer* like this.

Please see the *pystemmer* documentation for details on how to use the
stemming algorithms.


Differences between *purestemmer* and *pystemmer*
=================================================
* *purestemmer* has only been tested on Python 2.7
* ``purestemmer.Stemmer`` instances are thread-safe
* *purestemmer* is on average about 100x slower than *pystemmer*


License
=======
*pystemmer* itself is covered by the `MIT License`_. The underlying
Snowball algorithms are covered by the `BSD-3 License`_. Please see the
``LICENSE`` file for details.

.. _`MIT License`: http://opensource.org/licenses/MIT
.. _`BSD-3 License`: http://opensource.org/licenses/BSD-3-Clause
