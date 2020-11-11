from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User Must Have Email Address!!")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    class Meta:
        db_table = "users"


class Interest(models.Model):
    subject = models.CharField(max_length=100)

    class Meta:
        db_table = 'Interests'


class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pictures/avatar/')

    class Meta:
        db_table = 'avatars'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, default="Hello")
    birthday = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'users_profile'


class OpeningMessage(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_by_users = models.ManyToManyField(User, default=None, blank=True, related_name='viewed_by')

    class Meta:
        db_table = "opening_message"