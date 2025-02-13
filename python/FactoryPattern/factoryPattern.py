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
        return x+y


class NewMaths:
    new_ratio=1.2
    def __init__(self,name,his):
        self.name=name
        self.his=his
    @classmethod   #can modify attribute but not the instance and they donot take self but cls object
    def classMaths(cls,new_percent):
        cls.new_ratio=new_percent
        return cls.new_ratio

a=MathDo
print(a.sum(12,12))
    