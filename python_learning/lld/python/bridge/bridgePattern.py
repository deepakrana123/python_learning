class Device:
    def turn_on(self):
        return f'device turn on'
    def turn_of(self):
        return 'the device is off'
class Tv(Device):
    def turn_on(self):
        return 'tv is on'
    def turn_off(self):
        return 'tv is off'
class Fan(Device):
    def turn_on(self):
        return 'tv is on'
    def turn_off(self):
        return 'tv is off'
class RemoteControl:
    def __init__(self,device):
        self.d=device
    def turn_on(self):
        return self.d.turn_on()
    def turn_of(self):
        return self.d.turn_off()
