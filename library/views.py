from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from .queries import *
# Create your views here.


def index(request):
    all_books = get_all_books()
    if request.method == 'POST':
        if 'lendBook_frm' in request.POST:
            bookIsbn = request.POST.get("bookIsbn")
            custFirstName = request.POST.get("custFirstName")
            custLastName = request.POST.get("custLastName")
            librarianFirstName = request.POST.get("librarianFirstName")
            librarianLastName = request.POST.get("librarianLastName")
            lend_book(bookIsbn, custFirstName, custLastName, librarianFirstName, librarianLastName)
        elif 'searchBook_frm' in request.POST:
            searchQuery = request.POST.get("searchQuery")
            all_books = search_book(searchQuery)

    context = {
        'all_books': all_books,
    }
    return render(request, 'library/index.html', context)

def librarian(request):
    if request.method == 'POST':
        if 'addCustomer_frm' in request.POST:
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            phoneNumber = request.POST.get("phoneNumber")
            birthDate = request.POST.get("birthDate")
            gender = request.POST.get("gender")
            create_customer(firstName=firstName, lastName=lastName, phoneNumber=phoneNumber, birthDate=birthDate, gender=gender)
        elif 'addBook_frm' in request.POST:
            authorFirstName = request.POST.get("authorFirstName")
            authorLastName = request.POST.get("authorLastName")
            isbn = request.POST.get("isbn")
            title = request.POST.get("title")
            cost = request.POST.get("cost")
            language = request.POST.get("language")
            bookPicture = request.POST.get("bookPicture")
            add_book(authorFirstName, authorLastName, isbn, title, cost, language, bookPicture)
        elif 'removeCustomer_frm' in request.POST:
            customerId = request.POST.get("custId")
            remove_customer(customerId)
        elif 'removeBook_frm' in request.POST:
            bookId = request.POST.get("bookId")
            remove_book(bookId)

    return render(request, "library/librarian.html")

def customer(request, customerId):
    if request.method == 'POST':
        if 'return_frm' in request.POST:
            rentedBookId = request.POST.get("RentedBookId")
            return_book(rentedBookId)
        if 'extend_frm' in request.POST:
            rentedBookId = request.POST.get("RentedBookId")
            extend_book(rentedBookId)

    rentedBooks = get_customer_rented_books(customerId)
    context = {
        'rented_books': rentedBooks
    }
    return render(request, "library/customer.html", context)

def createCustomer(request):
    return render(request, 'library/librarian.html')
