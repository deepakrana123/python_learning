class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance



import threading

class SingleTonWithThreading:
    _instance=None
    _threading=threading.Lock()
#  __new__ initialize before __init__
    def __new__(cls):
        with cls._threading:
            if not cls._instance:
                cls._instance = super(SingleTonWithThreading, cls).__new__(cls)
            return cls._instance


class SingleTon:
    