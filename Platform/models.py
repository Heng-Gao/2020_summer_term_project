from django.db import models


class User(models.Model):
    uId = models.CharField(primary_key=True, max_length=8)
    uPwd = models.CharField(max_length=8)
    uName = models.CharField(max_length=10)
    uAddr = models.CharField(max_length=20)
    uPhone = models.CharField(max_length=15)


class Restaurant(models.Model):
    rId = models.CharField(primary_key=True, max_length=8)
    rPwd = models.CharField(max_length=8)
    rName = models.CharField(max_length=15)
    rAddr = models.CharField(max_length=2)
    rTel = models.CharField(max_length=15)
    rEmail = models.EmailField(default='1000000@163.com')
    dysy = models.IntegerField()


class Administrator(models.Model):
    aId = models.CharField(primary_key=True, max_length=8)
    aPwd = models.CharField(max_length=8)
    aName = models.CharField(max_length=20)
    aGender = models.CharField(max_length=8)
    aAge = models.CharField(max_length=4)


class Menu(models.Model):
    mId = models.CharField(primary_key=True, max_length=8)
    mName = models.CharField(max_length=15)
    price = models.IntegerField()
    restaurantId = models.ForeignKey(to="Restaurant", on_delete=models.CASCADE)


class Order(models.Model):
    oId = models.AutoField(primary_key=True)
    oTime = models.CharField(max_length=30)
    number = models.IntegerField()
    money = models.IntegerField()
    status = models.CharField(max_length=10, blank=True)
    userId = models.ForeignKey(to="User", on_delete=models.CASCADE)
    menuId = models.ForeignKey(to="Menu", on_delete=models.CASCADE)
