from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from . import validators


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def get_full_name(self):
        return self.name

    class Meta:
        db_table = "users"


class Interest(models.Model):
    subject = models.CharField(max_length=100)

    def __str__(self):
        return '%d: %s' % (self.id, self.subject)

    class Meta:
        db_table = 'interests'


class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pictures/avatar/')

    class Meta:
        db_table = 'avatars'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, default=None, null=True)
    birthday = models.DateField(default=None, null=True, validators=[validators.birth_validation])
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, default=None, null=True)
    interests = models.ManyToManyField(Interest, default=None, blank=True, related_name='user_interests')

    class Meta:
        db_table = 'user_profiles'


class OpeningMessage(models.Model):

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    message = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_by_users = models.ManyToManyField(User, default=None, blank=True, related_name='viewed_by')
    categories = models.ManyToManyField(Interest, default=None, blank=True)
    max_number_of_members = models.IntegerField(default=2, blank=True)
    status = models.CharField(max_length=20, default=ACTIVE)

    class Meta:
        db_table = "opening_messages"


class RequestModel(models.Model):

    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    source = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='req_from')
    target = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='req_to')
    opening_message = models.ForeignKey(to=OpeningMessage, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, default=PENDING)
    message = models.CharField(max_length=255)

    class Meta:
        unique_together = ('source', 'target', 'opening_message')
        db_table = 'requests'
