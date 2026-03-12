from django.db import models
from django.utils import timezone # Import timezone for default date

# FOR DEPARTMENT
class Department(models.Model):
    TYPE_CHOICES = [('Academic', 'Academic'), ('Administrative', 'Administrative')]
    
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    type = models.CharField(choices=TYPE_CHOICES , max_length=20)
    description = models.TextField()
    programs = models.IntegerField(null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"

# FOR COURSE
class Course(models.Model):
    LEVEL_CHOICES = [('AI', 'AI'), ('General', 'General'), ('Honours', 'Honours')]
    TYPE_CHOICES = [('UG', 'UG'), ('PG', 'PG')]
    
    image = models.ImageField(upload_to='course_image/', null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    fees = models.IntegerField() # fees per semester
    semesters = models.IntegerField()
    description = models.TextField()
    max_student = models.PositiveIntegerField(default=100)
    eligibility = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name}'

# FOR POSITION  
class Position(models.Model):
    TYPE_CHOICES = [('Teaching', 'Teaching'), ('Non-Teaching', 'Non-Teaching'), ('Both', 'Both')]
    ROLE_CHOICES = [('Faculty', 'Faculty'), ('Admin', 'Admin'), ('SuperAdmin', 'SuperAdmin')]
    RANK_CHOICES = [(1, "SuperAdmin"), (2, "Admin"), (3, "HOD"), (4, "Faculty"), (5, "Normal Staff")]
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    responsibility = models.TextField()
    salary = models.IntegerField(null=True)  
    status = models.BooleanField(default=True)
    rank = models.IntegerField(choices=RANK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
from django.conf import settings
from django.contrib.auth.models import User
class SuperAdmin(models.Model):
    college_id = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.college_id:

            last_superadmin = SuperAdmin.objects.order_by('-id').first()

            if last_superadmin and last_superadmin.college_id:
                last_id = int(last_superadmin.college_id.replace("SUP", ""))
                new_id = last_id + 1
            else:
                new_id = 1

            self.college_id = f"SUP{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.last_name}"
    
from django.db.models import Max
from django.conf import settings
class Staff(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    MS_CHOICES = [('Married', 'Married'), ('Unmarried', 'Unmarried')]
    CATEGORY_CHOICES = [('Genral', 'Genral'), ('BC(A)', 'BC(A)'), ('BC(B)', 'BC(B)'), ('SC', 'SC'), ('ST', 'ST'), ('Others', 'Others')]
    RELIGION_CHOICES = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Sikh', 'Sikh'), ('Christian', 'Christian'), ('Jain', 'Jain'), ('Buddhist', 'Buddhist'), ('Other', 'Other')]
    
    # BASIC INFO
    profile_picture = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    college_id=models.CharField(max_length=15,unique=True, blank=True, null=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True)
    emergency_contact = models.IntegerField(unique=True)
    adhar_no = models.BigIntegerField(unique=True)
    pan_no = models.CharField(max_length=10,unique=True)
    dob = models.DateField()
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    martial_status = models.CharField(max_length=10, choices=MS_CHOICES, default='Unmarried')

    # ADDRESS
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    pin_code = models.IntegerField()
    country = models.CharField(max_length=10, default='India')
    
    # QUALIFICATION DETAILS
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    experience = models.DecimalField(max_digits=4, decimal_places=1)
    doj = models.DateField(auto_now_add=True)
 
    # Nationality & Religion
    nationality = models.CharField(max_length=10, default="Indian")
    religion = models.CharField(max_length=10, choices=RELIGION_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    # LOGIN INFO
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=10)
    personal_pin = models.CharField(max_length=5, default='00000')
    status = models.BooleanField(default=True)
    document_permission = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"

# FOR FACULTY DOCUMENTS
from django.core.validators import FileExtensionValidator
class StaffDocument(models.Model):
    VALIDATOR = [FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    adhar = models.ImageField(upload_to="adhar/", blank=True, null=True, validators=VALIDATOR)
    pan = models.ImageField(upload_to="pan/", blank=True, null=True, validators=VALIDATOR)
    qualification_certificate = models.ImageField(upload_to="qualification_certificate/", blank=True, null=True, validators=VALIDATOR)
    experience_certificate = models.ImageField(upload_to="experience_certificate/", blank=True, null=True, validators=VALIDATOR)
    resume = models.ImageField(upload_to="resume/", blank=True, null=True, validators=VALIDATOR)
    digital_signature = models.ImageField(upload_to="digital_signature/", blank=True, null=True, validators=VALIDATOR)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff.name} {self.staff.last_name}"
    
from django.conf import settings
class Student(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MS_CHOICES = [('Married', 'Married'), ('Unmarried', 'Unmarried')]
    CS_CHOICES = [('Active', 'Active'), ('Passout', 'Passout'), ('Dropout', 'Dropout')]
    CATEGORY_CHOICES = [('General', 'General'), ('BC(A)', 'BC(A)'), ('BC(B)', 'BC(B)'), ('SC', 'SC'), ('ST', 'ST'), ('Others', 'Others')]
    RELIGION_CHOICES = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Sikh', 'Sikh'), ('Christian', 'Christian'), ('Jain', 'Jain'), ('Buddhist', 'Buddhist'), ('Other', 'Other')]
    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    college_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    martial_status = models.CharField(max_length=15, choices=MS_CHOICES)
    email = models.EmailField(unique=True)
    registration_no = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=15,unique=True)
    emergency_contact = models.CharField(max_length=15, unique=True)
    father_occupation = models.CharField(max_length=50,null=True)
    father_income = models.IntegerField()

    # Academic Details
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField(default=1)
    year = models.IntegerField(default=1)
    doj = models.DateField(auto_now_add=True)
    
    # Address Details
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=20,default='India')

    # Educational Details
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tenth_board = models.CharField(max_length=10)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_board = models.CharField(max_length=10)
    previous_college = models.CharField(max_length=50, null=True)

    # Nationality & Religion
    blood_group = models.CharField(max_length=10, null=True)
    nationality = models.CharField(max_length=20, default="Indian")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)

    # Identity Details
    adhar_no = models.IntegerField()
    pan_no = models.CharField(max_length=20, null=True)
    family_id = models.CharField(max_length=20, null=True)
    family_id_phone_no = models.IntegerField()

    # Login Details
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20, unique=True)
    personal_pin = models.CharField(max_length=5, default='00000')
    current_status = models.CharField(max_length=20, choices=CS_CHOICES, default="Active")
    section = models.CharField(max_length=10, null=True)
    status = models.BooleanField(default=True)
    last_login = models.DateField(auto_now=True)
    permission = models.BooleanField(default=False, null=True)

    # Extra Details
    hostel_student = models.BooleanField(default=False, null=True)
    transport_opted = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return f"{self.name} {self.last_name}"  

