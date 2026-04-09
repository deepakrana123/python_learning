class Command:
    def execute(self):
        pass
    def undo(self):
        pass

class MusicPlayer:
    def play(self):
        print("🎵 Music is PLAYING")
    def stop(self):
        print("🎵 Music is Off")

class Light:
    def turn_on(self):
        print("🎵 Light is on")
    def turn_off(self):
        print("🎵 Light is Off")

class Ac:
    def turn_on(self):
        print("🎵 Ac is on")
    def turn_off(self):
        print("🎵 Ac is Off")

class LightCommand(Command):
    def __init__(self,light):
        self.light=light
    def execute(self):
        return self.light.turn_on()
    def undo(self):
        return self.light.turn_off()

class AcCommand(Command):
    def __init__(self,light):
        self.light=light
    def execute(self):
        return self.light.turn_on()
    def undo(self):
        return self.light.turn_off()

class MusicPlayerCommand(Command):
    def __init__(self,light):
        self.light=light
    def execute(self):
        return self.light.play()
    def undo(self):
        return self.light.stop()


class RemoteControl:
    def __init__(self):
        self.history = []
    def press_button(self,command):
        command.execute()
        self.history.append(command)
    def press_back(self):
        if self.history:
            a=self.history.pop()
            a.undo()
        else:
            print("first action")

class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light
    def execute(self):
        self.light.turn_off()
    def undo(self):
        self.light.turn_on()
class SmartHomeThreater:
    def __init__(self):
        self.light_turn_on=LightCommand(Light)
        self.light_turn_off=LightOffCommand(Light)
        self.ac=AcCommand(Ac)
        self.music=MusicPlayerCommand()
        self.remote=RemoteControl(MusicPlayer)
    def remote_on(self):
        self.remote.press_button(self.light_turn_off)
        self.remote.press_button(self.ac)
        self.remote.press_button(self.music)
    def remote_off(self):
        self.remote.press_back(self.light_turn_on)
        self.remote.press_back(self.ac)
        self.remote.press_back(self.music)