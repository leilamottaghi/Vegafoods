from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import *

# Create your models here.




def product_image_path(instance, filename):
    date_str = datetime.now().strftime('%Y/%m/%d')
    unique_filename = f'product_images/{date_str}/{filename}'
    return unique_filename

def category_image_path(instance, filename):
    date_str = datetime.now().strftime('%Y/%m/%d')
    unique_filename = f'category_images/{date_str}/{filename}'
    return unique_filename

def blog_image_path(instance, filename):
    date_str = datetime.now().strftime('%Y/%m/%d')
    unique_filename = f'blog_images/{date_str}/{filename}'
    return unique_filename



class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    

class CategoryModel(BaseModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=category_image_path)  

    def __str__(self):
        return self.title



class ProductModel(BaseModel):
    SIZE_CHOICES = (
        ('small', 'کوچک'),
        ('medium', 'متوسط'),
        ('large', 'بزرگ'),
        ('extra_large', 'خیلی بزرگ'),
    )
    title = models.CharField(max_length=200)
    price = models.IntegerField()  
    sale_price = models.IntegerField(null=True, blank=True) 
    description = models.TextField()
    quantity_available = models.IntegerField(default=0) 
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)  
    likes = models.IntegerField(default=0)  
    size = models.CharField(max_length=11, choices=SIZE_CHOICES)
    discount = models.IntegerField() 
    
    def __str__(self):
        return self.title



class ProductImageModel(BaseModel):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_path)


    def __str__(self):
        return f"Image for {self.product.title}"




class ContactModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject




class BlogModel(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=blog_image_path)

    def __str__(self):
        return self.title

    

class PurchaseInvoice(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.IntegerField()
    products = models.ManyToManyField(ProductModel)
    address = models.ForeignKey(UserAddressModel, on_delete=models.SET_NULL, null=True, verbose_name="آدرس انتخابی")
    def __str__(self):
        return f'Invoice for {self.user.username} on {self.created_date}'

