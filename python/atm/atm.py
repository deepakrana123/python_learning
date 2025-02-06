class Atm:
    def __init__(how):
        how.__pin=''
        how.__balance=0
        print(how)
        # how.menu()
        pass
    def menu(how):
        user_input=input("How would you process   1. Enter 1 to crate pin  2.Enter 2 to deposit 3.Enter for withdraw 4.Enter for check balance ")
        if user_input=='1':
            print('Create Pin')
        elif user_input=='2':
            print('Deposit')
        elif user_input=='3':
            print('Withdraw')
        elif user_input=='4':
            print('Check balance')
        pass
    def createPin(how):
        pass
    def p(how):
        print(how.__pin)
        return how.__pin
# getter
    def get_pin(self):
        return self.__pin
# setter
    def set_pin(self,new_pin):
        self.__pin=new_pin
        print('pin chnaged')



class Fraction:
    def __init__(self,n,d):
        self.num=n
        self.deno=d
    def d(self):
        return self.num//self.deno
    
    def __str__(self):
        return '{}/{}'.format(self.num,self.deno)
    
    def __add__(self,other):
        temp_num=self.num*other.deno + other.num*self.deno
        temp_deno=self.num+other.deno
        return '{}/{}'.format(temp_num,temp_deno)
    def __sub__(self,other):
        temp_num=self.num*other.deno - other.num*self.deno
        temp_deno=self.num+other.deno
        return '{}/{}'.format(temp_num,temp_deno)
    def __mul__(self,other):
        temp_num=self.num*other.deno * other.num*self.deno
        temp_deno=self.num*other.deno
        return '{}/{}'.format(temp_num,temp_deno)
    def __truediv__(self,other):
        temp_num=other.num*self.deno * self.num*other.deno
        temp_deno=self.num *other.deno
        return '{}/{}'.format(temp_num,temp_deno)
    
