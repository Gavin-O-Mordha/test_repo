from useful_functions import *
from datetime import datetime

def Borrow_a_Book():
    '''Updates the inventory that a book has been borrowed and creates a record of the borrowing'''
    # Get a name that is at least 1 character long and at most 20 characters
    name = get_string("Full Name: ")
    while 20 < len(name):
        name = get_string("Full Name: ")

    # Get a membership number that is only valid with a length of 6 digits
    memNo = get_positive_integer("Membership Number: ")
    while len(str(memNo)) != 6:
        memNo = get_positive_integer("Membership Number: ")

    # check for any outstanding borrows
    formatted_datetime = datetime.now().strftime("%d/%m/%Y")
    current_date = formatted_datetime.split("/")
    logs, dates = Review_Borrowed_Books(str(memNo))
    counter = 0
    for date in dates:
        return_date = date.split("/")
        if current_date[0] <= return_date[0] or current_date[1] <= return_date[1]:
            counter+=1
            if counter == 4:
                print("You have borrowed an excess of books already!")
                return

    # Get a book to be borrowed, validated through book_validator
    book = book_validator()

    # update available amount
    with open('book_inventory.txt', 'r') as file:
        counter = -1
        lines = file.readlines()
        for line in lines:
            counter += 1
            line = line.split(", ")
            if book in line[0].capitalize():
                break
        c_available = int(line[2])
        if c_available == 0:
            print("No copies are available for borrowing")
            return
        u_available = str(c_available-1)
        line[2] = u_available
        lines[counter] = ", ".join(line)
    with open('book_inventory.txt', 'w') as file:
        file.writelines(lines)

    # update borrow amount inventory
    with open('book_inventory.txt', 'r') as file:
        counter = -1
        lines = file.readlines()
        for line in lines:
            counter += 1
            line = line.split(", ")
            if book in line[0].capitalize():
                break
        line[3] = str(int(line[3])+1) + "\n"
        lines[counter] = ", ".join(line)
    with open('book_inventory.txt', 'w') as file:
        file.writelines(lines)

    # record of borrowing is written into Borrowed_Books.txt
    print("Book Borrow Recorded!")
    formatted_datetime = datetime.now().strftime("%d/%m/%Y")
    with open('Borrowed_Books.txt', 'a') as file:
        print(f"{name}, {memNo}, {book}, {formatted_datetime}", file=file)

def book_validator() -> str:
    '''forms an array of book titles and ensures the title to be borrowed exists in it'''
    with open("book_inventory.txt", "r") as file:
        books = []
        for line in file:
            line = line.split(", ")
            books.append(line[0].capitalize())
    book = input("Book name: ").capitalize()
    while book not in books:
        book = input("Book name: ")
    return book

def Review_Borrowed_Books(allORnameORnumber: str) -> list:
    '''Finds the logs for the specified grouping, whether that be all or a specific member by their name or number, and appends the logs and return dates to their respective arrays'''
    with open('Borrowed_Books.txt', 'r') as file:
        logs = []
        return_dates = []
        for line in file:
            line = line.strip().split(", ")
            name = line[0]
            number = line[1]
            date = line[3]
            date = date.split("/")
            borrow_day = int(date[0])
            return_day = borrow_day + 7
            month = int(date[1])
            year = int(date[2])

            if return_day > 28 and month == 2 and year%4 != 0:
                return_day-=28
                month+=1

            if return_day > 29 and month == 2 and year%4 == 0:
                return_day-=29
                month+=1

            if return_day > 30 and month in (4, 6, 9, 11):
                return_day-=30
                month+=1

            if return_day > 31 and month in (1, 3, 5, 6, 7, 8, 10, 12):
                return_day-=31
                month+=1
            
            if return_day < 10:
                return_day = "0" + str(return_day)
            if month < 10:
                month = "0" + str(month)
            if 12 < int(month):
                month-=12
                year+=1
            return_date = f"{return_day}/{month}/{year}"
            line[3] = return_date
            line = ", ".join(line)
            if allORnameORnumber == name or allORnameORnumber == number or allORnameORnumber == "all":
                logs.append(line)
                return_dates.append(line)
    return logs, return_dates

