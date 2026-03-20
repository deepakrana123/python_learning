class BookDatabase:
    def __init__(self, bookId, title, genre, isbn, status):
        self.bookId = bookId
        self.title = title
        self.genre = genre
        self.isbn = isbn
        self.status = status


class User:
    def __init__(self, userId, name, email, phone, role):
        self.userId = userId
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role


class Member(User):
    def __init__(self, userId, name, email, phone, memebership, borrowedBooks):
        super().__init__(userId, name, email, phone, role="Member")
        self.memebership = memebership
        self.borrowedBooks = borrowedBooks if borrowedBooks is not None else []


class Libarain(User):
    def __init__(self, userId, name, email, phone, employeeID):
        super().__init__(userId, name, email, phone, role="Librarian")
        self.employeeID = employeeID


class Transcation:
    def __init__(
        self, transactionID, bookID, userID, borrowDate, dueDate, returnDate, fine
    ):
        self.transactionID = transactionID
        self.bookID = bookID
        self.userID = userID
        self.borrowDate = borrowDate
        self.dueDate = dueDate
        self.returnDate = returnDate
        self.fine = fine

    def calulcate_fare(self, currentDate):
        if self.returnDate and currentDate > self.returnDate:
            days_late = self.returnDate - currentDate
            self.fine = days_late * 1.0
            return self.fine
        return 0


class Fine:
    def __init__(self, fineID, userID, amount, dueDate, status):
        self.fineID = fineID
        self.userID = userID
        self.amount = amount
        self.dueDate = dueDate
        self.status = status

    def paid_fine(self):
        self.amount = 0
        self.status = "Paid"


class LibarayManage:
    def __init__(self):
        self.books = []
        self.user = []

    def add_book(self, book, userId):
        user = self.find_user(userId)
        if user.role == "librarian":
            self.books.append(book)
        else:
            print("books cannot added as user is not librarian")

    def remove_book(self, bookId, userId):
        user = self.find_user(userId)
        book = self.find_book(bookId)
        if user.role == "librarian" and book:
            self.books.remove(book)
        else:
            print("books cannot added as user is not librarian")

    def borrowed_books(self, bookId, userId):
        user = self.find_user(userId)
        book = self.find_book(bookId)
        if user.role == "member" and book:
            book.status = "borrwoed"
        else:
            print("books cannot added as user is not librarian")

    def return_books(self, bookId, userId):
        user = self.find_user(userId)
        book = self.find_book(bookId)
        if user.role == "member" and book:
            book.status = "avaliable"
        else:
            print("books cannot added as user is not avaliable")

    def add_user(self, user):
        self.user.append(user)

    def remove_user(self, userId):
        self.user.remove(userId)

    def find_user(self, userId):
        return self.user.find(userId)

    def find_books(self, bookId):
        return self.books.find(bookId)
