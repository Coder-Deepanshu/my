from django.db import models
from django.utils import timezone # Import timezone for default date


# for department
class Department(models.Model):
    department_id = models.CharField(max_length=200,unique=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    type = models.CharField(max_length=10) # faculty ha ya admin
    description = models.TextField()
    programs_count = models.PositiveIntegerField(default=1)
    faculty_count = models.PositiveIntegerField(default=1)
    student_capacity = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Level(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    course_id = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='pictures')
    name = models.CharField(max_length=100)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    no_of_years = models.IntegerField()
    no_of_semesters = models.IntegerField()
    code = models.CharField(max_length=50)
    description = models.TextField()
    student_capacity = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    fees_per_year = models.IntegerField()
    no_of_lecture = models.IntegerField()

    def __str__(self):
        return self.name
    
class Position(models.Model):
    position_id = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    responsibility = models.TextField()
    requirment = models.TextField()
    specialization = models.TextField()
    salary = models.IntegerField()
    
    status = models.CharField(max_length=10,default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
class Faculty(models.Model):
    # Basic Info
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    college_id=models.CharField(max_length=15,unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    position = models.OneToOneField(Position,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=50)

    # Experience & Joining
    experience = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 5.5 years
    date_of_joining = models.DateField()

    # Contact Info
    phone = models.CharField(max_length=15,unique=True)
    other_phone_no = models.CharField(max_length=15,null=True,unique=True)
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
],default='India')

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
    adhar_no = models.BigIntegerField(unique=True)
    pan_no = models.CharField(max_length=20,unique=True)

    # Marital Status
    martial_status = models.CharField(max_length=15, choices=[
        ('married', 'Married'),
        ('unmarried', 'Unmarried')
    ], default='unmarried')
    user_id=models.CharField(max_length=50,null=True,)
    username=models.EmailField()
    password=models.CharField(max_length=15,null=True)
    chat_identifier = models.CharField(max_length=100,unique=False,null=True,blank=True)
    online_status = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    
    permission = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.chat_identifier:
            self.chat_identifier = f"faculty_{self.college_id}"
        super().save(*args, **kwargs)


    def _str_(self):
        return self.name
    
class FacultyDocuments(models.Model):
    faculty = models.OneToOneField(Faculty,on_delete=models.CASCADE)
    pic1 = models.ImageField(upload_to="pic1/",blank=True,null=True) # Adhar no
    pic2 = models.ImageField(upload_to="pic2/",blank=True,null=True)# Pan Card
    pic3 = models.ImageField(upload_to="pic3/",blank=True,null=True)# caste certificate
    pic4 = models.ImageField(upload_to="pic4/",blank=True,null=True)# residence certificate
    pic5 = models.ImageField(upload_to="pic5/",blank=True,null=True)# last qualification
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.faculty.name}-{self.uploaded_at}"
    
class Student(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    college_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,unique=True)
    other_phone_no=models.CharField(max_length=15,null=True,unique=True)
    occupation=models.CharField(max_length=50,null=True)
    income=models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=10)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)  # Changed to ForeignKey
    birthday = models.DateField()
    address = models.TextField()
    semester = models.IntegerField(default=1)
    year = models.IntegerField(default=1)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100,default='India')
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
    user_id=models.CharField(max_length=10,unique=True)
    username=models.EmailField(null=True,blank=True)
    password=models.CharField(max_length=15,unique=True)
    chat_identifier = models.CharField(max_length=255,unique=False,blank=True,null=True)
    online_status = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    followed_faculty = models.ManyToManyField(Faculty, related_name='followers', blank=True)
    permission = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.chat_identifier:
            self.chat_identifier = f"student_{self.college_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.college_id})"  
    
