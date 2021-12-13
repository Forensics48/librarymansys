from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #path('<book_id>', views.bookDetail,  name='bookDetail'),

    path('librarian/', views.librarian, name="librarian"),

    path('librarian/addCustomer/', views.librarian, name="addCustomer"),

    path('librarian/addBook', views.librarian, name="addBook"),

    path('customer/<customerId>', views.customer, name="customer")
]
