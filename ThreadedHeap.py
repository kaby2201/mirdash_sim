from threading import Semaphore
from heapq import heappop, heappush


class ThreadedHeap:
    def __init__(self):
        self.values = []
        self.semaphore = Semaphore(value=0)
        self.mutex = Semaphore(value=1)

    def heappop(self):
        self.semaphore.acquire()
        self.mutex.acquire()
        result = heappop(self.values)
        self.mutex.release()
        return result

    def heappush(self, val):
        self.mutex.acquire()
        heappush(self.values, val)
        self.semaphore.release()
        self.mutex.release()
