#
import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def yfunc():
    print 2
    yield 1

set_interval(yfunc, 1)
