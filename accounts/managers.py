import secrets
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    # Creates and saves a User with the given data.
    def create_user(self,
                    first_name=None,
                    last_name=None,
                    phone=None,
                    email=None,
                    password=None,
                    personal_id=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        if not personal_id:
            raise ValueError("Users must have a personal ID")

        user = self.model(
            email=self.normalize_email(email),
            personal_id=personal_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creates and saves a staff user with the given
    def create_staffuser(self,
                         first_name=None,
                         last_name=None,
                         phone=None,
                         email=None,
                         password=None,
                         personal_id=None):
        user = self.create_user(
            email=email,
            password=password,
            personal_id=personal_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    # Creates and saves a superuser with the given data
    def create_superuser(self,
                         email=None,
                         password=None,
                         personal_id=None):
        user = self.create_user(
            email=email,
            password=password,
            personal_id=str(secrets.randbits(32)),
            first_name='SUPER',
            last_name='USER',
            phone=str(secrets.randbits(32)),
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    # Creates and saves a client user with the given data.
    def create_client(self,
                      first_name=None,
                      last_name=None,
                      phone=None,
                      email=None,
                      password=None,
                      personal_id=None):
        user = self.create_user(
            email=email,
            password=password,
            personal_id=personal_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_client = True
        user.save(using=self._db)
        return user

    # Creates and saves an operator user with the given data.
    def create_operator(self,
                        first_name=None,
                        last_name=None,
                        phone=None,
                        email=None,
                        password=None,
                        personal_id=None):
        user = self.create_user(
            email=email,
            password=password,
            personal_id=personal_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_active = False
        user.is_operator = True
        user.save(using=self._db)
        return user

    # Creates and saves a doctor user with the given data.
    def create_doctor(self,
                      first_name=None,
                      last_name=None,
                      phone=None,
                      email=None,
                      password=None,
                      personal_id=None):
        user = self.create_user(
            email=email,
            password=password,
            personal_id=personal_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_doctor = True
        user.save(using=self._db)
        return user
