from parkingLostConstant import users


class User:
    def __init__(
        self,
        user_id,
        name: str,
        contactNumber: int,
        vehicle,
        isVip: bool,
        company: str,
    ):
        self.user_id = user_id
        self.name = name
        self.contactNumber = contactNumber
        self.vehicle = vehicle
        self.isVip = isVip
        self.company = company
        self.otherDeatils = {}

    def display(self):
        base_info = (
            f"ID: {self.user_id or 'N/A'} | Name: {self.name or 'N/A'} | Contact: {self.contactNumber or 'N/A'} | "
            f"Vehicle: {self.vehicle or 'N/A'} | VIP: {self.isVip} | Company: {self.company or 'N/A'}"
        )
        extra_info = " | ".join([f"{k}: {v}" for k, v in self.otherDeatils.items()])
        return f"{base_info} | {extra_info}" if extra_info else base_info

    def update_other(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.otherDeatils[key] = value

    def __repr__(self):
        return self.display()


class UserBuilder:
    def __init__(self):
        self.user_id = None
        self.name = None
        self.contactNumber = None
        self.vehicle = None
        self.isVip = False
        self.company = None
        self.extra_data = {}

    def set_user_id(self, user_id):
        self.user_id = user_id
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_contact_number(self, contactNumber):
        self.contactNumber = contactNumber
        return self

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle
        return self

    def set_vip_status(self, isVip):
        self.isVip = isVip
        return self

    def set_company(self, company):
        self.company = company
        return self

    def add_extra_data(self, key, value):
        self.extra_data[key] = value
        return self


class UserManager:
    @staticmethod
    def add_user(user):
        if user.user_id in users:
            print(f"User with ID {user.user_id} already exists.")
        else:
            users[user.user_id] = user

    def get_user(self, user_id):
        return users.get(user_id, None)

    @staticmethod
    def update(user_id, key, value):
        if user_id in users:
            users[user_id][key] = value
        else:
            print(f"User with ID {user_id} not present.")

    @staticmethod
    def display_all_users():
        for user in users.values():
            print(user)


class UserManagerSingleTon:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.user_map = {}
        return cls._instance

    def add_user(self, user):
        if user.user_id in self.user_map:
            print(f"User with ID {user.user_id} already exists.")
        else:
            self.user_map[user.user_id] = user

    def get_user(self, user_id):
        return self.user_map.get(user_id, None)

    def update(self, user_id, key, value):
        if user_id in self.user_map:
            self.user_map[user_id][key] = value
        else:
            print(f"User with ID {user_id} not present.")

    def display_all_users(self):
        for user in self.user_map.values():
            print(user)


# dependency injection good for flexibility


class UserManagerDependency:
    def __init__(self, stroage):
        self.user_map = stroage

    def add_user(self, user):
        if user.user_id in self.user_map:
            print(f"User with ID {user.user_id} already exists.")
        else:
            self.user_map[user.user_id] = user

    def get_user(self, user_id):
        return self.user_map.get(user_id, None)

    def update(self, user_id, key, value):
        if user_id in self.user_map:
            self.user_map[user_id][key] = value
        else:
            print(f"User with ID {user_id} not present.")

    def display_all_users(self):
        for user in self.user_map.values():
            print(user)


userManagerDependency = UserManagerDependency(users)


class UserRepository:
    def __init__(self):
        self.userStroage = {}

    def add_user(self, user):
        if user.user_id in self.userStroage:
            print(f"User with ID {user.user_id} already exists.")
        else:
            self.userStroage[user.user_id] = user

    def get_user(self, user_id):
        return self.userStroage.get(user_id, None)

    def update(self, user_id, key, value):
        if user_id in self.userStroage:
            self.userStroage[user_id][key] = value
        else:
            print(f"User with ID {user_id} not present.")

    def display_all_users(self):
        for user in self.userStroage.values():
            print(user)


import pickle


class UserCache:
    def __init__(self):
        self.cache = {}

    def add_user(self, user):
        self.cache[user.user_id] = user

    def get_user(self, user_id):
        return self.cache.get(user_id)

    def save_to_file(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.cache, f)

    def load_from_file(self, filename):
        with open(filename, "rb") as f:
            self.cache = pickle.load(f)
