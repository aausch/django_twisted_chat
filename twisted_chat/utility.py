import logging
import collections

class DummyLock():
    def acquire():
        logging.warning('acquiring a non initialized write lock')

    def release():
	logging.warning('acquiring a non initialized write lock')


class WriteProtectedDict(dict):
    """A dictionary which applies an arbitrary key-altering function before accessing the keys"""
    write_lock = DummyLock()

    def __init__(self, write_lock=None):
        if write_lock:
            self.write_lock = write_lock
        dict.__init__(self)

    def __setitem__(self, key, value):
        write_lock.acquire()
        result = super.__setitem__(self,key,value)
        write_lock.release()
        return result

    def __delitem__(self, key):
        write_lock.acquire()
        super.__delitem__(self,key,value)
        write_lock.release()
