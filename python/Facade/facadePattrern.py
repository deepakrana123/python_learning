# when you do thinks one by one to compelete a single task by different
class Dvd:
    def play_movie(self,movie):
        return f'dvd sound on {movie}'
class Sound:
    def play_sound(self):
        return 'sound on'

class TV:
    def play_tv(self):
        return 'tv played'
    

class Facade:
    def __init__(self):
        self.dvd=Dvd
        self.sound=Sound
        self.Tv=TV
    def watch_movie(self,movie):
        self.tv.play_tv()
        self.sound.play_sound(50)
        self.dvd.play_movie(movie)

class Engine:
    def start_engine(self):
        return 'engine is started'
class TotalFueld:
    def count_fuel(self,fuel):
        return f'fuel is about to end {fuel} '
class InginationOn:
    def inigantion(self):
        return 'inigation is done'

class StartEngine:
    def __init__(self):
        self.engine=Engine
        self.fuel=TotalFueld
        self.inigantion=InginationOn
    def watch_movie(self):
        self.engine.start_engine()
        self.inigantion.inigantion()
        self.fuel.count_fuel(50)
