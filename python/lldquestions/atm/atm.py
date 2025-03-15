from enum import Enum


class TranscationType(Enum):
    BALANCE_INQUIRY, DEPOSIT_CASH, DEPOSIT_CHECK, WITHDRAW, TRANSFER = 1, 2, 3, 4, 5


class Status(Enum):
    SUCCESS, FAILURE, BLOCKED, FULL, PARTIAL, NONE = 1, 2, 3, 4, 5, 6


class CustomerStatus(Enum):
    ACTIVE, BLOCKED, BANNED, COMPROMISED, ARCHIEVED, CLOSED, UNKNOW = (
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    )


class Address:
    def __init__(self, stateAddress, city, state, zipcode, country):
        self.stateAddress = stateAddress
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country


class Customer:
    def __init__(self, name, email, phone, status, address):
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        self.status = status
        self.__card = Card()
        self.__account = Account()

    def make_transcation(self, transcation):
        pass

    def get_billing_address(self):
        pass


class Card:
    def __init__(self, number, card_expiry, pin, customer_name):
        self.number = number
        self.card_expiry = card_expiry
        self.pin = pin
        self.customer_name = customer_name

    def get_billing_address(self):
        pass

    def get_pin(self):
        return self.pin


class Account:
    def __init__(self, accountNumber):
        self.__accountNumber = accountNumber
        self.__totalbalance = 0
        self.__available_balance = 0

    def getAccountNumber(self):
        return self.__accountNumber

    def get_available_balance(self):
        return self.__available_balance

    def set_available_balance(self, amount):
        if amount >= 0:
            self.__available_balance = amount
        else:
            print("Balance can't be negative")

    def get_total_balance(self):
        return self.__totalbalance

    def set_total_balance(self, amount):
        if amount >= 0:
            self.__totalbalance = amount
        else:
            print("Total balance can't be negative")


class SavingAccount(Account):
    def __init__(self, withdraw_limit):
        self.withdraw_limit = withdraw_limit


class CheckingAccount(Account):
    def __init__(self, debit_card_number):
        self.__debit_card_number = debit_card_number


from abc import ABC


class Bank:
    def __init__(self, name, bank_code):
        self.__name = name
        self.__bank_code = bank_code

    def get_bank_code(self):
        return self.__bank_code

    def add_atm(self, atm):
        None


class CashDispenser:
    def __init__(self):
        self.fifty = 0
        self.twenty = 0

    def dispense_cash(self, amount):
        pass

    def can_dispense_cash(self):
        None


class Keypad:
    def __init__(self):
        pass

    def get_input(self):
        pass


class Screen:
    def showTransctionMessage(self, message):
        None

    def get_input(self):
        None


class CashDeposit:
    def __init__(self):
        pass


class CheckDeposit:
    def __init__(self):
        pass


class Printer:
    def printer(self, transcations):
        pass


class DepositSlot(ABC):
    def __init__(self):
        self.totalAmount = 0

    def getTotalAmount(self):
        return self.totalAmount


class CheckDepoitSlot(DepositSlot):
    def get_check_amount(self):
        pass


class CashDepoistSlot(DepositSlot):
    def get_cash_amount(self):
        pass


class Transaction:
    def __init__(self, id, creation_date, status):
        self.__transcation_id = id
        self.__creation_date = creation_date
        self.__status = status

    def make_transition():
        pass


class BalanceInquiry(Transaction):
    def __init__(self, account_id):
        self.__account_id = account_id

    def get_account_id(self):
        return self.__account_id


