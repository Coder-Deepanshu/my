from rest_framework import serializers
from .models import Leave, Department, Course,  Student
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from .utils import leaves_limit

MAX_LEAVES_PER_MONTH = leaves_limit(True)

class LeaveSerializer(serializers.ModelSerializer):
    # Add this field to handle content_type as pk
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    department_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    applied_on = serializers.DateTimeField(
        format="%d-%m-%Y %I:%M %p",
        read_only=True
    )
    start_date = serializers.DateField(
        format="%d/%b/%Y",
    )
    end_date = serializers.DateField(
        format="%d/%b/%Y",
    )
    # def get_short_name(self, obj):
    #     name = ""

    #     if obj.content_type.model == 'admin':
    #         admin = Admin.objects.filter(college_id=obj.college_id).first()
    #         if admin:
    #             name = f"{admin.name} {admin.last_name}"

    #     elif obj.content_type.model == 'faculty':
    #         faculty = Faculty.objects.filter(college_id=obj.college_id).first()
    #         if faculty:
    #             name = f"{faculty.name} {faculty.last_name}"

    #     elif obj.content_type.model == 'student':
    #         student = Student.objects.filter(college_id=obj.college_id).first()
    #         if student:
    #             name = f"{student.name} {student.last_name}"

    #     if name:
    #         parts = name.split()
    #         return ''.join([p[0].upper() for p in parts[:2]])

    #     return ''

    # def get_department_name(self, obj):
    #     if obj.content_type.model == 'admin':
    #         return Admin.objects.filter(college_id=obj.college_id).values_list('department__name', flat=True).first()
    #     if obj.content_type.model == 'faculty':
    #         return Faculty.objects.filter(college_id=obj.college_id).values_list('department__name', flat=True).first()
    #     return None

    # def get_name(self, obj):
    #     if obj.content_type.model == 'admin':
    #         admin = Admin.objects.get(college_id=obj.college_id)
    #         name = f"{admin.name} {admin.last_name}"
    #         return name
    #     if obj.content_type.model == 'faculty':
    #         faculty = Faculty.objects.get(college_id=obj.college_id)
    #         name = f"{faculty.name} {faculty.last_name}"
    #         return name
    #     if obj.content_type.model == 'student':
    #         student = Student.objects.get(college_id=obj.college_id)
    #         name = f"{student.name} {student.last_name}"
    #         return name
    #     return None
    
    class Meta:
        model = Leave
        fields = '__all__'
    
    def validate_start_date(self, value):
        """Validate start date is not in past"""
        today = datetime.now().date()
        if value < today:
            raise serializers.ValidationError("Start date cannot be in the past")
        return value
    
    def validate_end_date(self, value):
        """Validate end date is after start date"""
        start_date = self.initial_data.get('start_date')
        
        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            if value < start_date:
                raise serializers.ValidationError("End date must be after start date")
        return value

    # def validate(self, attrs):
    #     content_type = attrs['content_type']
    #     college_id = attrs['college_id']
    #     leave_type = attrs['leave_type']
    #     total_days = attrs['total_days']
    #     limit = 3
    #     time = 6 # months
    #     taken_years = Leave.objects.filter(college_id = college_id, leave_type = leave_type, status = 'Approved')
    #     if taken_years + total_days > limit:
    #             raise serializers.ValidationError(f"Leave limit Exceeded Monthly limit = {limit} days")
    #     return attrs

    # def get_applied_by_detail(self, obj):
    #     user = obj.applied_by
    #     if user is None:
    #         return None
    #     return f'{user.name} {user.last_name}'







# FACULTY MINI
from .models import Staff
class FacultyMiniSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'last_name']

# LAB
from.models import Student, Lab
from django.db import models
class LabSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'

# LAB MINI
class LabMiniSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'name', 'number']

# LAB EXCEL 
class LabExcelImportSerializers(serializers.Serializer):
    file = serializers.FileField()
    # department = serializers.CharField(write_only = True)

    def validate_file(self, file):
        allowed_extension = ['xls', 'xlsx']
        ext = file.name.split('.')[-1].lower()

        if ext not in allowed_extension:
            raise serializers.ValidationError("Only Excel File (.xlx, .xlsx) are Allowed !")
        return file

# LECTURE
from .models import Lecture, Lab, Setting, Subject
class LectureSerializers(serializers.ModelSerializer):
    start_time = serializers.TimeField(input_formats=['%I:%M %p'])
    end_time = serializers.TimeField(input_formats=['%I:%M %p'])
    
    class Meta:
        model = Lecture
        fields = '__all__'

# FOR SUBJECT 
class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

# SUBJECTS MINI 
from .models import Subject, Staff
class SubjectMiniSerializers(serializers.ModelSerializer):
    faculties = serializers.SerializerMethodField()
    labs = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = ["id", "name", "code", "faculties", "labs"]

    def get_faculties(self, obj):
        faculties = Staff.objects.filter(department = obj.department)
        return FacultyMiniSerilizers(faculties, many =True).data

    def get_labs(self, obj):
        labs = Lab.objects.filter(department = obj.department)
        return LabMiniSerilizers(labs, many = True).data

# FOR SETTING
class SettingSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'   




            

