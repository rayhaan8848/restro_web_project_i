from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100, null=True)
    email=models.EmailField(null=True)
    message=models.TextField()
    def __str__(self):
        return self.name

class Category(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="category_images", null=True)
    def __str__(self):
            return self.title

class Momo(models.Model):
     name=models.CharField(max_length=200)
     category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="items")
     desc=models.TextField()
     price=models.DecimalField(max_digits=8,decimal_places=2)
     image=models.ImageField(upload_to="images")
     is_available=models.BooleanField(default=True)
     created_at=models.DateField(auto_now_add=True)
     update_at=models.DateTimeField(auto_now=True)
class Review(models.Model):
     name=models.CharField(max_length=200)
     message=models.TextField()
     order=models.CharField(max_length=200)
     rating=models.BigIntegerField()
     created_at=models.DateField(auto_now_add=True, null=True)
     update_at=models.DateTimeField(auto_now=True, null=True)