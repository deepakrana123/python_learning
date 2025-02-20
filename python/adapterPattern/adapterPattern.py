# thats a legacy code you donot want to chnage it but wants to use to make new thinks
class OldPrinter:
    def __init__(self):
        pass
    def print_text(self,msg):
        print(f"Printing: {msg}")


class NewPrinter:
    def __init__(self,Old):
        self.old=Old
    def print(self,msg):
        return self.old.print_text(msg)

a=NewPrinter(OldPrinter)


# with the help of inheritance

class InheritanceAdapter(OldPrinter):
    def __init__(self):
        pass
    def print(self,msg):
        return self.print_text(msg)
    

class TempertureFarenhite:
    def tempertueFarenhite(self,city):
        weather_data = {
            "New York": 86,  # Fahrenheit
            "London": 68,
            "Tokyo": 77
        }
        return weather_data.get(city,"City Not found")

class TempertureInCelius:
    def __init__(self,weatherApi):
        self.weatherApi = weatherApi
    
    def tempertureToCelisus(self,city):
        temp_fr = self.weatherApi.tempertueFarenhite(city)
        if isinstance(temp_fr,str):
            return temp_fr
        temp_c = (temp_fr - 32) * 5 / 9
        return round(temp_c, 2)
temp_cr=TempertureInCelius(TempertureFarenhite())
print(temp_cr.tempertureToCelisus("New York"))


class USBKeyBoard:
    def connect_via_wire(self):
        return "USB board connect view a keyboard"

class BloothKeyBoard:
    def connect_viw_blooth(self,device):
        return f"BlueTooth board connect view a keyboard",{device}

class Adapter:
    def __init__(self,board):
        self.board=board
    
    def connect_via_blooth(self):
        return self.board.connect_via_wire().replace("USB","BlooTooth")
temp_cr=Adapter(USBKeyBoard()).connect_via_blooth()
print(temp_cr)

    
temp_b=USBKeyBoard()
temp_a=Adapter(temp_b)
temp_blue=BloothKeyBoard()
print(temp_blue.connect_viw_blooth(temp_a.connect_via_blooth()))