#MODULES
import json
from json import JSONEncoder
import time
import csv
import os
import random

#BACKEND
person = []
bookList = []
bookLoans = []
Employees = []

class PublicLibrary:
    def __init__(self, libraryName):
        self.name = libraryName

class Person:
    def __init__(self, fname, lname, address, username, email):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.username = username
        self.email = email

class librarian:
    def __init__(self, fname, lname, employeenumber, role):
        self.name = fname
        self.lname = lname
        self.employeeNumber = employeenumber
        self.role = role

    def backupSystem(self):
        AllData = []
        for persons in person:
            AllData.append(json.dumps(persons, indent=3, cls=classEncoder))
        for books in bookList:
            AllData.append(json.dumps(books,indent=3, cls=classEncoder))
        for loans in bookLoans:
            AllData.append(json.dumps(loans,indent=3, cls=classEncoder))
        with open ("PLSbackup.json", "w") as file:
            json.dump(AllData, file)
            print("System is backing up all data...")
            time.sleep(2)
            print("Backup succes")
            time.sleep(2)
            file.close()

    def restoreBackup(self):
        global person
        print("Please enter the backup file (Dont forget the file extension)")
        file = input()
        with open (file, "r")as importedfile:
            for items in importedfile:
                temp = json.loads(items)
                for lines in temp:
                    linetoDict = json.loads(lines)
                    if "fname" in linetoDict:
                        person.append(Person(linetoDict.get("fname"),linetoDict.get("lname"),linetoDict.get("address"),linetoDict.get("username"),linetoDict.get("email")))
                    elif "title" in linetoDict:
                        bookList.append(BookItem(linetoDict.get("title"),linetoDict.get("author"),linetoDict.get("year"),linetoDict.get("isbn"),linetoDict.get("copies")))
                    elif "book" in linetoDict:
                        bookname = linetoDict.get("book")
                        loaner = linetoDict.get("person")
                        loanedBook = BookItem(bookname.get("title"),bookname.get("author"),bookname.get("year"),bookname.get("isbn"),bookname.get("copies"))
                        loaningPerson = Person(loaner.get("fname"),loaner.get("lname"),loaner.get("address"),loaner.get("username"),loaner.get("email"))
                        bookLoans.append(LoanItem(loanedBook,loaningPerson))
        print("All data has been restored...")
        time.sleep(2)


    def buildCustomerSet(self, customerset):
        global person
        with open(customerset, 'r')as file:
            reader = csv.reader(file)
            customers = []
            person = []
            for row in reader:
                customers.append(row)
            for customer in customers:
                person.append(Person(customer[3], customer[4], customer[5], customer[9], customer[8]))

    def buildBookSet(self, booksset):
        global bookList
        with open(booksset, 'r')as books:
            bookCatalog = json.load(books)
        bookList = []
        for book in bookCatalog:
            isbn=random.randrange(1000000000, 9999999999)
            copies= random.randrange(1,5)
            bookItem = BookItem(book.get("title"), book.get("author"), book.get("year"), isbn, copies)
            bookList.append(bookItem)
    
    def addBook(self):
        global bookList
        print("Please enter the book title")
        btitle = input()
        print("Please enter the book author")
        bauthor = input()
        print("Please enter the published year")
        byear = input()
        print("Please enter the isbn number")
        bisbn = input()
        print("Please enter the amount of book copies")
        while(True):
            bcopies = input()
            try:
                int(bcopies)
                break
            except:
                print("Please enter a number")
        print("Adding book...")
        time.sleep(2)
        bookList.append(BookItem(btitle,bauthor,byear,bisbn,int(bcopies)))
        print(f"\n{btitle} has been added to the catalog")
        time.sleep(2)

class Subscriber(Person):
    def __init__(self, fname, lname, address, username, email, role):
        super().__init__(fname, lname, address, username, email)
        self.role = role 

