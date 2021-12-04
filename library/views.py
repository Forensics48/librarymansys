from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from .models import Book, Librarian, RentBook, Author, Customer
import logging
from datetime import datetime, timedelta


# Create your views here.


def index(request):
    all_books = Book.objects.filter(available__gt=0)

    if request.method == 'POST':
        if 'lendBook_frm' in request.POST:
            bookIsbn = request.POST.get("bookIsbn")
            custFirstName = request.POST.get("custFirstName")
            custLastName = request.POST.get("custLastName")
            librarianFirstName = request.POST.get("librarianFirstName")
            librarianLastName = request.POST.get("librarianLastName")
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
        elif 'searchBook_frm' in request.POST:
            searchQuery = request.POST.get("searchQuery")
            all_books = Book.objects.filter(title__contains=searchQuery)

    context = {
        'all_books': all_books,
    }
    return render(request, 'library/index.html', context)


def bookDetail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request,  "library/detail.html", {'book': book})


def librarian(request):
    if request.method == 'POST':
        if 'addCustomer_frm' in request.POST:
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            phoneNumber = request.POST.get("phoneNumber")
            birthDate = request.POST.get("birthDate")
            gender = request.POST.get("gender")
            Customer.objects.create(firstName=firstName, lastName=lastName, phoneNumber=phoneNumber, birthDate=birthDate, gender=gender)
        elif 'addBook_frm' in request.POST:
            authorFirstName = request.POST.get("authorFirstName")
            authorLastName = request.POST.get("authorLastName")
            if(Author.objects.filter(firstName=authorFirstName, lastName=authorLastName)).exists():
                author = Author.objects.get(firstName=authorFirstName, lastName=authorLastName)
            else:
                author = Author.objects.create(firstName=authorFirstName, lastName=authorLastName)
            isbn = request.POST.get("isbn")
            title = request.POST.get("title")
            cost = request.POST.get("cost")
            language = request.POST.get("language")
            bookPicture = request.POST.get("bookPicture")
            bookPicture = "images\\" + bookPicture
            Book.objects.create(author=author, isbn=isbn, title=title, cost=cost, language=language, bookPicture=bookPicture)
        elif 'removeCustomer_frm' in request.POST:
            customerId = request.POST.get("custId")
            Customer.objects.filter(pk=customerId).delete()
        elif 'removeBook_frm' in request.POST:
            bookId = request.POST.get("bookId")
            book = get_object_or_404(Book, pk=bookId)
            book.delete()
            
    context = {

    }
    
    return render(request, "library/librarian.html", context)

def customer(request, customer_id):
    if request.method == 'POST':
        if 'return_frm' in request.POST:
            rentedBookId = request.POST.get("RentedBookId")
            rentedBook = RentBook.objects.get(pk=rentedBookId)
            book = rentedBook.book
            book.available += 1
            book.save()
            RentBook.objects.filter(pk=rentedBookId).delete()
        if 'extend_frm' in request.POST:
            rentedBookId = request.POST.get("RentedBookId")
            rentedBook = RentBook.objects.get(pk=rentedBookId)
            rentedBook.returnDate = rentedBook.returnDate + timedelta(days=14)
            rentedBook.save()

    rentedBooks = RentBook.objects.filter(customer__pk=customer_id)
    context = {
        'rented_books': rentedBooks
    }
    return render(request, "library/customer.html", context)

def createCustomer(request):
    context = {

    }
    return render(request, 'library/librarian.html', context)
