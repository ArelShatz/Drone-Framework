from collections import deque
from time import sleep, perf_counter
from helpers import insort_left_key

class EventLoop():
    def __init__(self):
        self.Running = True
        self.taskQueue = deque()
        self.sleepQueue = deque()
        self.bgCallbacks = {}
        self.returnValue = None


    def run(self, init_func):
        next(init_func)
        self.add_task(init_func)

        while self.Running:

            """if self.callbacks:
                for event in self.callbacks:
                    if event[0]():
                        event[1]()"""

            if self.taskQueue:
                task = self.taskQueue.popleft()
                coroutine = task[0]
                interval = task[1]
                try:
                    self.returnValue = next(coroutine)
                    self.add_task(coroutine, timeout=interval, interval=interval)

                except StopIteration:
                    pass

            if self.sleepQueue:
                task = self.sleepQueue[0]
                coroutine = task[0]
                delay = task[1]
                interval = task[2]

                if perf_counter() >= delay:
                    self.sleepQueue.popleft()
                    self.add_task(coroutine, interval=interval)

            else:
                sleep(0.001)


    def add_task(self, task, timeout=0, interval=0):
        if timeout == 0:
            self.taskQueue.append((task, interval))

        else:
            timeToExec = perf_counter() + timeout
            insort_left_key(self.sleepQueue, (task, timeToExec, interval), key=lambda x: x[1])


    def add_callback(self, event, callback):
        if not isinstance(event, Event):
            return

        self.bgCallbacks[id(event)] = callback


    def emit(self, event, *args):
        if not isinstance(event, Event):
            return

        try:
            coroutine = self.bgCallbacks[id(event)]
            coroutine(args)

        except KeyError:
            pass


    def stop(self):
        self.add_task(lambda: self.__stop())


    def __stop(self):
        self.Running = False
