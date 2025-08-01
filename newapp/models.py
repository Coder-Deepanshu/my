from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    department=models.CharField(max_length=50)
    no_of_years = models.IntegerField()
    no_of_semesters = models.IntegerField()

    def __str__(self):
        return self.name

class Student(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    college_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    other_phone_no=models.CharField(max_length=15,null=True)
    occupation=models.CharField(max_length=50,null=True)
    income=models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=10)
    course = models.CharField(max_length=100)  # Changed to ForeignKey
    birthday = models.DateField()
    address = models.TextField()
    semester = models.IntegerField(default=1)
    year = models.IntegerField(default=1)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, blank=True, null=True,default='India')
    date_of_joining = models.DateField()
    tenth_percent = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_percent = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=10, choices=[
        ('General', 'General'),
        ('BC(A)', 'BC(A)'),
        ('BC(B)', 'BC(B)'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('Others', 'Others')
    ])

    # Nationality & Religion
    nationality = models.CharField(max_length=20, choices=[
        ('Indian', 'Indian'),
        ('NRI', 'NRI'),
        ('Other', 'Other')
    ])
    religion = models.CharField(max_length=20, choices=[
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Sikh', 'Sikh'),
        ('Christian', 'Christian'),
        ('Jain', 'Jain'),
        ('Buddhist', 'Buddhist'),
        ('Other', 'Other')
    ])

    # Identity Info
    adhar_no = models.BigIntegerField()
    pan_no = models.CharField(max_length=20,null=True)
    family_id=models.CharField(max_length=20,null=True)
    family_id_phone_no=models.CharField(max_length=15,null=True)

    # Marital Status
    martial_status = models.CharField(max_length=15, choices=[
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried')
    ], default='Unmarried')
    user_id=models.CharField(max_length=10)
    username=models.EmailField()
    password=models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.college_id})"

