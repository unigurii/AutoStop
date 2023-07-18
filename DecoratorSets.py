import time
import threading
from functools import wraps

class Timer:

    def __init__(self,func):
        self.func = func


    def __call__(self, *args, **kwargs):

        start_time = time.time()
        result = self.func(*args,**kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"函数 {self.func.__name__} 执行时间：{execution_time} 秒")
        return result

class Fer:

    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        if not int(execution_time):
            print(f"函数 {self.func.__name__} 执行频率：{1e5} 帧")
            return result
        else:
            print(f"函数 {self.func.__name__} 执行频率：{1 / execution_time} 帧")
            return result

class Logger:

    def __init__(self, func):
        self.func = func
        self.stop_event = threading.Event()
    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        with open('log.txt', 'a') as file:
            file.write(f"函数 {self.func.__name__} 被调用\n")
            file.write(f"参数: {args}, {kwargs}\n")
            file.write(f"结果: {result}\n")
        return result

class LoggerPrinter:

    def __init__(self, func):
        self.func = func
        self.stop_event = threading.Event()
    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        print('-----------------******--------------------')
        print(f"函数 {self.func.__name__} 被调用\n")
        print(f"参数: {args}, {kwargs}\n")
        print(f"结果: {result}\n")
        print('-----------------******--------------------')
        return result


class Eventer:
    def __init__(self,func):
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        while not self.stop_event.is_set():
            try:
                self.func(*args, **kwargs)
            except Exception as e:
                print(f"异常: {e}")
                self.stop_event.set()
                break  # break the loop if an exception occurs
            return result
