from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from .validators import personal_id_validator, phone_validator
from django.db.models.signals import post_save
from django.dispatch import receiver
from generic.models import Specialization, Clinic


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={
            'unique':
                "A user with that email already exists.",
        },
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=27,
                             validators=[phone_validator],
                             help_text="International format is preffered")
    personal_id = models.CharField(
        max_length=128,
        unique=True,
        error_messages={
            'unique':
                "A user with that personal ID already exists.",
        },
        validators=[personal_id_validator],
        help_text="Do not include spaces",
        verbose_name="Personal ID")

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(
        default=True,
        verbose_name='active status',
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.'
    )
    is_connected = models.BooleanField(
        default=False,
        verbose_name='connection status',
        help_text='Describes the connection status of an user.'
    )
    is_client = models.BooleanField(
        default=False,
        verbose_name='client status',
        help_text='A non-staff user with the client status.'
    )
    is_operator = models.BooleanField(
        default=False,
        verbose_name='operator status',
        help_text='A non-staff user with the operator status.'
    )
    is_doctor = models.BooleanField(
        default=False,
        verbose_name='doctor status',
        help_text='A non-staff user with the doctor status.'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='staff status',
        help_text='An user without permissions, but can log into the admin site.'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='superuser status',
        help_text='An user with all permissions.'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"User(email={self.email}, first_name={self.first_name}, " \
               f"last_name={self.last_name}, phone={self.phone}, " \
               f"personal_id={self.personal_id}, " \
               f"date_joined={self.date_joined}, " \
               f"is_active={self.is_active}, " \
               f"is_connected={self.is_connected}, " \
               f"is_client={self.is_client}, " \
               f"is_operator={self.is_operator}, " \
               f"is_doctor={self.is_doctor}, " \
               f"is_staff={self.is_staff}, " \
               f"is_superuser={self.is_superuser})"

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


@receiver(post_save, sender=User, dispatch_uid="create_doctor_profile")
def create_doctor_profile(sender, instance, **kwargs):
    if instance.is_doctor:
        DoctorProfile.objects.get_or_create(user=instance)


class DoctorProfile(models.Model):
    description = models.CharField(max_length=4000, null=True, blank=True)
    picture = models.ImageField(help_text="1:1 aspect ratio required.",
                                null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True,
                               blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.SET_NULL,
                                       null=True, blank=True)

    def __str__(self):
        return self.user.full_name
