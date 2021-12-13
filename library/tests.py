from .models import Address, Book, Librarian, RentBook, Author, Customer
from django.test import TestCase
from .queries import *

# Create your tests here.
class BookTestCase(TestCase):
    def setUp(self):
        address = Address.objects.create(country="Germany", city="Heilbronn", state="Baden-Württemberg", zipCode="74072", street="Oststraße 33")
        Librarian.objects.create(firstName="John", lastName="Snow", userName="johnSnow", birthDate="2000-11-27", gender="male", password="JohnSnowTheGreat123", address=address)

    def test_add_book(self):
        add_book("TestAuthor1", "TestAuthor1", "518481912", "TestBook", "555", "English", "testpicture.jpeg")
        book = Book.objects.get(isbn="518481912")
        self.assertEqual(book.available, 1)

    def test_remove_book(self):
        add_book("TestAuthor1", "TestAuthor1", "518481912", "TestBook", "555", "English", "testpicture.jpeg")
        book = Book.objects.get(isbn="518481912")
        remove_book(book.id)
        with self.assertRaises(Book.DoesNotExist): 
            Book.objects.get(isbn="518481912")
    
    def test_get_all_books(self):
        add_book("TestAuthor1", "TestAuthor1", "518481912", "TestBook", "555", "English", "testpicture.jpeg")
        add_book("TestAuthor1", "TestAuthor1", "518481913", "TestBook2", "555", "English", "testpicture2.jpeg")
        add_book("TestAuthor1", "TestAuthor1", "518481914", "TestBook3", "555", "English", "testpicture3.jpeg")
        books = get_all_books()
        self.assertEqual(books.count(), 3)

class CustomerTestCase(TestCase):
    def test_add_customer(self):
        customer = create_customer("Antoan", "Atanasov", "01766444321", "1997-07-29", "male")
        self.assertEqual(customer.firstName, "Antoan")

    def test_remove_customer(self):
        customer = create_customer("Antoan", "Atanasov", "01766444321", "1997-07-29", "male")
        self.assertEqual(customer.firstName, "Antoan")
        remove_customer(customer.id)
        with self.assertRaises(Customer.DoesNotExist): 
            Customer.objects.get(pk=customer.id)

    def test_get_customer_rented_books(self):
        address = Address.objects.create(country="Germany", city="Heilbronn", state="Baden-Württemberg", zipCode="74072", street="Oststraße 33")
        Librarian.objects.create(firstName="John", lastName="Snow", userName="johnSnow", birthDate="2000-11-27", gender="male", password="JohnSnowTheGreat123", address=address)

        add_book("TestAuthor1", "TestAuthor1", "518481912", "TestBook", "555", "English", "testpicture.jpeg")
        add_book("TestAuthor1", "TestAuthor1", "518481913", "TestBook2", "555", "English", "testpicture2.jpeg")
        books = get_all_books()
        self.assertEqual(books.count(), 2)
        customer = create_customer("Antoan", "Atanasov", "01766444321", "1997-07-29", "male")
        self.assertEqual(customer.firstName, "Antoan")

        lend_book("518481912", "Antoan", "Atanasov", "John", "Snow")
        lend_book("518481913", "Antoan", "Atanasov", "John", "Snow")
        rentedBooks = get_customer_rented_books(customer.id)
        self.assertEqual(rentedBooks.count(), 2)

    def test_return_rented_book(self):
        address = Address.objects.create(country="Germany", city="Heilbronn", state="Baden-Württemberg", zipCode="74072", street="Oststraße 33")
        Librarian.objects.create(firstName="John", lastName="Snow", userName="johnSnow", birthDate="2000-11-27", gender="male", password="JohnSnowTheGreat123", address=address)

        add_book("TestAuthor1", "TestAuthor1", "518481912", "TestBook", "555", "English", "testpicture.jpeg")
        add_book("TestAuthor1", "TestAuthor1", "518481913", "TestBook2", "555", "English", "testpicture2.jpeg")
        books = get_all_books()
        self.assertEqual(books.count(), 2)
        customer = create_customer("Antoan", "Atanasov", "01766444321", "1997-07-29", "male")
        self.assertEqual(customer.firstName, "Antoan")

        lend_book("518481912", "Antoan", "Atanasov", "John", "Snow")
        lend_book("518481913", "Antoan", "Atanasov", "John", "Snow")
        rentedBooks = get_customer_rented_books(customer.id)
        return_book(rentedBooks[1].id)
        self.assertEqual(rentedBooks.count(), 1)        

    def test_extend_rented_book(self):
        address = Address.objects.create(country="Germany", city="Heilbronn", state="Baden-Württemberg", zipCode="74072", street="Oststraße 33")
        Librarian.objects.create(firstName="John", lastName="Snow", userName="johnSnow", birthDate="2000-11-27", gender="male", password="JohnSnowTheGreat123", address=address)

        add_book("TestAuthor1", "TestAuthor1", "518481912", "TestBook", "555", "English", "testpicture.jpeg")
        add_book("TestAuthor1", "TestAuthor1", "518481913", "TestBook2", "555", "English", "testpicture2.jpeg")
        books = get_all_books()
        self.assertEqual(books.count(), 2)
        customer = create_customer("Antoan", "Atanasov", "01766444321", "1997-07-29", "male")
        self.assertEqual(customer.firstName, "Antoan")

        lend_book("518481912", "Antoan", "Atanasov", "John", "Snow")
        lend_book("518481913", "Antoan", "Atanasov", "John", "Snow")
        rentedBooks = get_customer_rented_books(customer.id)
        oldDate = rentedBooks[0].returnDate
        extend_book(rentedBooks[0].id)
        self.assertEqual(rentedBooks[0].returnDate, oldDate + timedelta(days=14)) 
        