class Catalog:
    def __init__(self, catalogName):
        self.name = catalogName
    
    def catalogShow(self, user):
        while(True):
            os.system('cls||clear')
            print(f"\nWelcome to the {LibrarysCatalog.name}!")
            try:
                for books in bookList:
                    print(f"\nTitle: {books.title}\nWritten by: {books.author}\nPublished in: {books.year}\nISBN: {books.isbn}\nAvailable: {books.copies}\n")
            except:
                print("\nNo books found\n")
                time.sleep(2)
            print("What would u like to do?\n1. Search book\n2. Back")
            choice = input()
            if choice == "1":
                LibrarysCatalog.bookSearcher(user)
            elif choice == "2":
                break
            elif choice != "1" or choice != "2":
                print("Please make a valid input")
                time.sleep(2)

    def bookSearcher(self, user):
        while(True):
            print("\nPlease type the name of the book, the isbn, the published year or the author (type 'exit' to stop)")
            bookToSearch = input()
            found = False
            bookL = ""
            booksFound = 0
            if bookToSearch == "exit":
                print("You will be send back to the main menu")
                time.sleep(2)
                break
            else:
                try:
                    for books in bookList:                       
                        book = f"{books.title} {books.author} {books.year} {books.isbn}"
                        if bookToSearch in book:
                            print(f"\nTitle: {books.title}\nWritten by: {books.author}\nPublished in: {books.year}\nISBN: {books.isbn}\nAvailable: {books.copies}\n")
                            bookL += f"\nTitle: {books.title}\nWritten by: {books.author}\nPublished in: {books.year}\nISBN: {books.isbn}\nAvailable: {books.copies}\n"
                            found = True
                            bookFound = books
                            booksFound += 1
                    if booksFound > 1:
                        print("Multiple books found please search more specific")
                        time.sleep(1)
                    else:
                        print("What would you like to do?\n1. Loan book\n2. Search another book\n3. Back")
                        choice = input()
                        if choice == "1":
                            bookLoanScreen(user, bookFound)
                        elif choice == "2":
                            pass
                        elif choice == "3":
                            break
                        if found == False:
                            print("\nBook not found\n")
                            time.sleep(2)
                            mainScreen(user)
                except:
                    print("\nNo books found\n")
                    time.sleep(2)
                    mainScreen(user)

class BookItem:
    def __init__(self, title, author, year, ISBN, copies):
        self.title = title
        self.author = author
        self.isbn = ISBN
        self.year = year
        self.copies = copies

class LoanAdministration:
    def __init__(self, loanitemsList):
        self.LoanedIemsListName = loanitemsList
    
    def addBookLoan(self, bookitem, person):
        global bookLoans
        bookLoans.append(LoanItem(bookitem, person))

    def showLoanAdministration(self):
        while(True):
            os.system('cls||clear')
            print(f"Welcome to {LoanAdminiStration.LoanedIemsListName}!")
            print("Please type what you would like to do\n")
            print("1. Show loaned books\n2. Back")
            choice = input()
            if choice == "1":
                if len(bookLoans) == 0:
                    print("No loaned books found")
                    time.sleep(2)
                else:
                    print("Currently loaned books:")
                    time.sleep(2)
                    for books in bookLoans:
                        print(f"Title: {books.book.title}\nBy: {books.person.fname}\n")
                    print("Enter anything to continue...")
                    input()
            elif choice == "2":
                break
            elif choice != "1" or choice != "2":
                print("Please enter a valid input")
                time.sleep(2)

class LoanItem:
    def __init__(self, book, person):
        self.book = book
        self.person = person

class classEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

LoanAdminiStration = LoanAdministration("Pythons library loan administration")
PublicLibrarySystem = PublicLibrary("Pythons Library")
LibrarysCatalog = Catalog("Pythons Catalog")

#FRONTEND
def login():
    while(True):
        os.system('cls||clear')
        print(f"\nWelcome to {PublicLibrarySystem.name}!")
        print("Please enter the number of what you would like to do\n")
        print("1. Continue as customer\n2. Continue as librarian\n3. Register librarian\n4. Exit")
        choice = input()
        print("")
        if choice == "1":
            loginScreen()
        elif choice == "2":
            if len(Employees) == 0:
                print("No employees registerd please register a librarian first")
                time.sleep(2)
            else:
                print("Please enter your name")
                RegisterdLibrarianName = input()
                for employee in Employees:
                    if employee.name == RegisterdLibrarianName:
                        librarianScreen(employee)
        elif choice == "3":
            print("Please enter your name")
            libName = input()
            print("Please enter your surname")
            libSurname = input()
            print("Please enter your employee number")
            libNumb = input()
            print("Thank you your account is being created")
            time.sleep(2)
            NewLibrarian = Employees.append(librarian(libName,libSurname,libNumb,"Librarian"))
            print("Your account has been created!")
            time.sleep(2)
        elif choice == "4":
            exit()
        elif choice != "1" or choice != "2" or choice != "3" or choice != "4":
            print("Please make a valid input")

