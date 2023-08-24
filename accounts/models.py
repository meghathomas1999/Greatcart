from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
# Create your models here.
class MyAccountmanager( BaseUserManager):
    def create_user(self, first_name, last_name,username, email, phone_number,password=None):
        if not email:
            raise ValueError("Email is mandatory ")
        if not username:
            raise ValueError("Username is required")
        user= self.model(
            email= self.normalize_email(email),
            username= username,
            first_name= first_name,
            last_name= last_name,
            password= password,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name,username, email, password):
        user= self.create_user(
            email= self.normalize_email(email),
            username= username,
            password= password,
            first_name= first_name,
            last_name= last_name,
            )
        user.is_admin= True
        user.is_active= True
        user.is_staff= True
        user.is_superadmin= True 
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    first_name= models.CharField(max_length=50)
    last_name= models.CharField( max_length=50)
    username= models.CharField( max_length=100, unique= True)
    email= models.EmailField(max_length=300, unique=True)
    phone_number=models.CharField(max_length=100)
    date_joined= models.DateTimeField(auto_now_add=True)
    last_login= models.DateTimeField(auto_now_add=True)
    is_admin= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    is_superadmin= models.BooleanField(default=False)
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['username','first_name','last_name']
    objects= MyAccountmanager()
    def __str__(self) :
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True

# Create your models here.
