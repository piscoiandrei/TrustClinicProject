import csv
import os
from secrets import randbits
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from accounts.models import DoctorProfile
from generic.models import Specialization, Clinic

lorem_clinic = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut et est mi. Quisque a eros eget leo gravida rhoncus. Duis vitae libero et neque rutrum dapibus.'
lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut et est mi. Quisque a eros eget leo gravida rhoncus. Duis vitae libero et neque rutrum dapibus. Integer ac massa pretium, gravida mauris vel, dictum nulla. Morbi dui lorem, congue et egestas a, pellentesque sed eros. Sed sed leo facilisis, euismod dolor ut, varius mi. Quisque turpis tortor, rutrum eget risus sit amet, pretium cursus tortor.'
User = get_user_model()

base_path = Path(__file__).resolve().parent.parent.parent.parent


def pid():
    return randbits(64)


def clients():
    print('clients')
    path = os.path.join(base_path, 'fixtures/clients.csv')
    with open(path) as file:
        fixture = csv.reader(file)
        for row in fixture:
            if row:
                print(row)
                User.objects.create_client(
                    email=row[0],
                    password=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    phone=row[4],
                    personal_id=pid()
                )


def operators():
    print('operators')
    path = os.path.join(base_path, 'fixtures/operators.csv')
    with open(path) as file:
        fixture = csv.reader(file)
        for row in fixture:
            if row:
                print(row)
                User.objects.create_operator(
                    email=row[0],
                    password=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    phone=row[4],
                    personal_id=pid()
                )


def doctors():
    print('doctors')
    path = os.path.join(base_path, 'fixtures/doctors.csv')
    with open(path) as file:
        fixture = csv.reader(file)
        for row in fixture:
            if row:
                print(row)
                User.objects.create_doctor(
                    email=row[0],
                    password=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    phone=row[4],
                    personal_id=pid()
                )


def specializations():
    print('specializations')
    path = os.path.join(base_path, 'fixtures/specializations.csv')
    with open(path) as file:
        fixture = csv.reader(file)
        for row in fixture:
            if row:
                print(row)
                Specialization.objects.create(name=row[0])


def clinics():
    print('clinics')
    path = os.path.join(base_path, 'fixtures/clinics.csv')
    with open(path) as file:
        fixture = csv.reader(file)
        for row in fixture:
            if row:
                print(row)
                Clinic.objects.create(
                    name=row[0],
                    description=lorem_clinic,
                    address=row[1],
                    phone=row[2],
                    start_time=row[3],
                    end_time=row[4],
                    extra_details=row[5],
                )


def doc_profiles():
    print('profiles')
    profiles = DoctorProfile.objects.all()
    for p in profiles:
        p.description = lorem
        p.save()


class Command(BaseCommand):
    def handle(self, **options):
        clients()
        operators()
        doctors()
        specializations()
        clinics()
        doc_profiles()
