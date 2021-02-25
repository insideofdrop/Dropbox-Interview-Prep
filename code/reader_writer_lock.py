"""
Dropbox

Implement a Reader-Writer Lock.

This question is FREQUENTLY asked in ONSITE interviews and is rarely asked in phone screens.

The Java version looks different and you can find it in the packet. 
We first implement a read-preferring lock, then a write-preferring lock.
"""

import threading

class RWLock(object):
    def __init__(self):
        self.writer_lock = threading.Lock()
        self.num_readers_lock = threading.Lock() #Lock for incrementing and decrementing num_readers
        self.num_readers = 0

    def acquire_reader(self):
        with self.num_readers_lock:
            self.num_readers += 1
            if self.num_readers == 1:
                self.writer_lock.acquire()

    def release_reader(self):
        assert self.num_readers > 0
        with self.num_readers_lock:
            self.num_readers -= 1
            if self.num_readers == 0:
                self.writer_lock.release()

    def acquireWriter(self):
        self.writer_lock.acquire()

    def w_release(self):
        self.writer_lock.release()


class WritePreferringRWLock:

    def __init__(self):
        self.num_writers_waiting = 0
        self.is_writing = False
        self.writer_lock = threading.Lock()
        self.writer_condition = threading.Condition(self.wLock())
        self.num_readers_reading = 0

    def acquire_reader(self):
        self.writer_lock.acquire()
        while self.num_writers_waiting > 0 or self.is_writing:
            self.writer_condition.wait()
        self.num_readers_reading += 1
        self.writer_lock.release()
    
    def release_reader(self):
        with self.writer_lock:
            self.numReadersReading -= 1
            if self.num_readers_reading < 0:
                raise Exception("Improper use of lock!")
            if self.num_readers_reading == 0:
                self.writer_condition.notifyAll()

    def acquire_writer(self):
        with self.writer_lock:
            self.num_writers_waiting += 1
            while self.num_readers_reading > 0 or self.is_writing:
                self.writer_condition.wait()
            self.num_writers_waiting -= 1
            self.is_writing = True

    def release_writer(self):
        with self.writer_lock:
            self.is_writing = False
            self.writer_condition.notifyAll()
