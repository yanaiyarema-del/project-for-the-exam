from django.urls import path
from .views import (
    book_list_view, add_book_view, edit_book_view, delete_book_view, 
    create_offer_view, received_offers_view, accept_offer_view, reject_offer_view,
    sent_offers_view, book_detail_view
)

urlpatterns = [
    path('', book_list_view, name='book_list'),
    path('add/', add_book_view, name='add_book'),
    path('<int:pk>/edit/', edit_book_view, name='edit_book'),
    path('<int:pk>/delete/', delete_book_view, name='delete_book'),
    path('offers/create/', create_offer_view, name='create_offer'),
    path('offers/received/', received_offers_view, name='offers_received'),
    path('offers/<int:pk>/accept/', accept_offer_view, name='accept_offer'),
    path('offers/<int:pk>/reject/', reject_offer_view, name='reject_offer'),
    path('offers/sent/', sent_offers_view, name='offers_sent'),
    path('<int:pk>/detail/', book_detail_view, name='book_detail'),
]



