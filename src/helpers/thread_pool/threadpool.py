__author__ = "Darrell Best"
__copyright__ = "Copyright 2018, MTEQ"
__credits__ = ["Darrell Best, John Burton, Thomas Moulton"]
__version__ = "1.0.0"
__maintainer__ = "Behrad Behmardi"
__email__ = "bbehmardi@mteq.com"
__status__ = "Development"


from threading import Semaphore, Lock
from helpers import PyLog


class ThreadPool:

    def __init__(self, size=10):
        self.__active = []
        self.__lock = Lock()
        self.__semaphore = Semaphore(size)
        self.__log = PyLog.Instance().log  # @UndefinedVariable
        self.__dark_grey = '\033[1;37m'

    @property
    def log(self):
        return self.__log

    @property
    def signal(self):
        return self.__semaphore

    def make_active(self, name):
        with self.__lock:
            self.__active.append(name)

    def make_inactive(self, name):
        with self.__lock:
            self.__active.remove(name)

    def threads_utilized(self):
        return str(len(self.__active))
