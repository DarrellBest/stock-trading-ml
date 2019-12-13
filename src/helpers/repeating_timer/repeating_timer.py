
from threading import Thread, Event, RLock
from time import sleep


class RepeatingTimer(Thread):
    """Call a function and repeate after a specified number of seconds:

            t = Timer(30.0, f, args=None, kwargs=None)
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, args=None, kwargs=None):
        Thread.__init__(self, daemon=True)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()
        self.__lock = RLock()

    def cancel(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def run(self):
        with self.__lock:
            while not self.finished.is_set():
                sleep(self.interval)
                self.function(*self.args, **self.kwargs)
            self.finished.set()