# FOR STAFF
from .models import Staff
from django.contrib.auth.models import User
from .tasks import send_email
from django.db.models import Max
class StaffSerializer(serializers.ModelSerializer):
    position_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Staff
        fields = '__all__'

    def create(self, validated_data):
        college_id = validated_data.pop('college_id', None)
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        email = validated_data.get("email")

        if not username:
            username = validated_data.get('email')

        if not password:
            password = str(validated_data.get("phone"))

        if not college_id:
            max_id = Staff.objects.aggregate(Max("college_id"))["college_id__max"]

            if max_id:
                number = int(max_id[2:])
                college_id = f"SF{number + 1}"
            else:
                college_id = "SF1001"

            
        user = User.objects.create_user(username=username, password=password, email=validated_data.get('email'))
        staff = Staff.objects.create(user=user, college_id=college_id, username=username, password=password, **validated_data)

        message = f"Your College ID is {college_id}.\n Your Login Details are:\n Username: {username}\n Password: {password}\n Don't Share to anyone. "
        subject = "Your Account is Created."
        
        send_email.apply_async(args= [email, subject, message], countdown=2)
        return staff

    def get_department_name(self, obj):
        dept_name = Department.objects.get(id=obj.department.id).name
        return dept_name

    def get_position_name(self, obj):
        pos_name = Position.objects.get(id=obj.position.id).name
        return pos_name

class StaffMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'last_name', 'email', 'department__name', 'position']

# FOR STUDENT
from .models import Student
class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        college_id = validated_data.pop('college_id', None)
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        email = validated_data.get("email")

        if not username:
            username = validated_data.get('email')

        if not password:
            password = str(validated_data.get("phone"))

        if not college_id:
            max_id = Student.objects.aggregate(Max("college_id"))["college_id__max"]

            if max_id:
                number = int(max_id[2:])
                college_id = f"ST{number + 1}"
            else:
                college_id = "ST1001"

        # FETCH REGISTARTION NO.
        last_student = Student.objects.order_by("-registration_no").first()

        if last_student:
            last_reg = last_student.registration_no
            number = int(last_reg[5:]) + 1
        else:
            number = 1
        new_reg = f"ABCDE{number:04d}"
        validated_data["registration_no"] = new_reg        

        # CREATE USER
        user = User.objects.create_user(username=username, password=password, email=validated_data.get('email'))
        staff = Student.objects.create(user=user, college_id=college_id, username=username, password=password, **validated_data)

        # SEND EMAIL
        message = f"Your College ID is {college_id}.\n Your Login Details are:\n Username: {username}\n Password: {password}\n Don't Share to anyone. "
        subject = "Your Account is Created."
        
        send_email.apply_async(args= [email, subject, message], countdown=2)
        return staff


class StudentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'last_name', 'email', 'department__name', 'course']

# FOR COURSE
from .models import Course, Department
class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p", read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        name = data.get("name")
        level = data.get("level")

        # Update case handle karne ke liye
        instance = self.instance

        qs = Course.objects.filter(name=name, level=level)

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError("Course with this name and type already exists.")

        return data

    def validate_image(self, value):
        max_size = 2 * 1024 * 1024  # 2MB

        if value.size > max_size:
            raise serializers.ValidationError("Image size must be less than 2MB.")

        return value

    def get_department_name(self, obj):
        dept_name = Department.objects.get(id=obj.department.id).name
        return dept_name

class CourseMiniSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Course
        fields = ['id', 'name', 'level']

# FOR DEPARTMENT
from .models import Department
from rest_framework.validators import UniqueValidator
class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=Department.objects.all(), message="Department Already Exists!")])
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p", read_only=True)
    class Meta:
        model = Department
        fields = '__all__'

    def validate(self, data):
        name = data.get("name")
        code = data.get("code")
        type = data.get("type")

        # Update case handle karne ke liye
        instance = self.instance

        qs = Department.objects.filter(name=name, code=code, type=type)

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError("Department with this name and type already exists.")

        return data

class DepartmentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

# FOR POSITION
from .models import Position
class PositionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p", read_only=True)
    class Meta:
        model = Position
        fields = '__all__'

    def validate(self, data):
        name = data.get("name")
        role = data.get("role")
        type = data.get("type")
        rank = data.get("rank")

        # Update case handle karne ke liye
        instance = self.instance

        qs = Position.objects.filter(name=name, role=role, type=type, rank=rank)

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError("Course with this name and type already exists.")

        return data

class PositionMiniSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Position
        fields = ['id', 'name']

# FOR SCHEDULE
from .models import Schedule
class ScheduleSerilizer(serializers.ModelSerializer):
    lecture  = serializers.StringRelatedField()
    class Meta:
        model = Schedule
        fields = "__all__"

# FOR FEE STRUCTURE
from .models import FeeStructure
from rest_framework.exceptions import ValidationError
from django.db.models import Max
class FeeStrctureSerializers(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = "__all__"

    def create(self, validated_data):
        course = validated_data.get('course', None)
        semester = validated_data.get('semester', None)
        due_date = validated_data.get('due_date', None)

        student = Student.objects.filter(semester = semester, course = course).order_by('-id').first()
        if not student:
            raise serializers.ValidationError("Students Doesn't Exists with this details!")
        
        batch = str(student.doj.year)
        feestr = FeeStructure.objects.filter(course = course, semester = semester, batch = batch).first()

        if feestr:
            raise serializers.ValidationError("Fee Structure already exists!")
        else:
            structure = FeeStructure.objects.create(course = course, semester = semester, due_date = due_date, batch = batch)
            
        return structure     
        