class Faculty(models.Model):
    # Basic Info
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    college_id=models.CharField(max_length=15,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    qualification=models.CharField(max_length=50)

    # Experience & Joining
    experience = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 5.5 years
    date_of_joining = models.DateField()

    # Contact Info
    phone = models.CharField(max_length=15)
    other_phone_no = models.CharField(max_length=15,null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    birthday = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10,null=True)
    country = models.CharField(max_length=30, choices=[
    ('India', 'India'),
    ('USA', 'USA'),
    ('UK', 'UK'),
    ('Canada', 'Canada'),
    ('Australia', 'Australia'),
    ('Germany', 'Germany'),
    ('France', 'France'),
    ('Japan', 'Japan'),
    ('China', 'China'),
    ('Other', 'Other')
])

    # Category
    category = models.CharField(max_length=10, choices=[
        ('Genral', 'General'),
        ('BC(A)', 'BC(A)'),
        ('BC(B)', 'BC(B)'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('Others', 'Others')
    ])

    # Nationality & Religion
    nationality = models.CharField(max_length=20, choices=[
        ('Indian', 'Indian'),
        ('NRI', 'NRI'),
        ('Other', 'Other')
    ])
    religion = models.CharField(max_length=20, choices=[
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Sikh', 'Sikh'),
        ('Christian', 'Christian'),
        ('Jain', 'Jain'),
        ('Buddhist', 'Buddhist'),
        ('Other', 'Other')
    ])

    # Identity Info
    adhar_no = models.BigIntegerField()
    pan_no = models.CharField(max_length=20)

    # Marital Status
    martial_status = models.CharField(max_length=15, choices=[
        ('married', 'Married'),
        ('unmarried', 'Unmarried')
    ], default='unmarried')
    user_id=models.CharField(max_length=50,null=True,)
    username=models.EmailField()
    password=models.CharField(max_length=15,null=True)



    def _str_(self):
        return self.name

class result(models.Model):
    Student_rollno = models.CharField(max_length=20,unique=True,null=False,default=1)
    course = models.CharField(max_length=50)
    one = models.CharField(max_length=20, blank=True, null=False,default=0)
    two = models.CharField(max_length=20, blank=True, null=True,default=0)
    three = models.CharField(max_length=20, blank=True, null=True,default=0)
    four = models.CharField(max_length=20, blank=True, null=True,default=0)
    five = models.CharField(max_length=20, blank=True, null=True,default=0)
    six = models.CharField(max_length=20, blank=True, null=True,default=0)
    seven = models.CharField(max_length=20, blank=True, null=True,default=0)
    eight = models.CharField(max_length=20, blank=True, null=True,default=0)
    nine = models.CharField(max_length=20, blank=True, null=True)
    ten = models.CharField(max_length=20, blank=True, null=True)
    eleven = models.CharField(max_length=20, blank=True, null=True)
    twelve = models.CharField(max_length=20, blank=True, null=True)
    thirteen = models.CharField(max_length=20, blank=True, null=True)
    fourteen = models.CharField(max_length=20, blank=True, null=True)
    fifteen = models.CharField(max_length=20, blank=True, null=True)
    sixteen = models.CharField(max_length=20, blank=True, null=True)
    seventeen = models.CharField(max_length=20, blank=True, null=True)
    eighteen = models.CharField(max_length=20, blank=True, null=True)
    nineteen = models.CharField(max_length=20, blank=True, null=True)
    twenty = models.CharField(max_length=20, blank=True, null=True)
    twenty_one = models.CharField(max_length=20, blank=True, null=True)
    twenty_two = models.CharField(max_length=20, blank=True, null=True)
    twenty_three = models.CharField(max_length=20, blank=True, null=True)
    twenty_four = models.CharField(max_length=20, blank=True, null=True)
    twenty_five = models.CharField(max_length=20, blank=True, null=True)
    twenty_six = models.CharField(max_length=20, blank=True, null=True)
    twenty_seven = models.CharField(max_length=20, blank=True, null=True)
    twenty_eight = models.CharField(max_length=20, blank=True, null=True)
    twenty_nine = models.CharField(max_length=20, blank=True, null=True)
    thirty = models.CharField(max_length=20, blank=True, null=True)
    thirty_one = models.CharField(max_length=20, blank=True, null=True)
    thirty_two = models.CharField(max_length=20, blank=True, null=True)
    thirty_three = models.CharField(max_length=20, blank=True, null=True)
    thirty_four = models.CharField(max_length=20, blank=True, null=True)
    thirty_five = models.CharField(max_length=20, blank=True, null=True)
    thirty_six = models.CharField(max_length=20, blank=True, null=True)
    thirty_seven = models.CharField(max_length=20, blank=True, null=True)
    thirty_eight = models.CharField(max_length=20, blank=True, null=True)
    thirty_nine = models.CharField(max_length=20, blank=True, null=True)
    fourty = models.CharField(max_length=20, blank=True, null=True)
    fourty_one = models.CharField(max_length=20, blank=True, null=True)
    fourty_two = models.CharField(max_length=20, blank=True, null=True)
    fourty_three = models.CharField(max_length=20, blank=True, null=True)
    fourty_four = models.CharField(max_length=20, blank=True, null=True)
    fourty_five = models.CharField(max_length=20, blank=True, null=True)
    fourty_six = models.CharField(max_length=20, blank=True, null=True)
    fourty_seven = models.CharField(max_length=20, blank=True, null=True)
    fourty_eight = models.CharField(max_length=20, blank=True, null=True)
    fourty_nine = models.CharField(max_length=20, blank=True, null=True)
    fifty = models.CharField(max_length=20, blank=True, null=True)
    fifty_one = models.CharField(max_length=20, blank=True, null=True)
    fifty_two = models.CharField(max_length=20, blank=True, null=True)
    fifty_three = models.CharField(max_length=20, blank=True, null=True)
    fifty_four = models.CharField(max_length=20, blank=True, null=True)
    fifty_five = models.CharField(max_length=20, blank=True, null=True)
    fifty_six = models.CharField(max_length=20, blank=True, null=True)
    fifty_seven = models.CharField(max_length=20, blank=True, null=True)
    fifty_eight = models.CharField(max_length=20, blank=True, null=True)
    fifty_nine = models.CharField(max_length=20, blank=True, null=True)
    sixty = models.CharField(max_length=20, blank=True, null=True)
    sixty_one = models.CharField(max_length=20, blank=True, null=True)
    sixty_two = models.CharField(max_length=20, blank=True, null=True)
    sixty_three = models.CharField(max_length=20, blank=True, null=True)
    sixty_four = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Marks for {self.Student_rollno}"

class subject(models.Model):
    semester = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    I = models.CharField(max_length=200)
    II = models.CharField(max_length=200)
    III = models.CharField(max_length=200)
    IV = models.CharField(max_length=200)
    V = models.CharField(max_length=200)
    VI = models.CharField(max_length=200)
    VII = models.CharField(max_length=200)
    VIII = models.CharField(max_length=200)

