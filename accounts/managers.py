from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
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
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_client(self, email, password):
        """
        Creates and saves a client user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_client = True
        user.save(using=self._db)
        return user

    def create_operator(self, email, password):
        """
        Creates and saves an operator user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_operator = True
        user.save(using=self._db)
        return user

    def create_doctor(self, email, password):
        """
        Creates and saves a doctor user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_doctor = True
        user.save(using=self._db)
        return user

