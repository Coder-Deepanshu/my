from rest_framework import serializers
from .models import Leave, Department, Course
from datetime import datetime

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
    
    def validate_start_date(self, value):
        """Validate start date is not in past"""
        if value < datetime.now().date():
            raise serializers.ValidationError("Start date cannot be in the past")
        return value
    
    def validate_end_date(self, value):
        """Validate end date is after start date"""
        start_date = self.initial_data.get('start_date')
        if start_date and value < datetime.strptime(start_date, '%Y-%m-%d').date():
            raise serializers.ValidationError("End date must be after start date")
        return value

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
            