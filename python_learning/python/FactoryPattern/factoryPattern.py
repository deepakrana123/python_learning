translations={"car": "voiture", "bike": "bicyclette",
                             "cycle":"cyclette"}
class FrenchTarnslations:
    def __init__(self):
        self.translations={"car": "voiture", "bike": "bicyclette",
                             "cycle":"cyclette"}
    def localize(self,msg):
        return self.translations.get(msg,msg)
class SpainshTarnslations:
    def __init__(self):
        self.translations={"car": "coche", "bike": "bicicleta",
                             "cycle":"ciclo"}
    def localize(self,msg):
        return self.translations.get(msg,msg)
class EnglishTarnslations:
    def localize(self,msg):
        return msg

class Factory:
    _localizers = {
        "French": FrenchTarnslations,
        "English": EnglishTarnslations,
        "Spanish": SpainshTarnslations,
    }
    @staticmethod   #when you donot need self and cls and it doesnot chnage the cls attribute and instance,act like a normal function
    def getTranslation(language):
        return Factory._localizers.get(language,EnglishTarnslations)()


f=Factory.getTranslation('French')
print(f.localize('car'))



class MathDo:
    @staticmethod
    def sum(x,y):
        return x + y


class NewMaths:
    new_ratio = 1.2
    def __init__(self,name,his):
        self.name=name
        self.his=his
    @classmethod   #can modify attribute but not the instance and they donot take self but cls object
    def classMaths(cls,new_percent):
        cls.new_ratio = new_percent
        return cls.new_ratio

a=MathDo
print(a.sum(12,12))



class EmailNotification:
    def __init__(self):
        pass

    def send(self,msg):
        return 'Email is send to ' + " " + msg

class OtpNotification:
    def __init__(self):
        pass

    def send(self,msg):
        return 'Otp notification' + " " + msg

class SmsNotification:
    def __init__(self):
        pass
    def send(self,msg):
        return 'Otp notification'+ " " + msg
    

class Notificaiton:
    __trans={
            "SMS":SmsNotification,
            "OTP":OtpNotification,
            "EMAIL":EmailNotification
        }
    @staticmethod
    def sendNotifcation(method):
        return Notificaiton.__trans.get(method,EmailNotification)()

a=Notificaiton.sendNotifcation('SMS')
# print(a.send('otp'))
print(a.send('hii how are you'))
class ConsoleLogger:
    def __init__(self):
        pass

    def logs(self,msg):
        return 'console ' + " " + msg

class DataBaseLogger:
    def __init__(self):
        pass

    def logs(self,msg):
        return 'database' + " " + msg

class FileLogger:
    def __init__(self):
        pass
    def logs(self,msg):
        return 'file'+ " " + msg
class ErrorBaseLogger:
    def __init__(self):
        pass
    def logs(self,msg):
        return 'file'+ " " + msg
    

class Logger:
    __logger={
            "console":ConsoleLogger,
            "file":FileLogger,
            "database":DataBaseLogger,
            "error":ErrorBaseLogger
        }
    @staticmethod
    def sendLogs(method,msg):
        a=Logger.__logger.get(method,ConsoleLogger)()
        return a.logs(msg)

logs = Logger
print(logs.sendLogs('console','hi console'))


