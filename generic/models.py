from django.db import models
from .validators import phone_validator


class Specialization(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(help_text="1:1 aspect ratio required.",
                                null=True, blank=True)

    def __str__(self):
        return self.name


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    picture = models.ImageField(help_text="1:1 aspect ratio required.",
                                null=True, blank=True)
    phone = models.CharField(max_length=27,
                             validators=[phone_validator],
                             help_text="International format is preffered")
    start_time = models.CharField(max_length=31)
    end_time = models.CharField(max_length=31)
    extra_details = models.CharField(max_length=255,
                                     help_text="Relevant information abouct clinic's schedule")
    specializations = models.ManyToManyField(Specialization)

    def __str__(self):
        return self.name


class FooterData(models.Model):
    class Meta:
        verbose_name = 'Footer Data'
        verbose_name_plural = 'Footer Data'

    phone = models.CharField(max_length=27,
                             validators=[phone_validator],
                             help_text="International format is preffered")
    creator_link = models.URLField(max_length=127)
    company_email = models.EmailField()

    def __str__(self):
        return 'Footer Data'
