from useful_functions import *
from datetime import datetime

'''BORROW A BOOK: MISSING NUMBER MAX
   Review_Borrowed_Books(): when is the due date
'''

def book_validator() -> str:
    # forms an array of book titles and ensures the title to be borrowed exists in it
    with open("book_inventory.txt", "r") as file:
        books = []
        for line in file:
            line = line.split(", ")
            books.append(line[0].capitalize())
    book = input("Book name: ")
    while book not in books:
        book = input("Book name: ")
    return book


def Review_Borrowed_Books():
    print("underconstruction, turn back")

def Borrow_a_Book():       
    # Get a name that is at least 1 character long and at most 20 characters
    name = get_string("Full Name: ")
    while 20 <= len(name):
        name = get_string("Full Name: ")

    # Get a membership Number that is only 6 digits in length
    memNo = get_positive_integer("Membership Number: ")
    while len(str(memNo)) != 6:
        memNo = get_positive_integer("Membership Number: ")

    # forms an array of book titles and ensures the title to be borrowed exists in it
    book = book_validator()

    # update inventory
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

    # record of borrowing
    print("Book Borrow Recorded!")
    formatted_datetime = datetime.now().strftime("%d/%m/%Y")
    with open('Borrowed_Books.txt', 'a') as file:
        print(f"{name}, {memNo}, {book}, {formatted_datetime}", file=file)

def Manage_Inventory():
    while True:
        print("-"*80)
        print("a) Add a new book (add all required information about the book title,author name, total copies available, and copies borrowed")
        print("b) Remove a book from the inventory.")
        print("c) Update the total copies available or copies borrowed for a book.")
        print("d) Return to the main menu.")
        choice = get_string(">>> ")
        if choice == "A" or choice == "Add a new book":
            bookName = get_string("Book Name: ")
            authorName = get_string("Author Name: ")
            copiesAvailable = get_positive_integer("Copies Available: ")
            copiesBorrowed = get_positive_integer("Copies Borrowed: ")
            with open("book_inventory.txt", "a") as file:
                print(f"\n{bookName}, {authorName}, {copiesAvailable}, {copiesBorrowed}", file=file)
            print("Book Added!")
                    
        if choice == "B" or choice == "Remove a book":
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

def main():
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
            Review_Borrowed_Books()
        if choice == "C" or choice == "Manage inventory":
            Manage_Inventory()
        if choice == "D" or choice == "exit":
            break
main()