class Deposit(Transaction):
    def __init__(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount


class CheckDeposit(Deposit):
    def __init__(self, check_number, bank_code):
        self.__check_number = check_number
        self.__bank_code = bank_code

    def get_check_number(self):
        return self.__check_number


class CashDeposit(Deposit):
    def __init__(self, cash_deposit_limit):
        self.__cash_deposit_limit = cash_deposit_limit

    def get_cash_deposit_limit(self):
        return self.__cash_deposit_limit


class Withdraw(Transaction):
    def __init__(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount


class Transfer(Transaction):
    def __init__(self, destination_account_number, amount):
        self.__destination_account_number = destination_account_number

    def get_destination_account(self):
        return self.__destination_account_number


class Manage:
    def __init__(self):
        self.account = Account("09876543210", 10000, 9000)
        self.card = Card("98765432100", "21/12/32", 2345, "Devendra")
        self.user = Customer(
            "devendra",
            "rdev@gmail.com",
            "new hear",
            "9876543210",
            "active",
            self.card,
            self.account,
        )

    def balance_inquiry(self):
        balance_enquiry = BalanceInquiry(self.account.getAccountNumber())
        balance = self.account.get_available_balance()
        print(
            f"Available balance for {self.user.name}: {balance}:{balance_enquiry.get_account_id()}"
        )

    def checkDepoist(self, amount, check_number, bank_code):
        depoist_enquiry = CheckDeposit(amount, check_number, bank_code)
        amount = depoist_enquiry.get_amount()
        currentBalance = self.account.get_available_balance()
        totalBalance = self.account.get_total_balance()
        self.account.set_available_balance(currentBalance + amount)
        self.account.set_available_balance(totalBalance + amount)
        print(
            f"Available balance for {self.user.name}:{self.account.get_available_balance()}"
        )

    def cashDepoist(self, amount):
        depoist_enquiry = CashDeposit(amount)
        amount = depoist_enquiry.get_amount()
        currentBalance = self.account.get_available_balance()
        totalBalance = self.account.get_total_balance()
        self.account.set_available_balance(currentBalance + amount)
        self.account.set_available_balance(totalBalance + amount)
        print(
            f"Available balance for {self.user.name}:{self.account.get_available_balance()}"
        )

    def withDrwaAmount(self, amount):
        withdraw_enquiry = Withdraw(amount)
        amount = withdraw_enquiry.get_amount()
        currentBalance = self.account.get_available_balance()
        totalBalance = self.account.get_total_balance()
        if currentBalance < amount:
            print("in sufficient money")
        else:
            self.account.set_available_balance(currentBalance - amount)
            self.account.set_total_balance(totalBalance - amount)
        print(f" cash withdrwal {amount}")

    def transferMoney(self, destination_account_number, amount):
        transfer_enquiry = Transfer(destination_account_number, amount)
        currentBalance = self.account.get_available_balance()
        totalBalance = self.account.get_total_balance()
        if currentBalance < amount:
            print("in sufficient money")
        else:
            self.account.set_available_balance(currentBalance - amount)
            self.account.set_total_balance(totalBalance - amount)
            print(f"{transfer_enquiry.get_destination_account()} {amount} send")

    def checkPin(self, pin):
        userPin = self.user.__card.get_pin()
        if userPin == pin:
            print("user authenticate")
        else:
            print("not a valid user")


class ATM:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.__cash_dispenser = CashDispenser()
        self.__keypad = Keypad()
        self.__screen = Screen()
        self.__printer = Printer()
        self.__check_deposit = CheckDeposit()
        self.__cash_deposit = CashDeposit
        self.failedAtempts = 0
        self.current_user = None

    def authenticate_user(self, card, pin, customer):
        if card.number == customer.card.number and customer.card.pin == pin:
            if customer.status == "active":
                self.current_user = customer
                self.failed_attempts = 0
                print(f"Authentication successful! Welcome, {customer.name}.")
                self.__screen.showTransctionMessage(
                    f"Authentication successful! Welcome, {customer.name}"
                )
                return True

        else:
            self.failed_attempts += 1
            print("Invalid card number or PIN.")
            self.__screen.showTransctionMessage(f"Invalid card number or PIN.")
            if self.failed_attempts >= 3:
                customer.status = "blocked"
                print("Card blocked due to multiple failed attempts.")
            return False

    def make_transaction(self, transcation_type, amount, dest_number):
        if transcation_type == "balance_inquiry":
            balance = BalanceInquiry(self.current_user.__account.getAccountNumber())
            self.__printer(balance)
            self.__screen(
                balance.get_account_id(), self.current_user.__account.avaliableBalance
            )
        if transcation_type == "withdraw":
            withdraw = Withdraw(amount)
            amount_available = self.current_user.__account.get_available_balance()
            amount1 = self.current_user.__account.get_total_balance()
            if amount < amount_available:
                self.__screen("Insuficent balane")
            else:
                self.current_user.__account.set_available_balance(
                    amount_available - amount
                )
                self.current_user.__account.set_total_balance(
                    amount1 - amount_available
                )
            self.__printer(withdraw)