def loginScreen():
    while(True):
        os.system('cls||clear')
        print("Welcome customer")
        print("Please type what you would like to do\n")
        print("1. login\n2. Register\n3. Back")
        choice = input()
        if choice == "2":
            print("Please enter your firstname")
            firstname = input()
            print("Please enter your lastname")
            lastname = input()
            print("Please enter your addresss")
            address = input()
            print("Please enter your username")
            username = input()
            print("Please enter your email")
            email = input()
            person.append(Person(firstname,lastname,address,username,email))
            print("Account added!")
            time.sleep(2)
        elif choice == "1":
            print("Please enter your username")
            username = input()
            found = False
            try:
                for persons in person:
                    if username in persons.username:
                        print(f"\n{persons.fname} logging in...")
                        time.sleep(2)
                        found = True
                        mainScreen(persons)
                if found == False:
                    print("User not found please try again")
                    time.sleep(2)
            except:
                pass
        elif choice == "3":
            break
        elif choice != "1" or choice != "2" or choice != "3":
            print("Please make a valid input")
            time.sleep(2)

def mainScreen(user):
    while(True):
        os.system('cls||clear')
        print(f"Welcome {user.fname}\nPlease enter what you would like to do\n")
        print("1. Search book\n2. Show catalog\n3. Back")
        choice = input()
        print("")
        if choice == "1":
            LibrarysCatalog.bookSearcher(user)
        elif choice == "2":
            LibrarysCatalog.catalogShow(user)
        elif choice == "3":
            break
        elif choice != "1" or choice != "2" or choice != "3":
            print("Please make a valid input")
            time.sleep(2)      

def bookLoanScreen(user, bookItem):
    while(True):
        os.system('cls||clear')
        print(f"Welcome {user.fname}!")
        print(f"\nTitle: {bookItem.title}\nWritten by: {bookItem.author}\nPublished in: {bookItem.year}\nISBN: {bookItem.isbn}\nAvailable: {bookItem.copies}\n")
        print("Confirm book loan?\n1. Yes\n2. No")
        while(True):
            option = input()
            if option == "1":
                if bookItem.copies <= 0:
                    print("Sorry there are no copies left")
                    time.sleep(2)
                    mainScreen(user)
                else:
                    bookItem.copies -= 1
                    LoanAdminiStration.addBookLoan(bookItem,user)
                    print(f"Thank you {user.fname} your loan has been placed")
                    time.sleep(2)
                    mainScreen(user)
            elif option == "2":
                print("You will be send back to the main menu")
                time.sleep(2)
                break
            elif option != "1" or option != "2":
                print("Please make a valid input")
                time.sleep(2)
        break

def librarianScreen(librarian):
    while(True):
        os.system('cls||clear')
        print(f"Welcome {librarian.name}")
        print("Please type what you would like to do\n")
        print("1. Import books\n2. Import customers\n3. Add book\n4. Show loan administration\n5. Backup system\n6. Restore from backup\n7. Back")
        choice = input()
        if choice == "1":
            print("Please enter the booksset file name (Only use .json file)")
            filename = input()
            try:
                print("Importing booksset")
                time.sleep(2)
                librarian.buildBookSet(filename)
                print("Booksset imported succesfully")
            except:
                time.sleep(2)
                print("File not found please try again")
            time.sleep(2)
        elif choice == "2":
            print("Please enter the customerset file name (Only use .csv file)")
            filename = input()
            try:
                print("Importing customerset")
                time.sleep(2)
                librarian.buildCustomerSet(filename)
                print("Customerset imported succesfully")
            except:
                time.sleep(2)
                print("File not found please try again")
            time.sleep(2)
        elif choice == "3":
            librarian.addBook()
        elif choice == "4":
            LoanAdminiStration.showLoanAdministration()
        elif choice == "5":
            librarian.backupSystem()
        elif choice == "6":
            librarian.restoreBackup()
        elif choice == "7":
            break
        elif choice != "1" or choice != "2" or choice != "3" or choice != "4" or choice != "5" or choice != "6" or choice != "7":
            print("Please make a valid input")
            time.sleep(2)
l = librarian("f","f","f","f")
l.buildBookSet("booksset1.json")
f = person.append(Person("f","f","f","f","f"))

login()