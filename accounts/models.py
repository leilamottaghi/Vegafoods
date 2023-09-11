from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='نام')
    national_id = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تلفن')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = models.DateField(verbose_name='تاریخ تولد',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربری'


    def __str__(self):
        return self.name




class UserAddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    address = models.CharField(max_length=255, verbose_name="آدرس ")
    city = models.CharField(max_length=100, verbose_name="شهر")
    state = models.CharField(max_length=100, verbose_name="استان")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    def __str__(self):
        return f"{self.user.username}'s Address"

    class Meta:
        verbose_name = "آدرس کاربر"
        verbose_name_plural = "آدرس‌های کاربران"




