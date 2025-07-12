from django.db import models

# Create your models here.
class Student_add(models.Model):
    Student_rollno = models.CharField(max_length=30,unique=True)
    semester = models.CharField(max_length=30,default='I')
    Student_name = models.CharField(max_length=30)
    Father_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=30, null=False, unique=True)
    Address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)  # <-- default de diya
    state=models.CharField(max_length=50)
    Email = models.EmailField(null=False)
    course = models.CharField(max_length=50, null=False)  # Added max_length
    tenth_dmc = models.FileField(null=False, upload_to='upload/', blank=True)  # Fixed blank=True
    twelth = models.FileField(null=False, upload_to='upload/', blank=True)  # Fixed blank=True

    class Meta:
        db_table = 'student'

from django.db import models

class Student_percent(models.Model):
    Student_rollno = models.CharField(max_length=20, unique=True)
    percentage = models.FloatField(null=True, blank=True)  # New field for percentage

class result(models.Model):
    Student_rollno = models.CharField(max_length=100,unique=True)
    course = models.CharField(max_length=50)
    one=models.CharField(max_length=20)
    two=models.CharField(max_length=20)
    three=models.CharField(max_length=20)
    four=models.CharField(max_length=20)
    five=models.CharField(max_length=20)
    six=models.CharField(max_length=20)
    seven=models.CharField(max_length=20)
    eight=models.CharField(max_length=20)
    nine=models.CharField(max_length=20)
    ten=models.CharField(max_length=20)
    eleven=models.CharField(max_length=20)
    twelve=models.CharField(max_length=20)
    thirteen=models.CharField(max_length=20)
    fourteen=models.CharField(max_length=20)
    fifteen=models.CharField(max_length=20)
    sixteen=models.CharField(max_length=20)
    seventeen=models.CharField(max_length=20)
    eighteen=models.CharField(max_length=20)
    nineteen=models.CharField(max_length=20)
    twenty=models.CharField(max_length=20)
    twenty_one=models.CharField(max_length=20)
    twenty_two=models.CharField(max_length=20)
    twenty_three=models.CharField(max_length=20)
    twenty_four=models.CharField(max_length=20)
    twenty_five=models.CharField(max_length=20)
    twenty_six=models.CharField(max_length=20)
    twenty_seven=models.CharField(max_length=20)
    twenty_eight=models.CharField(max_length=20)
    twenty_nine=models.CharField(max_length=20)
    thirty=models.CharField(max_length=20)
    thirty_one=models.CharField(max_length=20)
    thirty_two=models.CharField(max_length=20)
    thirty_three=models.CharField(max_length=20)
    thirty_four=models.CharField(max_length=20)
    thirty_five=models.CharField(max_length=20)
    thirty_six=models.CharField(max_length=20)
    thirty_seven=models.CharField(max_length=20)
    thirty_eight=models.CharField(max_length=20)
    thirty_nine=models.CharField(max_length=20)
    fourty=models.CharField(max_length=20)
    fourty_one=models.CharField(max_length=20)
    fourty_two=models.CharField(max_length=20)
    fourty_three=models.CharField(max_length=20)
    fourty_four=models.CharField(max_length=20)
    fourty_five=models.CharField(max_length=20)
    fourty_six=models.CharField(max_length=20)
    fourty_seven=models.CharField(max_length=20)
    fourty_eight=models.CharField(max_length=20)
    fourty_nine=models.CharField(max_length=20)
    fifty=models.CharField(max_length=20)
    fifty_one=models.CharField(max_length=20)
    fifty_two=models.CharField(max_length=20)
    fifty_three=models.CharField(max_length=20)
    fifty_four=models.CharField(max_length=20)
    fifty_five=models.CharField(max_length=20)
    fifty_six=models.CharField(max_length=20)
    fifty_seven=models.CharField(max_length=20)
    fifty_eight=models.CharField(max_length=20)
    fifty_nine=models.CharField(max_length=20)
    sixty=models.CharField(max_length=20)
    sixty_one=models.CharField(max_length=20)
    sixty_two=models.CharField(max_length=20)
    sixty_three=models.CharField(max_length=20)
    sixty_four=models.CharField(max_length=20)

class subject(models.Model):
    semester=models.CharField(max_length=200)
    course=models.CharField(max_length=200)
    I=models.CharField(max_length=200)
    II=models.CharField(max_length=200)
    III=models.CharField(max_length=200)
    IV=models.CharField(max_length=200)
    V=models.CharField(max_length=200)
    VI=models.CharField(max_length=200)
    VII=models.CharField(max_length=200)
    VIII=models.CharField(max_length=200)

