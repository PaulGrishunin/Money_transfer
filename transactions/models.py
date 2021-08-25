from django.db import models

class Client(models.Model):
    inn = models.CharField(max_length=12, unique=True, primary_key=True)
    clientname = models.CharField("clientname", max_length=255)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=20, null=True)
    address =  models.TextField(blank=True, null=True)
    money = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.clientname


class Transaction(models.Model):
    sender = models.ForeignKey(Client, on_delete=models.CASCADE)
    payee = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    createdAt = models.DateTimeField("Created datetime", auto_now_add=True)

    def __str__(self):
        return self.sender.clientname