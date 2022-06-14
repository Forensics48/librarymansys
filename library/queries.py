from .models import Book, Librarian, RentBook, Author, Customer
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

# Returns all available books
def get_all_books():
    return Book.objects.filter(available__gt=0)

# Returns all customers rented books
def get_customer_rented_books(customerId):
    return RentBook.objects.filter(customer__pk=customerId)

# A librarian lends a book to a customer
def lend_book(bookIsbn, custFirstName, custLastName, librarianFirstName, librarianLastName):
    if(Customer.objects.filter(firstName=custFirstName, lastName=custLastName)).exists():
        customer = Customer.objects.get(firstName=custFirstName, lastName=custLastName)
        if(Librarian.objects.filter(firstName=librarianFirstName, lastName=librarianLastName)).exists():
            librarian = Librarian.objects.get(firstName=librarianFirstName, lastName=librarianLastName)
            if(Book.objects.filter(isbn=bookIsbn)).exists():
                book = Book.objects.get(isbn=bookIsbn)
                date = datetime.today() + timedelta(days=14)
                book.available -= 1
                book.save()
                RentBook.objects.create(librarian=librarian, customer=customer, book=book, returnDate=date)

# Returns book filtered with a specific query
def search_book(searchQuery):
    return Book.objects.filter(title__contains=searchQuery)

# A librarian creates a customer
def create_customer(firstName, lastName, phoneNumber, birthDate, gender):
    return Customer.objects.create(firstName=firstName, lastName=lastName, phoneNumber=phoneNumber, birthDate=birthDate, gender=gender)

# A customer returns a rented book
def return_book(rentedBookId):
    rentedBook = RentBook.objects.get(pk=rentedBookId)
    book = rentedBook.book
    book.available += 1
    book.save()
    RentBook.objects.filter(pk=rentedBookId).delete()

# Extends the lending period of a rented book
def extend_book(rentedBookId):
    rentedBook = RentBook.objects.get(pk=rentedBookId)
    rentedBook.returnDate = rentedBook.returnDate + timedelta(days=14)
    rentedBook.save()

# A librarian adds a book to the system
def add_book(authorFirstName, authorLastName, isbn, title, cost, language, bookPicture):
    if(Author.objects.filter(firstName=authorFirstName, lastName=authorLastName)).exists():
        author = Author.objects.get(firstName=authorFirstName, lastName=authorLastName)
    else:
        author = Author.objects.create(firstName=authorFirstName, lastName=authorLastName)
    bookPicture = "images\\" + bookPicture
    Book.objects.create(author=author, isbn=isbn, title=title, cost=cost, language=language, bookPicture=bookPicture)

# Remove a customer
def remove_customer(customerId):
    Customer.objects.filter(pk=customerId).delete()

# A librarian removes a book from the system
def remove_book(bookId):
    Book.objects.filter(pk=bookId).delete()
