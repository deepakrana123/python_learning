class Menemnto:
    def __init__(self,text):
        self.text=text

class Text:
    def __init__(self):
        self.text=""
    def write(self,text):
        self.text=text
    def save(self):
        return Menemnto(self.tex)
    def undo(self,menemnto):
        self.text = menemnto.text

class Histroy:
    def __init__(self):
        self.histroy=[]
    
    def save(self,menemento):
        self.histroy.append(menemento)
    
    def undo(self):
        if self.histroy:
            self.histroy.pop()
        return None