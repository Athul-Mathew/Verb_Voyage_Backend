from django.db import models


from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class UserAccountManager(BaseUserManager):
    
    def _create_user(self,email,password,**extra_fields):
       if not email:
            raise ValueError('Your have not provided a valid e-mail address')
       
       email=self.normalize_email(email)
       user=self.model(email=email,**extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user
    

    def create_user(self, email=None, password=None, **extra_fields):
      
        return self._create_user(email, password, **extra_fields)
        
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    def update_user_status(self, user, is_online):
        user.is_online = is_online
        user.save()



    

        

    

class UserAccount(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255,default="Unnamed")
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False) 
    objects = UserAccountManager()
    remaining_subscription_days = models.IntegerField(default=0)

   



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name
    def __str__(self):
        return self.email
    
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None