class StudentDocuments(models.Model):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    pic1 = models.ImageField(upload_to="pic1/",blank=True,null=True) # Adhar no
    pic2 = models.ImageField(upload_to="pic2/",blank=True,null=True)# Pan Card
    pic3 = models.ImageField(upload_to="pic3/",blank=True,null=True)# caste certificate
    pic4 = models.ImageField(upload_to="pic4/",blank=True,null=True)# residence certificate
    pic5 = models.ImageField(upload_to="pic5/",blank=True,null=True)# character certificate
    pic6 = models.ImageField(upload_to="pic6/",blank=True,null=True)# income certificate
    pic7 = models.ImageField(upload_to="pic7/",blank=True,null=True)# family id
    pic8 = models.ImageField(upload_to="pic8/",blank=True,null=True)# 10th DMC
    pic9 = models.ImageField(upload_to="pic9/",blank=True,null=True)# 12th DMC
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name}-{self.uploaded_at}"  
    
# for admin 
class Admin(models.Model):
    # Basic Info
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    college_id=models.CharField(max_length=15,unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    position = models.OneToOneField(Position,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=50)

    # Experience & Joining
    experience = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 5.5 years
    date_of_joining = models.DateField()

    # Contact Info
    phone = models.CharField(max_length=15,unique=True)
    other_phone_no = models.CharField(max_length=15,null=True,unique=True)
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
    
    permission = models.BooleanField(default=False)
    
    def _str_(self):
        return self.name
    
class AdminDocuments(models.Model):
    admin = models.OneToOneField(Admin,on_delete=models.CASCADE)
    pic1 = models.ImageField(upload_to="pic1/",blank=True,null=True) # Adhar no
    pic2 = models.ImageField(upload_to="pic2/",blank=True,null=True)# Pan Card
    pic3 = models.ImageField(upload_to="pic3/",blank=True,null=True)# caste certificate
    pic4 = models.ImageField(upload_to="pic4/",blank=True,null=True)# residence certificate
    pic5 = models.ImageField(upload_to="pic5/",blank=True,null=True)# character certificate  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admin.name}-{self.uploaded_at}"  
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.CharField(max_length=50,null=True)
    lecture_number = models.IntegerField()  # e.g., 1, 2, 3 for the day
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    timing = models.TimeField(auto_now_add=True,null=True)

    class Meta:
        unique_together = ('student', 'course', 'lecture_number', 'date')

    def _str_(self):
        return f"{self.student.name} - Lecture {self.lecture_number} - {self.date}"

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


from django.db import models
from django.core.validators import MinValueValidator

# Example of what your model might look like
class FeeStructure(models.Model):
    structure_id = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    due_date = models.DateField()
    year = models.CharField(max_length=50)  # or IntegerField
    semester = models.CharField(max_length=50)  # or IntegerField
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    batch = models.CharField(max_length=20)  # or for_year if that's the field name
    
    def __str__(self):
        return f"{self.course} - {self.batch}"
    
class FeePayment(models.Model):
    PAYMENT_TYPES = [
        ('REGULAR', 'Regular Payment'),
        ('EXTRA', 'Extra Payment'),
        ('ADVANCE', 'Advance Payment'),
        ('ADJUSTMENT', 'Adjustment Payment'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Online', 'Online Transfer'),
        ('Card', 'Credit/Debit Card')
    ])
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='REGULAR')
    status = models.CharField(max_length=20, default='Paid', choices=[
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
        ('Partial', 'Partial Payment')
    ])
    remarks = models.TextField(blank=True, null=True)
    verified_by = models.CharField(max_length=100, blank=True, null=True)
    adjusted_in_year = models.CharField(max_length=5,null=True, blank=True)
    adjusted_in_semester = models.CharField(max_length=5,null=True, blank=True)
    extra = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.student.name} - {self.amount_paid} ({self.payment_type})"

class StudentBalance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    extra_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Extra: {self.extra_amount}, Advance: {self.advance_amount}"
    
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

# models.py
from django.db import models

class Students(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)

    def _str_(self):
        return self.name