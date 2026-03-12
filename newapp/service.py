from .models import Department, Course, Staff, SuperAdmin
from datetime import datetime

def admin_details(request):
    role = request.session.get('role')
    college_id = request.session.get('admin_college_id')
    admin = Staff.objects.get(college_id = college_id)    
    courses = Course.objects.all().order_by('id')
#     departments = Department.objects.filter(type = 'Faculty').order_by('-id')
    context = {
            'role': role,
            'college_id': college_id,
            'admin': admin,
            'courses': courses,
        #     'departments': departments
            }
    return context

def set_date_formate(input):
        time_obj = datetime.strptime(str(input), '%H:%M:%S')
        time_12 = time_obj.strftime("%I:%M %p")

        return time_12


from django.apps import apps

class Details():
    def __init__(self, model_name, college_id):
        self.model_name = model_name
        self.college_id = college_id

    def detail(self):
        model = apps.get_model('newapp', self.model_name)
        instance = model.objects.get(college_id=self.college_id)

        detail = {
            'college_id': self.college_id,
            'name': f"{instance.name} {instance.last_name}",
            'department': f"{instance.department.name}"
        }

        if self.model_name == "Student":
            detail["course"] = f"{instance.course.name} - {instance.course.code}"
        else:
            detail["position"] = f"{instance.position.name}"

        return detail

from .models import Course, Department
from .serializers import CourseMiniSerializer, DepartmentMiniSerializer
class Options:
    def CourseOptions(self):
        courses = Course.objects.all().order_by('id')[:5]
        serializers = CourseMiniSerializer(courses, many=True)
        return serializers.data
    
    def DeptOptions(self, type):
        depts = Department.objects.filter(type=type).order_by('id')[:5]
        serializers = DepartmentMiniSerializer(depts, many=True)
        return serializers.data
    