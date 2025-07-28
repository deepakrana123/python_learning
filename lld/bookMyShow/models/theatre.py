import uuid


class Theatre:
    def __init__(self, name, city, address):
        self.theatre_id = str(uuid.uuid4())
        self.name = name
        self.city = city
        self.address = address
        self.screens = []

    def addScreen(self, screen):
        self.screens.append(screen)

    def getCity(self):
        return self.city.lower()

    def getAddress(self):
        return self.address.lower()
