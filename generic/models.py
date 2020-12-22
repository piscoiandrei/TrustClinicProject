from django.db import models


class FooterData(models.Model):
    class Meta:
        verbose_name = 'Footer Data'
        verbose_name_plural = 'Footer Data'

    # different phone numbers will be separated by ','
    phone = models.CharField(max_length=2000)
    creator_link = models.URLField(max_length=127)
    company_email = models.EmailField()

    def __str__(self):
        return 'Footer Data'

