from abc import ABC, abstractmethod


class Card:
    def __init__(self, pin, cardNumber):
        self.__pin = pin
        self.__cardNumber = cardNumber

    def getPin(self):
        return self.__pin

    def setPin(self, pin):
        self.__pin = pin
        return self.__pin

    def getCardNumber(self):
        return self.__cardNumber


# class Transcation:
#     def __ini__(self, amount, transcationId, account):
#         self.transcationId = transcationId
#         self.account = account
#         self.amount = amount

#     @abstractmethod
#     def execute(self):
#         pass


class DepositTranscation:
    def __ini__(self, amount, transcationId, account):
        self.transcationId = transcationId
        self.account = account
        self.amount = amount

    def execute(self):
        self.account.credit(self.amount)


class WithdrawalTranscation:
    def __ini__(self, amount, transcationId, account):
        self.transcationId = transcationId
        self.account = account
        self.amount = amount

    def execute(self):
        self.account.withdraw(self.amount)


class TransactionFactory:
    _transaction_types = {
        "withdraw": WithdrawalTranscation,
        "deposit": DepositTranscation,
    }

    @staticmethod
    def create_transaction(transaction_type, amount, transaction_id, account):
        transaction_class = TransactionFactory._transaction_types.get(transaction_type)
        if not transaction_class:
            raise ValueError("Invalid transaction type")
        return transaction_class(amount, transaction_id, account)


class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount

    def credit(self, amount):
        self.balance += amount

    def getBalance(self):
        return self.balance

    def getAccountNumber(self):
        return self.account_number


import threading
import datetime


class CashDispenser:
    def __init__(self, amount):
        self.cash_avilable = amount
        self.lock = threading.Lock()

    def dispense_cash(self, currentAmount):
        with self.lock:
            if self.cash_avilable > currentAmount:
                self.cash_avilable -= currentAmount
            else:
                raise ValueError("Insufficient cash available in the ATM.")


class BankingService:
    def __init__(self):
        self.account = {}
        self.cardNumber = {}

    def create_account(self, accountNumber, amount):
        self.account[accountNumber] = amount

    def createCardNumber(self, accountNumber, cardNumber, pin):
        if accountNumber not in self.account:
            raise ValueError("Not having bank account")
        self.cardNumber[cardNumber] = [accountNumber, pin]

    def changePin(self, cardNumber, newPin):
        if cardNumber not in self.cardNumber:
            raise ValueError("Not having the card Number")
        self.cardNumber[cardNumber][1] = newPin

    def getCardNumber(self, cardNumber):
        return self.cardNumber[cardNumber]

    def get_account(self, accountNumber):
        return self.account[accountNumber]

    def get_balance(self):
        return self.amount

    def process_transaction(self, transaction):
        transaction.execute()


class Atm:
    def __init__(self, bankingService, cash_dispenser):
        self.bankingService = bankingService
        self.cash_dispenser = cash_dispenser
        self.transaction_counter = 0
        self.transaction_lock = threading.Lock()

    def authenticateUser(self, cardNumber, pin):
        cards = self.bankingService.getCardNumber(cardNumber)
        if not cards:
            raise ValueError("not member")
        if cards[cardNumber][1] == pin:
            print("user authenticated")

    def checkBalance(self, accountNumber):
        account = self.bankingService.get_account(accountNumber)
        return account.get_balance()

    def depositAmount(self, accountNumber, amount):
        userAccount = self.bankingService.get_account(accountNumber)
        deposit = TransactionFactory(
            "deposit", amount, self.getTranscationId, userAccount
        )
        self.bankingService.process_transaction(deposit)

    def withdrwalAmount(self, accountNumber, amount):
        userAccount = self.bankingService.get_account(accountNumber)
        deposit = TransactionFactory(
            "withdraw", amount, self.getTranscationId, userAccount
        )
        self.bankingService.process_transaction(deposit)
        self.cash_dispenser.dispense_cash(int(amount))

    def getTranscationId(self):
        with self.transaction_lock:
            self.transaction_counter += 1
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            return f"TXN{timestamp}{self.transaction_counter:010d}"
