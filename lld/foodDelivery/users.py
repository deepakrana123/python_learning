#  to many encaplustion leads to junk code

#  startgey + composotion helps there

# Encapsulation = how you protect and expose data/behavior

# Composition = a design choice that helps you encapsulate better, especially as complexity grows

from abc import ABC, abstractmethod
from enum import Enum

class UserStatus(Enum):
    ACTIVE='ACTIVE', BLOCKED='BLOCKED', DELETED='DELETED'


class RoleStrategy(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def perform_role_action(self):
        pass


class CustomerRole(RoleStrategy):
    def get_role(self):
        return "Customer"

    def perform_role_action(self):
        print("Viewing order history...")


class RestaurantRole(RoleStrategy):
    def get_role(self):
        return "Restaurant"

    def perform_role_action(self):
        print("Managing restaurant menu...")


class AdminRole(RoleStrategy):
    def get_role(self):
        return "Admin"

    def perform_role_action(self):
        print("Managing platform settings...")


class User:
    def __init__(self, userId, name, contactDetails, roleStrategy: RoleStrategy):
        self.userId = userId
        self.name = name
        self.contactDetails = contactDetails
        self.roleStrategy = roleStrategy

    def get_stragey_role(self):
        return self.roleStrategy.get_role()

    def perform_actions(self):
        return self.roleStrategy.perform_role_action()


class SessionManager:
    current_user = None

    @classmethod
    def login(cls, user):
        cls.current_user = user

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def get_current_user(cls):
        return cls.current_user
