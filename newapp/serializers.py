from rest_framework import serializers
from .models import Leave, Department, Course, Admin, Faculty, Student
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
    def get_short_name(self, obj):
        name = ""

        if obj.content_type.model == 'admin':
            admin = Admin.objects.filter(college_id=obj.college_id).first()
            if admin:
                name = f"{admin.name} {admin.last_name}"

        elif obj.content_type.model == 'faculty':
            faculty = Faculty.objects.filter(college_id=obj.college_id).first()
            if faculty:
                name = f"{faculty.name} {faculty.last_name}"

        elif obj.content_type.model == 'student':
            student = Student.objects.filter(college_id=obj.college_id).first()
            if student:
                name = f"{student.name} {student.last_name}"

        if name:
            parts = name.split()
            return ''.join([p[0].upper() for p in parts[:2]])

        return ''

    def get_department_name(self, obj):
        if obj.content_type.model == 'admin':
            return Admin.objects.filter(college_id=obj.college_id).values_list('department__name', flat=True).first()
        if obj.content_type.model == 'faculty':
            return Faculty.objects.filter(college_id=obj.college_id).values_list('department__name', flat=True).first()
        return None

    def get_name(self, obj):
        if obj.content_type.model == 'admin':
            admin = Admin.objects.get(college_id=obj.college_id)
            name = f"{admin.name} {admin.last_name}"
            return name
        if obj.content_type.model == 'faculty':
            faculty = Faculty.objects.get(college_id=obj.college_id)
            name = f"{faculty.name} {faculty.last_name}"
            return name
        if obj.content_type.model == 'student':
            student = Student.objects.get(college_id=obj.college_id)
            name = f"{student.name} {student.last_name}"
            return name
        return None
    
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

    def get_applied_by_detail(self, obj):
        user = obj.applied_by
        if user is None:
            return None
        return f'{user.name} {user.last_name}'


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

        def validate(self, data):
            code = data.get('code')
            type = data.get('type')
            department = Department.objects.filter(code = code, type = type)
            if department.exists():
                raise serializers.ValidationError('Department Already Exists!')
            return data

class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
            name = data.get('name')
            department = data.get('department')
            level = data.get('level')
            course = Course.objects.filter(name = name, department = department, level = level)
            if course.exists():
                raise serializers.ValidationError('Course Already Exists!')
            return data

from.models import Student, Attendance, Lab
class LabSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')
        number = attrs.get('number')
        lab = Lab.objects.filter(name = name, number = number)
        if lab.exists():
            raise serializers.ValidationError('Lab Already Exists!')
        return attrs
    
            