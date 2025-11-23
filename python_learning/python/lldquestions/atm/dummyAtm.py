import time
from enum import Enum


# Transaction types
class TransactionType(Enum):
    BALANCE_INQUIRY = 1
    DEPOSIT = 2
    WITHDRAW = 3
    TRANSFER = 4


# Singleton Pattern for ATM
class ATM:
    _instance = None

    def __new__(cls, id, location):
        if cls._instance is None:
            cls._instance = super(ATM, cls).__new__(cls)
            cls._instance.id = id
            cls._instance.location = location
            cls._instance.cash_dispenser = CashDispenser()
        return cls._instance

    def authenticate_user(self, customer, pin):
        attempts = 3
        while attempts > 0:
            if customer.card.validate_pin(pin):
                print("User authenticated successfully!")
                return True
            else:
                attempts -= 1
                print(f"Incorrect PIN. Attempts left: {attempts}")
        print("Card blocked due to too many failed attempts.")
        return False

    def eject_card(self):
        print("Ejecting card...")
        time.sleep(2)

    def make_transaction(self, transaction_type, customer, amount=0, dest_account=None):
        transaction = TransactionFactory.create_transaction(
            transaction_type, amount, dest_account
        )
        if transaction:
            transaction.execute(customer)
        else:
            print("Invalid transaction type!")


# Cash dispenser with simple bill logic
class CashDispenser:
    def __init__(self):
        self.cash_available = 10000

    def dispense_cash(self, amount):
        if amount <= self.cash_available:
            self.cash_available -= amount
            print(f"Dispensed: ${amount}")
            return True
        else:
            print("ATM out of cash!")
            return False


# Basic account and card classes
class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def debit(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def credit(self, amount):
        self.balance += amount


class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.__pin = pin

    def validate_pin(self, pin):
        return pin == self.__pin


# Customer class
class Customer:
    def __init__(self, name, card, account):
        self.name = name
        self.card = card
        self.account = account


# Factory pattern for transaction creation
class TransactionFactory:
    @staticmethod
    def create_transaction(transaction_type, amount=0, dest_account=None):
        if transaction_type == TransactionType.BALANCE_INQUIRY:
            return BalanceInquiry()
        elif transaction_type == TransactionType.DEPOSIT:
            return Deposit(amount)
        elif transaction_type == TransactionType.WITHDRAW:
            return Withdraw(amount)
        elif transaction_type == TransactionType.TRANSFER:
            return Transfer(amount, dest_account)
        return None


# Transaction classes
class Transaction:
    def execute(self, customer):
        pass


class BalanceInquiry(Transaction):
    def execute(self, customer):
        print(f"Available balance: ${customer.account.balance}")


class Deposit(Transaction):
    def __init__(self, amount):
        self.amount = amount

    def execute(self, customer):
        customer.account.credit(self.amount)
        print(f"Deposited: ${self.amount}")


class Withdraw(Transaction):
    def __init__(self, amount):
        self.amount = amount

    def execute(self, customer):
        if customer.account.debit(self.amount):
            atm = ATM._instance
            atm.cash_dispenser.dispense_cash(self.amount)
        else:
            print("Insufficient funds!")


class Transfer(Transaction):
    def __init__(self, amount, dest_account):
        self.amount = amount
        self.dest_account = dest_account

    def execute(self, customer):
        if customer.account.debit(self.amount):
            self.dest_account.credit(self.amount)
            print(
                f"Transferred ${self.amount} to account {self.dest_account.account_number}"
            )
        else:
            print("Insufficient funds for transfer!")


# Example usage
if __name__ == "__main__":
    atm = ATM("1234", "Downtown")

    # Creating a customer
    account = Account("0987654321", 5000)
    card = Card("1111222233334444", 1234)
    customer = Customer("John Doe", card, account)

    # Flow
    if atm.authenticate_user(customer, 1234):
        atm.make_transaction(TransactionType.BALANCE_INQUIRY, customer)
        atm.make_transaction(TransactionType.DEPOSIT, customer, 1000)
        atm.make_transaction(TransactionType.WITHDRAW, customer, 300)
        atm.eject_card()

# Let me know what you think — or if you want to push this further! 🚀
