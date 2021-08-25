from django.test import TestCase
from transactions.models import Client, Transaction
from transactions.views import ClientsListView, ClientCreateView, TransactionsListView, TransactionCreateView

class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Client.objects.create(clientname='Generous Bank', inn='0123456789', money=1000.06)
        Client.objects.create(clientname='Client1', inn='012345678912', money=200)
        Client.objects.create(clientname='Client2', inn='212345678912', money=300)


    def test_clients_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000/clients/')
        self.assertEqual(response.status_code, 200)

    def test_transactions_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000/transactions/')
        self.assertEqual(response.status_code, 200)

    def test_check_valid_inn(self):
        clients = Client.objects.all()
        for i in clients:
            self.assertTrue(i.inn.isdigit())
            self.assertTrue(len(i.inn) in [10, 12])

    def test_check_bad_response(self):
        clients = Client.objects.all()
        for i in clients:
            self.assertTrue(i.inn.isdigit())
            self.assertTrue(len(i.inn) in [10, 12])


