from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import DoctorProfile
from datetime import time

start_hour = time(hour=9, minute=0, second=0, microsecond=0)
end_hour = time(hour=17, minute=0, second=0, microsecond=0)

User = get_user_model()


class DoctorWorkingHours(models.Model):
    class Meta:
        verbose_name = 'Doctor Working Hours'
        verbose_name_plural = 'Doctor Working Hours'

    consultation_interval = models.SmallIntegerField(default=15, validators=[
        MinValueValidator(10), MaxValueValidator(55)])
    monday_start = models.TimeField(blank=True, null=True, default=start_hour)
    monday_end = models.TimeField(blank=True, null=True, default=end_hour)
    tuesday_start = models.TimeField(blank=True, null=True, default=start_hour)
    tuesday_end = models.TimeField(blank=True, null=True, default=end_hour)
    wednesday_start = models.TimeField(blank=True, null=True,
                                       default=start_hour)
    wednesday_end = models.TimeField(blank=True, null=True, default=end_hour)
    thursday_start = models.TimeField(blank=True, null=True, default=start_hour)
    thursday_end = models.TimeField(blank=True, null=True, default=end_hour)
    friday_start = models.TimeField(blank=True, null=True, default=start_hour)
    friday_end = models.TimeField(blank=True, null=True, default=end_hour)
    saturday_start = models.TimeField(blank=True, null=True, default=start_hour)
    saturday_end = models.TimeField(blank=True, null=True, default=end_hour)
    sunday_start = models.TimeField(blank=True, null=True, default=start_hour)
    sunday_end = models.TimeField(blank=True, null=True, default=end_hour)

    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.doctor_profile.user.full_name


@receiver(post_save, sender=DoctorProfile,
          dispatch_uid="create_doctor_schedule")
def create_doctor_schedule(sender, instance, **kwargs):
    DoctorWorkingHours.objects.create(doctor_profile=instance)


class Appointment(models.Model):
    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,
                                       related_name="doctors")
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                               null=True,
                               related_name="clients")
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.client.full_name + ' -> ' + self.doctor_profile.user.full_name