def Manage_Inventory():
    '''Manage the inventory with choices of adding a book, removing a book, updating the amounts (total and borrowed) and an option to return to main menu'''
    while True:
        # print a menu and ask what action is to be performed
        print("-"*80)
        print("a) Add a new book (add all required information about the book title,author name, total copies available, and copies borrowed")
        print("b) Remove a book from the inventory.")
        print("c) Update the total copies available or copies borrowed for a book.")
        print("d) Return to the main menu.")
        choice = get_string(">>> ")

        if choice == "A" or choice == "Add a new book":
            Inventory_Add_Book()
                    
        if choice == "B" or choice == "Remove a book":
            Inventory_Remove_Book()
            
            
        if choice == "C" or choice == "Update the database":
            choice = get_string("Edit total copy amount or borrowed copy amount (t/b): ")
            while choice != "Total copy amount" and choice != "T" and choice != "Borrowed copy amount" and choice != "B":
                choice = get_string("Edit total copy amount or borrowed amount (t/b): ")
            book = book_validator()
            
            if choice == "T" or choice == "Total copy amount":
                total_amount = get_positive_integer("Total Amount: ")
                with open('book_inventory.txt', 'r') as file:
                    counter = -1
                    lines = file.readlines()
                    for line in lines:
                        counter += 1
                        line = line.split(", ")
                        if book in line[0].capitalize():
                            line[2] = str(total_amount)
                            break
                    lines[counter] = ", ".join(line)
                with open('book_inventory.txt', 'w') as file:
                    file.writelines(lines)
                print("Total Amount Changed!")

            if choice == "B" or choice == "Borrowed copy amount":
                borrow_amount = get_positive_integer("Borrowed Amount: ")
                with open('book_inventory.txt', 'r') as file:
                    counter = -1
                    lines = file.readlines()
                    for line in lines:
                        counter += 1
                        line = line.split(", ")
                        if book in line[0].capitalize():
                            line[3] = str(borrow_amount) + "\n"
                            break
                    lines[counter] = ", ".join(line)
                with open('book_inventory.txt', 'w') as file:
                    file.writelines(lines)
                print("Borrow Amount Changed!")

        if choice == "D" or choice == "Return to the main menu":
            break

def Inventory_Add_Book():
    '''Retrieve a books name, author, total amount and borrowed amount before appending that information to the Inventory'''
    bookName = get_string("Book Name: ")
    authorName = get_string("Author Name: ")
    copiesAvailable = get_positive_integer("Copies Available: ")
    copiesBorrowed = get_positive_integer("Copies Borrowed: ")
    with open("book_inventory.txt", "a") as file:
        print(f"{bookName}, {authorName}, {copiesAvailable}, {copiesBorrowed}", file=file)
    print("Book Added!")

def Inventory_Remove_Book():
    '''Retrieve a books name before removing its information from the Inventory'''
    book = book_validator()
    with open("book_inventory.txt", 'r') as file:
        lines = file.readlines()
        index = 0
        for line in lines:
            index += 1
            line = line.split(", ")
            if book == line[0].capitalize():
                break
    # Remove the specific lines to delete
    del lines[index - 1]
    # Write the modified lines back to the file
    with open("book_inventory.txt", 'w') as file:
        file.writelines(lines)
    print("Book Removed!")

def main():
    to_get_rid_of_lines_left_over_by_remove_book()
    '''The full Book Management System'''
    while True:
        SYSNAME = "BOOK MANAGEMENT SYSTEM"
        print("-"*80)
        print(f"{SYSNAME:^80}")
        print("-"*80)
        print("a) Borrow a Book\nb) Review Borrowed Books\nc) Manage Inventory\nd) Exit")
        choice = get_string(">>> ")
        print("-"*80)
        if choice == "A" or choice == "Borrow a book":
            Borrow_a_Book()

        if choice == "B" or choice == "Review borrowed books":
            while True:
                print("Would you like to review borrowed books for:\na) A specific member\nb) All members")
                choice = get_string(">>> ")
                print("-"*80)

                if choice == "A" or choice == "A specific member":
                    with open('Borrowed_Books.txt', 'r') as file:
                        names = []
                        numbers = []
                        for line in file:
                            line = line.strip().split(", ")
                            names.append(line[0].capitalize())
                            numbers.append(line[1].capitalize())
                    print("Enter the member name or number below")
                    choice = input(">>> ").capitalize()
                    while choice not in names and choice not in numbers:
                        print("Name or Number inputted is not logged")
                        choice = input(">>> ").capitalize()
                    logs, dates = Review_Borrowed_Books(choice)
                    for log in logs:
                        print(log)
                    print("Specified logs have been printed")
                    break

                if choice == "B" or choice == "All members":
                    logs, dates = Review_Borrowed_Books("all")
                    for log in logs:
                        print(log)
                    print("Specified logs have been printed")
                    break

        if choice == "C" or choice == "Manage inventory":
            Manage_Inventory()
        if choice == "D" or choice == "exit":
            break
main()