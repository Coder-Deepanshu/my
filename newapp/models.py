from django.db import models

# Create your models here.
class Student_add(models.Model):
    Student_rollno = models.CharField(max_length=30, null=False, unique=True)
    Student_name = models.CharField(max_length=30)
    Father_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=30, null=False, unique=True)
    Address = models.CharField(max_length=100)
    Email = models.EmailField(null=False)
    course = models.CharField(max_length=50, null=False)  # Added max_length
    tenth_dmc = models.FileField(null=False, upload_to='upload/', blank=True)  # Fixed blank=True
    twelth = models.FileField(null=False, upload_to='upload/', blank=True)  # Fixed blank=True

    class Meta:
        db_table = 'student'

#  for BBA class
class BBA(models.Model):
    rollno = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    management = models.CharField(max_length=30, null=False)
    economics = models.CharField(max_length=30, null=False)
    accounting = models.CharField(max_length=30, null=False)
    mathematics = models.CharField(max_length=30, null=False)
    communication = models.CharField(max_length=30, null=False)
    computer = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'B.B.A'

#  for BCA class
class BCA(models.Model):
  rollno = models.CharField(max_length=30, null=False)
  name= models.CharField(max_length=30, null=False)
  C= models.CharField(max_length=30, null=False)
  Digital_Electronics= models.CharField(max_length=30, null=False)
  mathematics_I= models.CharField(max_length=30, null=False)
  communication= models.CharField(max_length=30, null=False)
  computer= models.CharField(max_length=30, null=False)
  class Meta:
     db_table='B.C.A'

# for Bsc
class B_Sc(models.Model):
  rollno = models.CharField(max_length=30, null=False)
  name= models.CharField(max_length=30, null=False)
  Physics= models.CharField(max_length=30, null=False)
  Chemistry= models.CharField(max_length=30, null=False)
  mathematics_I= models.CharField(max_length=30, null=False)
  communication= models.CharField(max_length=30, null=False)
  computer= models.CharField(max_length=30, null=False)
  Environmental_science=models.CharField(max_length=30,null=False)
  class Meta:
     db_table='B.Sc'

# for b.com
class B_Com(models.Model):
    rollno = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    Financial_Accounting = models.CharField(max_length=30, null=False)
    Business_management = models.CharField(max_length=30, null=False)
    mathematics = models.CharField(max_length=30, null=False)
    communication = models.CharField(max_length=30, null=False)
    environmental_studies = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'B.Com'

# for b.a
class B_A(models.Model):
    rollno = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    history = models.CharField(max_length=30, null=False)
    political_science = models.CharField(max_length=30, null=False)
    sociology = models.CharField(max_length=30, null=False)
    psychology = models.CharField(max_length=30, null=False)
    economics = models.CharField(max_length=30, null=False)
    english_literature = models.CharField(max_length=30, null=False)
    hindi = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'B.A'

from django.db import models

class Student_percent(models.Model):
    Student_rollno = models.CharField(max_length=20, unique=True)
    percentage = models.FloatField(null=True, blank=True)  # New field for percentage

class result(models.Model):
    roll_no=models.CharField(max_length=20)
    course=models.CharField(max_length=20)
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
