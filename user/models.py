from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from alchol.models import Alchol

class MyUserManager(BaseUserManager):
    def create_user(self, email,nickname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,nickname='admin', password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            nickname = nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    
    
    nickname = models.CharField(max_length=20, unique=True)
    followings = models.ManyToManyField("self", symmetrical=False, through='Follow')
    bookmark = models.ManyToManyField("user.BookMark", default=[], through='BookMark')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
class Verify(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    verification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    following = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='follower')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='following')

class BookMark(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    alchol = models.ForeignKey('alchol.Alchol', on_delete=models.CASCADE, null=True)

