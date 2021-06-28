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
subscribers = []

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
        for employee in Employees:
            AllData.append(json.dumps(employee,indent=3, cls=classEncoder))
        for subs in subscribers:
            AllData.append(json.dumps(subs, indent=3, cls=classEncoder))
        print("Please enter the backup file name")
        name = input()
        with open (name, "w") as file:
            json.dump(AllData, file)
            print("System is backing up all data...")
            time.sleep(2)
            print("Backup succes")
            print(f"Data is stored as {name} please use this when restoring data")
            time.sleep(4)
            file.close()
        return

    def restoreBackup(self):
        global person,bookList,bookLoans,Employees,subscribers
        person = []
        bookList = []
        bookLoans = []
        Employees = []
        subscribers = []
        print("Please enter the backup file")
        file = input()
        try:
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
                        elif "name" in linetoDict:
                            Employees.append(librarian(linetoDict.get("name"),linetoDict.get("lname"),linetoDict.get("employeeNumber"),linetoDict.get("role")))
                        if linetoDict.get("role") == "Subscriber":
                            subscribers.append(Subscriber(linetoDict.get("fname"),linetoDict.get("lname"),linetoDict.get("address"),linetoDict.get("username"),linetoDict.get("email"),linetoDict.get("role")))
            print("All data has been restored...")
            time.sleep(2)
        except:
            print("File not found please try again")
            time.sleep(2)
        return


    def buildCustomerSet(self, customerset):
        global person
        with open(customerset, 'r')as file:
            reader = csv.reader(file)
            customers = []
            for row in reader:
                customers.append(row)
            for customer in customers:
                person.append(Person(customer[3], customer[4], customer[5], customer[9], customer[8]))
        return

    def buildBookSet(self, booksset):
        global bookList
        with open(booksset, 'r')as books:
            bookcatalogue = json.load(books)
        for book in bookcatalogue:
            isbn=random.randrange(1000000000, 9999999999)
            copies= random.randrange(1,5)
            bookItem = BookItem(book.get("title"), book.get("author"), book.get("year"), isbn, copies)
            bookList.append(bookItem)
        return
    
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
        print(f"\n{btitle} has been added to the catalogue")
        time.sleep(2)
        return

class Subscriber(Person):
    def __init__(self, subname, lname, address, username, email, role,):
        super().__init__(subname, lname, address, username, email)
        self.role = role

