from django.test import TestCase
from transactions.models import Client, Transaction

class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(clientname='Generous Bank', inn='0123456789', money=1000.06)
        Client.objects.create(clientname='Client1', inn='012345678912', money=200)

    def test_clientname_label(self):
        client=Client.objects.get(inn='0123456789')
        field_label = client._meta.get_field('clientname').verbose_name
        self.assertEquals(field_label,'clientname')

    def test_inn_label(self):
        client=Client.objects.get(inn='0123456789')
        field_label = client._meta.get_field('inn').verbose_name
        self.assertEquals(field_label,'inn')

    def test_object_name_is_clientname(self):
        client=Client.objects.get(inn='0123456789')
        expected_object_name = '%s' % (client.clientname)
        self.assertEquals(expected_object_name,str(client))

    def test_money_format(self):
        client=Client.objects.get(inn='0123456789')
        max_digits = client._meta.get_field('money').max_digits
        decimal_places = client._meta.get_field('money').decimal_places
        self.assertEquals(max_digits, 20)
        self.assertEquals(decimal_places, 2)


class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(clientname='Generous Bank', inn='0123456789', money=1000.06)
        Client.objects.create(clientname='Client1', inn='012345678912', money=200)
        Client.objects.create(clientname='Client2', inn='212345678912', money=300)
        Transaction.objects.create(sender=Client.objects.filter(clientname='Generous Bank')[0], payee='012345678912', amount=500.01)

    def test_clientname_label(self):
        tran=Transaction.objects.get(id=1)
        field_label = tran._meta.get_field('sender').verbose_name
        self.assertEquals(field_label,'sender')

    def test_object_name_is_clientname(self):
        tran=Transaction.objects.get(id=1)
        expected_object_name = '%s' % (tran.sender.clientname)
        self.assertEquals(expected_object_name,str(tran))