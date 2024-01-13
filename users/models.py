from django.db import models
from django.contrib.auth.models import  AbstractUser
from .manage import UserManager

class User(AbstractUser):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255, unique=True)
    password=models.CharField(max_length=255)
    mobile=models.CharField(max_length=10,default="")
    otp=models.BooleanField(default=False)
    username = ""

    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = UserManager()

class Challenges(models.Model):
    problemstatement = models.TextField()
    sample_input_1 = models.TextField()
    sample_input_2 = models.TextField()
    image = models.ImageField( null=True, blank=True)
    sample_output_1 = models.TextField()
    sample_output_2 = models.TextField()
    explanations = models.TextField()

    class Stack(models.TextChoices):
        front = "1", "Frontend"
        back = "2", "Backtend"
        fstack = "3", "FullStack"
        machine = "4", "AI/ML"
        danylasis = "5", "Data Analyst"
        dscience = "6", "Data Science"
        
    class Language(models.TextChoices):
        pyt = "1", "Python" 
        java = "2", "Java"
        cpp = "3", "CPP"
        # AI/Ml = "4", ""
        # dataanalysis= "5", "dataanalysi"
        # datascinece = "6", "datascinece"
    
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.pyt)
    stack = models.CharField(max_length=20, choices=Stack.choices)
          
    class Level(models.TextChoices):
        easy = "Easy", "Easy"
        medium = "Medium","Mediun"
        hard  = "Hard","Hard"
        
    class Rating(models.TextChoices):
        one = "1","1"
        two = "2","2"
        three = "3","3"
        four = "4", "4"
        five = "5","5"
        
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.easy)
    rating = models.CharField(max_length=10, choices=Rating.choices, default=Rating.one)
        
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField() 
    writer = models.CharField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return self.title
    
from django.db import models
import uuid


class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productname=models.CharField(max_length=500)
    productid=models.CharField(unique=True,max_length=100)
    productdesc=models.CharField(max_length=500)