# FOR STUDENT DOCUMENTS   
class StudentDocuments(models.Model):
    VALIDATOR = [FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    adhar = models.ImageField(upload_to="adhar/", blank=True, null=True, validators=VALIDATOR)
    pan = models.ImageField(upload_to="pan/", blank=True, null=True, validators=VALIDATOR)
    caste_certificate = models.ImageField(upload_to="caste_certificate/", blank=True, null=True, validators=VALIDATOR)
    residence_certificate = models.ImageField(upload_to="residence_certificate/", blank=True, null=True, validators=VALIDATOR)
    character_certificate = models.ImageField(upload_to="character_certificate/", blank=True, null=True, validators=VALIDATOR)
    income_certificate = models.ImageField(upload_to="income_certificate/", blank=True, null=True, validators=VALIDATOR)
    family_id = models.ImageField(upload_to="family_id/", blank=True, null=True, validators=VALIDATOR)
    tenth_marksheet = models.ImageField(upload_to="tenth_marksheet/", blank=True, null=True, validators=VALIDATOR)
    twelfth_marksheet = models.ImageField(upload_to="twelfth_marksheet/", blank=True, null=True, validators=VALIDATOR)
    digital_signature = models.ImageField(upload_to="digital_signature/", blank=True, null=True, validators=VALIDATOR)
    uploaded_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} {self.student.last_name}" 
    
# FOR SUBJECT
class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    semester = models.IntegerField()
    content = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.name} - {self.code}"

# FOR LAB 
class Lab(models.Model):
    TYPE_CHOICES = [('Laboratory', 'Laboratory'), 
                    ('Classroom', 'Classroom'), 
                    ('Lecture Room', 'Lecture Room'), 
                    ('Seminar Hall', 'Seminar Hall'),
                    ('Room', 'Room'),('Other', 'Other')]
    STATUS_CHOICES = [('Available', 'Available'), ('Occupied', 'Occupied')]
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    facility = models.TextField()
    capacity = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    floor = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}-{self.number}"

# FOR LECTURE
class Lecture(models.Model):
    TYPE_CHOICES = [('lecture', 'lecture'), ('interval', 'interval')]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester= models.IntegerField()
    name = models.CharField(max_length=50)
    type = models.CharField(choices=TYPE_CHOICES, max_length=50)
    start_time = models.TimeField(default="00:00")
    end_time = models.TimeField(default="00:00")
    
    def __str__(self):
        return f"{self.name}"

