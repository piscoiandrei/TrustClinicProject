from django.db import models
from .validators import phone_validator


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
