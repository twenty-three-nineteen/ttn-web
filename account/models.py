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
        db_table = 'all_interests'


class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pictures/avatar/')

    class Meta:
        db_table = 'avatars'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, default=None, null=True)
    birthday = models.DateField(default=None, null=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, default=None, null=True)
    interests = models.ManyToManyField(Interest, default=None, blank=True, related_name='user_interests')
    requests = models.ManyToManyField(to='self', symmetrical=False, through='RequestModel',
                                      through_fields=('req_from', 'req_to'), related_name='chat_requests')

    class Meta:
        db_table = 'users_profile'


class OpeningMessage(models.Model):
    message = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_by_users = models.ManyToManyField(User, default=None, blank=True, related_name='viewed_by')

    class Meta:
        db_table = "opening_message"


class RequestModel(models.Model):
    req_from = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='req_from')
    req_to = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='req_to')
    req_opening_message = models.ForeignKey(to=OpeningMessage, on_delete=models.CASCADE)
    req_state = models.CharField(max_length=20, default='pending')

    class Meta:
        unique_together = ('req_from', 'req_to', 'req_opening_message')
        db_table = 'Requests'