class catalogue:
    def __init__(self, catalogueName):
        self.name = catalogueName
    
    def catalogueShow(self, user):
        if len(bookList) == 0:
            print("No books found")
            time.sleep(2)
        else:
            while(True):
                os.system('cls||clear')
                print(f"\nWelcome to the {Libraryscatalogue.name}!")
                try:
                    for books in bookList:
                        print(f"\nTitle: {books.title}\nWritten by: {books.author}\nPublished in: {books.year}\nISBN: {books.isbn}\nAvailable: {books.copies}\n")
                except:
                    print("\nNo books found\n")
                    time.sleep(2)
                print("What would u like to do?\n1. Search book\n2. Back")
                choice = input()
                if choice == "1":
                    Libraryscatalogue.bookSearcher(user)
                    return
                elif choice == "2":
                    break
                elif choice != "1" or choice != "2":
                    print("Please make a valid input")
                    time.sleep(2)
                break
        return

    def bookSearcher(self, user):
        if len(bookList) == 0:
            print("No books found")
            time.sleep(2)
        else: 
            while(True):
                print("\nPlease type the name of the book, the isbn, the published year or the author (type 'exit' to stop)")
                bookToSearch = input()
                found = False
                booksFound = 0
                if bookToSearch == "exit":
                    print("You will be send back to the main menu")
                    time.sleep(2)
                    break
                else:
                    try:
                        for books in bookList:                       
                            if bookToSearch == books.title or bookToSearch == books.author or bookToSearch == str(books.year) or bookToSearch == str(books.isbn):
                                print(f"\nTitle: {books.title}\nWritten by: {books.author}\nPublished in: {books.year}\nISBN: {books.isbn}\nAvailable: {books.copies}\n")
                                found = True
                                bookFound = books
                                booksFound += 1
                        if booksFound > 1:
                            print("Multiple books found please search more specific")
                            time.sleep(2)
                        else:
                            if found == False:
                                print("\nBook not found\n")
                                time.sleep(2)
                                break
                            print("What would you like to do?\n1. Loan book\n2. Search another book\n3. Back")
                            choice = input()
                            if choice == "1":
                                bookLoanScreen(user, bookFound)
                                return
                            elif choice == "2":
                                break
                            elif choice == "3":
                                break
                    except:
                        print("\nNo books found\n")
                        time.sleep(2)
                        mainScreen(user)
        return

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
        global bookLoans, subscribers
        bookLoans.append(LoanItem(bookitem, person))
        subscribers.append(Subscriber(person.fname,person.lname,person.address,person.username,person.email,"Subscriber"))
        return

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
                    print("Currently loaned books:\n")
                    time.sleep(1)
                    for books in bookLoans:
                        print(f"Title: {books.book.title}\nBy: {books.person.fname}\n")
                    print("Enter anything to continue...")
                    input()
            elif choice == "2":
                break
            elif choice != "1" or choice != "2":
                print("Please enter a valid input")
                time.sleep(2)
        return
    
    def returnBook(self,user):
        found = False
        bookfound = False
        if len(subscribers) == 0:
                print("No loaned books found")
                time.sleep(2)
        else:
            print("Loaned books:")
            for books in bookLoans:
                if books.person.fname == user.fname:
                    print(f"{books.book.title}")
                    found = True
            if found == False:
                print("You have no loaned books")
                time.sleep(2)
            else:
                print("Please enter the title of the book you would like to return (type 'exit' to stop)")
                choice = input()
                if choice == "exit":
                    return
                else:
                    for bookItem in bookList:
                        if bookItem.title == choice:
                            bookItem.copies +=1
                            for book in bookLoans:
                                if choice == book.book.title:
                                    bookLoans.remove(book)
                                    break
                            print(f"{bookItem.title} has been returned")
                            time.sleep(2)
                            bookfound = True
                            break
                    if bookfound == False:
                        print("Book not found please try again")
                        time.sleep(2)
                        found = True
                    if found == False:
                        print("No loaned books found")
                        time.sleep(2)
        return

class LoanItem:
    def __init__(self, book, person):
        self.book = book
        self.person = person

class classEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

LoanAdminiStration = LoanAdministration("Pythons library loan administration")
PublicLibrarySystem = PublicLibrary("Pythons Library")
Libraryscatalogue = catalogue("Pythons catalogue")
defaultLibrarian = librarian("admin", "admin", "0000","Librarian")
Employees.append(defaultLibrarian)

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
                        break
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
                    if username == persons.username:
                        print(f"\n{persons.fname} logging in...")
                        time.sleep(2)
                        found = True
                        mainScreen(persons)
                        break
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
        print("1. Search book\n2. Show catalogue\n3. Return book\n4. Back")
        choice = input()
        print("")
        found = False
        bookfound = False
        if choice == "1":
            Libraryscatalogue.bookSearcher(user)
        elif choice == "2":
            Libraryscatalogue.catalogueShow(user)
        elif choice == "3":
            LoanAdminiStration.returnBook(user)
        elif choice == "4":
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
                    break
                else:
                    bookItem.copies -= 1
                    LoanAdminiStration.addBookLoan(bookItem,user)
                    print(f"Thank you {user.fname} your loan has been placed")
                    time.sleep(2)
                    break
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

defaultLibrarian.buildBookSet("booksset1.json")
defaultLibrarian.buildCustomerSet("FakeNameSet20.csv")
login()
