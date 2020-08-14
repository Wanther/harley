import os, multiprocessing
from concurrent import futures

class Executor(object):

    def __init__(self, pool_size=os.cpu_count() or 1):
        self.pool_size = pool_size

    def submit(self, func, args):
        pass

    def __enter__(self):
        print('enter')
        return self
    
    def __exit__(self, type, value, trace):
        print('exit')


class Task(object):
    def __init__(self, task):
        self.task = task
    
    def result(self):
        pass

    def done(self):
        pass

    def cancel(self):
        pass

class ProcessTask(Task):
    def result(self):
        return self.task.get()
    
    def done(self):
        return self.task.ready()
    
    def cancel(self):
        raise Exception('method not implemented')

class ThreadTask(Task):
    def result(self):
        return self.task.result()
    
    def done(self):
        return self.task.done()
    
    def cancel(self):
        return self.task.cancel()


class ProcessPoolExecutor(Executor):

    def submit(self, func, args):
        return ProcessTask(self.pool.apply_async(func, args))

    def __enter__(self):
        self.pool = multiprocessing.Pool(self.pool_size)
        return self

    def __exit__(self, type, value, trace):
        if self.pool:
            self.pool.close()


class ThreadPoolExecutor(Executor):

    def submit(self, func, args):
        return ThreadTask(self.pool.submit(func, args))

    def __enter__(self):
        self.pool = futures.ThreadPoolExecutor(self.pool_size)
        return self
    
    def __exit__(self, type, value, trace):
        self.pool.shutdown()


class TxtCycleFileParser:
    def parse_each_cycle(self, sample_file):
        with open(sample_file, 'rb') as f:
            cycle_lines = list()
            for line in f:
                if line.startswith(b'Cycle'):
                    if cycle_lines:
                        yield cycle_lines
                        cycle_lines = list()
                    cycle_lines.append(line)
                elif cycle_lines:
                    cycle_lines.append(line)
            if cycle_lines:
                yield cycle_lines