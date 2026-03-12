from django.core.management.base import BaseCommand
from newapp.models import Department, Position, SuperAdmin
from newapp.serializers import DepartmentSerializer, PositionSerializer
from django.contrib.auth.models import User
from getpass import getpass

department_data = {
    "name": "SuperAdmin",
    "code": "SA",
    "type": "Administrative",
    "description": "Handle all management and power of the college.",
    "programs": 0,
    "status": True
}

position_data = {
    "role": "Superadmin",
    "type": "Non-Teaching",
    "responsibility": "Handle all Management.",
    "salary": None,
    "status": True,
    "rank": 1,
}

class Command(BaseCommand):
    help = "Create the SuperAdmin"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("SuperAdmin Setup Started!"))
        self.create_department()
        self.create_position()
        self.create_superadmin()

    def create_department(self):
        self.stdout.write(self.style.WARNING("Department Setup Started!"))
        
        department, created = Department.objects.get_or_create(name=department_data["name"], defaults=department_data)
        
        if created:
            self.stdout.write(self.style.SUCCESS("Department Created!"))
        else:
            self.stdout.write(self.style.WARNING("Department Already Exists!"))

        self.dept_id = department.id

    def create_position(self):
        self.stdout.write(self.style.WARNING("Position Setup Started!"))
        position_name = input("Position Name: ")
        position_data["name"] = position_name
        position, created = Position.objects.get_or_create(name=position_name, defaults=position_data)

        if created:
            self.stdout.write(self.style.SUCCESS("Position Created!"))
        else:
            self.stdout.write(self.style.WARNING("Position Already Exists!"))

        self.pos_id = position.id

    def create_superadmin(self):
        department = Department.objects.get(id=self.dept_id)
        position = Position.objects.get(id=self.pos_id)

        name = str(input("Name: "))
        while name == None or name == '':
            self.stdout.write(self.style.ERROR("Name is Required!"))
            name = str(input("Name: "))
            
        last_name = str(input("Last Name: "))
        while last_name == None or last_name == '':
            self.stdout.write(self.style.ERROR("Last Name is Required!"))
            last_name = str(input("Last Name: "))
            
        username = str(input("Username: "))
        while username == None or username == '':
            self.stdout.write(self.style.ERROR("Username is Required!"))
            username = str(input("Username: "))
            
        password = str(getpass("Password (Hide): "))
        while password == None or password == '':
            self.stdout.write(self.style.ERROR("Password is Required!"))
            password = str(input("Password (Hide): "))

        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            self.stdout.write(self.style.WARNING("User Already Exists! Using Existing User."))
            user = existing_user
            
        else:
            user = User.objects.create_user(
            username=username,
            password=password,
            first_name=name,
            last_name=last_name,
            )
            
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS("Django User Created!"))

        superadmin, created = SuperAdmin.objects.get_or_create(
            user=user,
            defaults={
                "username": username,
                "password": password,
                "name": name,
                "last_name": last_name,
                "department": department,
                "position": position,
                }
            )

        if created:
            self.stdout.write(self.style.SUCCESS(f"SuperAdmin Created with ID - {superadmin.college_id}!"))
        else:
            self.stdout.write(self.style.WARNING("SuperAdmin Already Exists!"))

        return self.stdout.write(self.style.SUCCESS("SuperAdmin Created Successfully with all Setup!"))