# FOR SCHEDULE
class Schedule(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    day_name = models.CharField(max_length=10)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lecture', 'lab', 'subject', 'faculty', 'day_name')

# FEE STRUCTURE
class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    semester = models.IntegerField() 
    batch = models.CharField(max_length=4, null=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ["course", "semester"]
            
    def __str__(self):
        return f"{self.course.name}"

# PAYMENT 
class Payment(models.Model):   
    PAYMENT_CHOICES = [("Cash", "Cash"), ("Cheque", "Cheque"), ("Online", "Online"), ("Card", "Credit/Debit Card")] 
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    date = models.DateField(auto_now=True)
    method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    remarks = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name}"





        
class UserDetail(models.Model):
    username = models.CharField(max_length=50, )
    user_id = models.CharField(max_length=50, )
    password = models.CharField(max_length=50, )

    def _str_(self):
        return f"{self.username} - {self.user_id}"

# FOR Apply Ai on login page 
from django.db import models

class DeviceFingerprint(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    fingerprint = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    is_suspicious = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.user.username} - {self.fingerprint[:10]}..."

from django.utils import timezone
from datetime import timedelta

class OTPVerification(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)  # 5 min expiry

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
    



















    
    
class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participant1 = models.CharField(max_length=100)
    participant2 = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_other_participant(self, current_participant):
        return self.participant2 if self.participant1 == current_participant else self.participant1

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)  # Add this field
    read_at = models.DateTimeField(null=True, blank=True)      # Add this field

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender_id} in {self.chat_room.name}"

class History(models.Model):
    history_id = models.CharField(max_length=50)
    content = models.TextField(null=False)
    position = models.CharField(max_length=50)
    updatedFrom = models.CharField(max_length=50)
    updatedTo = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    reciver_type = models.CharField(max_length=50)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.history_id



    


from django.db import models




# FOR QR GENERATION
class QR_code(models.Model):
    date = models.CharField(max_length=50, unique=True)
    time = models.CharField(max_length=50, unique=True)
    timestamp = models.CharField(max_length=50, unique=True)
    token = models.CharField(max_length=100, unique=True)
    random_data = models.CharField(max_length=50, unique=True)
    expired = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    expiry_time = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return f"token:{self.token}-data{self.random_data}"

class OTP(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True ,unique=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    otp = models.PositiveIntegerField()
    expired = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"otp:{self.otp}-data{self.lecture}"

# FOR STUDENT ATTENDANCE
class Attendance(models.Model):
    college_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave'), ('Pending', 'Pending')])
    timing = models.TimeField(auto_now_add=True,null=True)
    leave_time = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('college_id', 'lecture', 'date')

    def _str_(self):
        return f"{self.college_id.name} - Lecture {self.lecture} - {self.date}"

# FOR FACULTY AND ADMIN ATTENDANCE
class Faculty_and_Admin_Attedance(models.Model):
    CHOICES_STATUS = [('Absent', 'Absent'), 
                      ('Present', 'Present'), 
                      ('Leave', 'Leave'), 
                      ('Pending', 'Pending')]
    
    collegeID = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices= CHOICES_STATUS)
    type = models.CharField(max_length=20)
    timing = models.CharField(max_length=20)
    date = models.DateField()
    leave_time = models.IntegerField(null=True)

    def __str__(self):
        return f'CollegeID:{self.collegeID}'

# FOR LEAVE REQUESTS
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class Leave(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'), 
        ('Approved', 'Approved'), 
        ('Rejected', 'Rejected')
    ]
    
    # Change 1: Consistent naming
    LEAVE_TYPE_CHOICES = [
        ('Emergency Leave', 'Emergency Leave'),
        ('Planned Leave', 'Planned Leave'), 
        ('Short Leave', 'Short Leave'),
    ]
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    college_id = models.CharField(max_length=20)
    applied_by = GenericForeignKey('content_type', 'college_id')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField()
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)  # Change 2: Updated variable name
    time = models.TimeField(auto_now_add=True)
    contact_during_leave = models.CharField(max_length=15)
    reason = models.TextField()
    rejection_reason = models.TextField(default='')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='Pending')
    leave_time = models.IntegerField(null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.college_id}-{self.start_date}-{self.end_date}-{self.status}"

# FOR CREATING SETTING
class Setting(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} = {self.value}({self.type})"















    
# Student Assignment Model
class StudentAssignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('late', 'Late Submission'),
    ]
    
    assignment_id = models.AutoField(primary_key=True)
    faculty_id = models.CharField(max_length=50)
    student_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    assignment_title = models.CharField(max_length=200)
    description = models.TextField()
    marks = models.IntegerField(default=0)
    max_marks = models.IntegerField(default=100)
    due_date = models.DateField()
    submitted_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attachment = models.FileField(upload_to='assignments/', null=True, blank=True)
    feedback = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.assignment_title} - {self.student_name}"
    
    def is_overdue(self):
        if self.due_date and self.submitted_date:
            return self.submitted_date > self.due_date
        return False
    
    def save(self, *args, **kwargs):
        if self.submitted_date and self.due_date and self.submitted_date > self.due_date:
            self.status = 'late'
        super().save(*args, **kwargs)









