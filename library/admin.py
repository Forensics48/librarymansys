from django.contrib import admin
from .models import Customer, Librarian, Author, Book, Address, RentBook

# Register your models here.
admin.site.register(Customer)
admin.site.register(Librarian)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Address)
admin.site.register(RentBook)