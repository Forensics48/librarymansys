from django.db import models
import datetime
from django.db.models.aggregates import Count

# Create your models here.
class Customer(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    birthDate = models.DateField(default=datetime.date.today)
    gender = models.CharField(max_length=255)
    
class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

class Librarian(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    birthDate = models.DateField(default=datetime.date.today)
    gender = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Author(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    cost = models.IntegerField()
    available = models.IntegerField(default=1)
    language = models.CharField(max_length=255)
    bookPicture = models.CharField(max_length=255, default="")

class RentBook(models.Model):
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    returnDate = models.DateField(default=datetime.date.today)