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
    rEmail = models.EmailField()
    dysy = models.IntegerField(default=0)  # 月营业额
    image = models.ImageField(upload_to='image')


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
    image = models.ImageField(upload_to='image')  # 格式：'p'+mId+照片后缀,同图片文件名,比例统一为3：2
    infor = models.CharField(max_length=100)  # 菜品描述，不得多于100字（商户上传菜品时验证）


class Order(models.Model):
    oId = models.AutoField(primary_key=True)
    oTime = models.CharField(max_length=30)
    number = models.IntegerField()
    money = models.IntegerField()
    status = models.CharField(max_length=10, blank=True)
    userId = models.ForeignKey(to="User", on_delete=models.CASCADE)
    menuId = models.ForeignKey(to="Menu", on_delete=models.CASCADE)
    evaluation = models.CharField(max_length=3, null=True)#评价
    # realId=models.IntegerField()


class TmpRestaurant(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=15)
    t_addr = models.CharField(max_length=2)
    t_tel = models.CharField(max_length=15)
    t_email = models.EmailField()
    t_status = models.IntegerField(default=1)


class Activity(models.Model):
    name = models.CharField(max_length=15)
    start = models.CharField(max_length=15)
    end = models.CharField(max_length=15)
    discount = models.IntegerField()
    restaurantId = models.ForeignKey(to="Restaurant", on_delete=models.CASCADE)


# class orderId(models.Model):
#     first=models.IntegerField(primary_key=True)
#     id=models.IntegerField(default=1)