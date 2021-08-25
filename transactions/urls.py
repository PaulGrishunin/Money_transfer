from django.conf import settings
from django.urls import path
from .views import ClientsListView, ClientCreateView, TransactionsListView, TransactionCreateView

app_name = 'transactions'

urlpatterns = [

    path('clients/', ClientsListView.as_view(), name='clients_list'),                #Get all clients with detail from database
    path('createclient/', ClientCreateView.as_view(), name='client_create'),         #Create new client

    path('transactions/', TransactionsListView.as_view(), name='transactions_list'), #Get list of all payment transactions with details
    path('pay/', TransactionCreateView.as_view(), name='transaction_create'),        #Create new transaction (payment)

]
