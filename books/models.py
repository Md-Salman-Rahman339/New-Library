from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    Name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)

    def __str__(self):
        return self.Name



class Book(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image = models.ImageField(upload_to='books/media/uploads', blank=True, null=True)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return f"comments by {self.user.username}"


class BorrowedBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return f"Borrow this: {self.book.title}"
    
        
    
