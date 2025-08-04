from collections import defaultdict, OrderedDict


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class GroupExpense:
    def __init__(self, group_name):
        self.group_name = group_name
        self.users = set()
        self.balance_sheet = BalanceSheet()


class BalanceSheet:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(float))

    def add_transcation(self, payer, payee, amount):
        self.balances[payer][payee] += amount
        self.balances[payee][payer] -= amount

    def show_balance(self):
        for user, owed in self.balances.items:
            for other_user, amount in owed.items():
                if amount > 0:
                    print(f"{user} owes {other_user}: {amount:.2f}")


class Expense:
    def __init__(self):
        self.users = {}
        self.balance_sheet = BalanceSheet()
        self.groups = {}

    def add_user(self, user_id, name):
        self.users[user_id] = User(user_id, name)

    def add_expense(self, paid_to, amount, splits):
        # splits is dicts of user_id and amount how much it have to pay

        if sum(splits.values()) != amount:
            print("Split amounts do not settle")
            return
        for user_id, split_amount in splits.items():
            if user_id != paid_to:
                self.balance_sheet.add_transcation(user_id, paid_to, split_amount)

    def show_balance(self):
        self.balance_sheet.show_balance(self.users)

    def settle_up(self, user1, user2, fullPayment, payment):

        if (
            user1 not in self.balance_sheet.balances
            or user2 not in self.balance_sheet.balances[user1]
        ):
            print("No balance exists between the users.")
            return
        owed = self.balance_sheet.balances[user1][user2]
        if fullPayment:
            if owed == payment:
                del self.balance_sheet.balances[user1][user2]
                del self.balance_sheet.balances[user2][user1]
            else:
                print("Amount is overpay")
        else:
            if payment > owed:
                print("Cannot overpay.")
                return
            self.balance_sheet.balances[user1][user2] -= payment
            self.balance_sheet.balances[user2][user1] += payment
            if self.balance_sheet.balances[user1][user2] == 0:
                del self.balance_sheet.balances[user1][user2]
                del self.balance_sheet.balances[user2][user1]

    def auto_split(self, user1, partcipants, amount):
        for users in partcipants:
            self.balance_sheet.add_transcation(users, user1, amount // len(partcipants))

    def create_group(self, group_name, user_ids):
        if group_name in self.groups:
            print("Group already exists.")
            return

        group = GroupExpense(group_name)

        for uid in user_ids:
            if uid not in self.users:
                print(f"user {uid} does not")
                return
            group.users.add(uid)
        self.groups[group_name] = group

    def add_group_expense(self, group_name, paid_to, amount, splits):
        if group_name not in self.groups:
            print("Group not found.")
            return
        group = self.groups[group_name]
        if paid_to not in group.users:
            print("Payer not in group.")
            return
        for uid in splits:
            if uid not in group.users:
                print(f"User {uid} not in group.")
                return
        for user_id, split_amount in splits.items():
            if user_id != paid_to:
                group.balance_sheet.add_transcation(user_id, paid_to, split_amount)

    def show_group_balance(self, group_name):
        if group_name in self.groups:
            self.groups[group_name].balance_sheet.show_balance()
