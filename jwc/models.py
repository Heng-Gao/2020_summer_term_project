from django.db import models


# Create your models here.
class user(models.Model):   #
    number = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=8)
    department = models.CharField(max_length=10)
    usertype = models.CharField(max_length=10)
    sex = models.CharField(max_length=2)
    age = models.CharField(max_length=2)  # m w
    pswd = models.CharField(max_length=8)


class courseinfo(models.Model):
    course_id = models.CharField(max_length=8)
    course_name = models.CharField(max_length=15)
    course_credit = models.CharField(max_length=2)
    course_status = models.CharField(max_length=8)
    teacher_number = models.CharField(max_length=8)
    teacher_name = models.CharField(max_length=8)
    student_number = models.CharField(max_length=8)
    student_name = models.CharField(max_length=8)
    student_score = models.CharField(max_length=3, null=True)


class term(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=8)


class opened_course(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    credit = models.CharField(max_length=2)
    name = models.CharField(max_length=15)
    teacher_name = models.CharField(max_length=8)
    teacher_number = models.CharField(max_length=8)




