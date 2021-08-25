from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .service import Pagination
from .models import Client, Transaction
from .serializers import GetClientSerializer, ClientSerializer, TransactionSerializer
from decimal import *
from rest_framework.renderers import JSONRenderer


class ClientsListView(generics.ListAPIView):
    """List of clients"""
    queryset = Client.objects.all().order_by('clientname')
    serializer_class = GetClientSerializer
    pagination_class = Pagination


def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


class ClientCreateView(generics.CreateAPIView):
    """Create new client"""
    serializer_class = ClientSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        d = dict(request.data)
        inn = d['inn'][0]
        money = d['money'][0]
        if inn.isdigit() and (len(inn) == 10 or len(inn) == 12):
            if is_digit(money)==False or float(money)<0:
                return Response({"message": "Please check client money. It should it should be non-negative number."})
            else:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please check client inn. It should consist of 10 or 12 digits only."})


class TransactionsListView(generics.ListAPIView):
    """List of payments"""
    queryset = Transaction.objects.all().order_by('createdAt')
    serializer_class = TransactionSerializer
    pagination_class = Pagination


class TransactionCreateView(generics.CreateAPIView):
    """Make a payment"""
    serializer_class = TransactionSerializer

    def create(self, request):
        data=request.data
        d=dict(data)
        #Check enough money
        sender=Client.objects.filter(inn=d['sender'][0])[0]
        if is_digit(d['amount'][0]):
            if float(d['amount'][0]) > sender.money:
                return Response({"message": "Not enough money"})
            else:
                payeelist = d['payee'][0].split(', ')
                divided_amount = float(d['amount'][0]) / len(payeelist)

                clients_inn_list=[]
                clients_list=Client.objects.all()
                for i in clients_list:
                        clients_inn_list.append(i.inn)

                for p in payeelist:
                    if p not in clients_inn_list:
                        return Response({"message": "Sorry, Payee with this inn: '{}' is not in database".format(p)})
                    if p == sender.inn:
                        return Response({"message": "Sorry, Payee with this inn: '{}' is a sender".format(p)})

                for p in payeelist:
                    if p in clients_inn_list:
                            new_dict={}
                            new_dict['sender'] = sender.inn
                            new_dict['payee'] = p
                            new_dict['amount'] = divided_amount
                            #Increase Payee money
                            payee = Client.objects.filter(inn=p)[0]
                            payee.money += Decimal(divided_amount)
                            payee.save()
                            serializer = self.serializer_class(data=new_dict)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()
                #Decrease Sender money
                sender.money -= Decimal(d['amount'][0])
                sender.save()
                return Response({"message": "Success! {} transaction(s) created successfully!".format(len(payeelist))},
                                            status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please enter a valid amount of money in 'Amount' field"})


def hello(self):
    return JsonResponse({'Description':"Simple REST API allows to create clients and send payments between clients",

'USAGE. endpoint /createclient/': 'Post form or JSON with client detail information',

'/clients/': 'GET clients list',
'/pay/': 'Post form or JSON with new transaction(s) - send payment from one client to enother (or others). Example: 0987654321, 1234567890,... ',
'/transactions/': 'GET transactions list',
})