#!/usr/bin/env python

"""
Helper class meant to ease the creation of singletons. This
should be used as a decorator -- not a metaclass -- to the class
that should be a singleton.

The decorated class should define only one `__init__` function
that takes only the `self` argument. Other than that, there are
no restrictions that apply to the decorated class.

To get the singleton instance, use the `Instance` method. Trying
to use `__call__` will result in a `SingletonError` being raised.

"""


import threading


class Singleton:
    _singletons = dict()

    def __init__(self, decorated):
        self._lock = threading.Lock()
        self._decorated = decorated

    def instance(self, *args, **kwargs):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        key = self._decorated.__name__
        with self._lock:
            try:
                return Singleton._singletons[key]
            except KeyError:
                Singleton._singletons[key] = self._decorated(*args, **kwargs)
                return Singleton._singletons[key]

    def __call__(self):
        """
        Call method that raises an exception in order to prevent creation
        of multiple instances of the singleton. The `Instance` method should
        be used instead.

        """
        raise SingletonError(
            'Singletons must be accessed through the `Instance` method.')


class SingletonError(Exception):
    pass
