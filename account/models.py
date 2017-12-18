from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        if not email:
        	raise ValueError("Users must have an email address")

        if not password:
        	raise ValueError("Users must have a password")
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
	'''Creating a custom user model where email is used instead of username'''
	email       	= models.EmailField(verbose_name='email address', max_length=255, unique=True)
	surname			= models.CharField(max_length=255)
	firstname		= models.CharField(max_length=255)
	active 			= models.BooleanField(default=True)
	staff 			= models.BooleanField(default=False) # a admin user; non super-user
	admin 			= models.BooleanField(default=False) # a superuser
	date_created	= models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] # Email & Password are required by default.
	objects = UserManager()

	def get_full_name(self):
		'''The user is identified by their email address'''
		full_name = self.surname +" "+self.firstname
		return full_name

	def get_short_name(self):
		'''The user is identified by their email address'''
		return self.firstname

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		return self.staff

	@property
	def is_admin(self):
		"Is the user a admin member?"
		return self.admin

	@property
	def is_active(self):
		"Is the user active?"
		return self.active


