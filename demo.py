# s = 0
# e = 2
# data = []
# for i in range(1, 4):   
#     for j in range(s+i, e+i):
#         if (i, j) != (1, 1):
#             print(i, j)
        
#     s+=1
#     e+=1

# from datetime import datetime
# current_year = str(datetime.now().year)
# max_receipt_no = 'GK2025RC01'
                            


# try:
#         # Extract numeric part and increment
#         numeric_part = int(max_receipt_no[8:])  # Remove 'ST' prefix
#         receipt_no = f'GK{current_year}RC{numeric_part + 1}'
        
# except (ValueError, IndexError):
#         receipt_no = 'GK' + current_year + 'RC1'  # Fallback if format is wrong

# print(receipt_no)


# data = [0]
    

# if 1>2:
#     data[0] = 1
# elif 1<2:
#     data[0] =2



# Library Management System (OOP Based)

# class Book:
#     def __init__(self, book_id, title, author): 
#         self.book_id = book_id
#         self.title = title
#         self.author = author
#         self.is_issued = False

#     def __str__(self): 
#         status = "Issued" if self.is_issued else "Available"
#         return f"[{self.book_id}] {self.title} by {self.author} - {status}"


# class Member:
#     def __init__(self, member_id, name):  
#         self.member_id = member_id
#         self.name = name
#         self.issued_books = []

#     def __str__(self):
#         return f"Member ID: {self.member_id}, Name: {self.name}"


# class Library:
#     def __init__(self):  
#         self.books = []
#         self.members = []

#     def add_book(self, book_id, title, author):
#         # Check if book ID already exists
#         if self.find_book(book_id):
#             print(f"Book ID '{book_id}' already exists!\n")
#             return
        
#         new_book = Book(book_id, title, author)
#         self.books.append(new_book)
#         print(f"Book '{title}' added successfully!\n")

#     def register_member(self, member_id, name):
#         # Check if member ID already exists
#         if self.find_member(member_id):
#             print(f" Member ID '{member_id}' already exists!\n")
#             return
            
#         new_member = Member(member_id, name)
#         self.members.append(new_member)
#         print(f"Member '{name}' registered successfully!\n")

#     def issue_book(self, book_id, member_id):
#         book = self.find_book(book_id)
#         member = self.find_member(member_id)

#         if book and member:
#             if not book.is_issued:
#                 book.is_issued = True
#                 member.issued_books.append(book)
#                 print(f"'{book.title}' issued to {member.name}\n")
#             else:
#                 print("Book already issued!\n")
#         else:
#             print("Invalid Book ID or Member ID!\n")

#     def return_book(self, book_id, member_id):
#         book = self.find_book(book_id)
#         member = self.find_member(member_id)

#         if book and member:
#             if book in member.issued_books:
#                 book.is_issued = False
#                 member.issued_books.remove(book)
#                 print(f"'{book.title}' returned by {member.name}\n")
#             else:
#                 print("This book was not issued to this member!\n")
#         else:
#             print("Invalid Book ID or Member ID!\n")

#     def display_books(self):
#         print("\n Available Books:")
#         available = [book for book in self.books if not book.is_issued]
#         if available:
#             for book in available:
#                 print(book)
#         else:
#             print("No books available right now.")
#         print()

#     def display_members(self):
#         print("\n Registered Members:")
#         if self.members:
#             for member in self.members:
#                 print(member)
#                 if member.issued_books:
#                     print("Issued Books:")
#                     for book in member.issued_books:
#                         print(f"    - {book.title}")
#                 else:
#                     print("No books issued")
#                 print()
#         else:
#             print("No members registered yet.")
#         print()

#     # Helper functions
#     def find_book(self, book_id):
#         for book in self.books:
#             if book.book_id == book_id:
#                 return book
#         return None

#     def find_member(self, member_id):
#         for member in self.members:
#             if member.member_id == member_id:
#                 return member
#         return None

# # Main Program
# def main():
#     library = Library()
#     while True:
#         print("\n" + "="*40)
#         print("      Library Management System")
#         print("="*40)
#         print("1. Add new book")
#         print("2. Register new member")
#         print("3. Issue a book")
#         print("4. Return a book")
#         print("5. Display available books")
#         print("6. Display all members") 
#         print("7. Exit")
        
#         choice = input("\nEnter your choice (1-7): ")

#         if choice == '1':
#             book_id = input("Enter Book ID: ")
#             title = input("Enter Book Title: ")
#             author = input("Enter Author Name: ")
#             library.add_book(book_id, title, author)

#         elif choice == '2':
#             member_id = input("Enter Member ID: ")
#             name = input("Enter Member Name: ")
#             library.register_member(member_id, name)

#         elif choice == '3':
#             book_id = input("Enter Book ID to Issue: ")
#             member_id = input("Enter Member ID: ")
#             library.issue_book(book_id, member_id)

#         elif choice == '4':
#             book_id = input("Enter Book ID to Return: ")
#             member_id = input("Enter Member ID: ")
#             library.return_book(book_id, member_id)

#         elif choice == '5':
#             library.display_books()

#         elif choice == '6':
#             library.display_members()

#         elif choice == '7':
#             print("Exiting the system. Goodbye!")
#             break

#         else:
#             print("Invalid choice! Please enter 1-7.\n")


# # Run the program
# if __name__ == "__main__":  
#     main()  
    



print('Hello World')

s=0
e=2
c = float('22.00')
for i in range(1,2):
    for j in range(s+i, e+i):
        print(i,j)
        print(c+i)
    s+=1
    e+=1