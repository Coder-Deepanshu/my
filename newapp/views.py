from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Student,Course, Attendance, FeeStructure
from django.http import JsonResponse
import json # For handling JSON data from AJAX requests
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import DeviceFingerprint, UserDetail
from django.utils import timezone
import hashlib
import platform
import socket
import uuid
import json


# function of front page 
def home(request):
    return render(request,'Home/home.html')

def feature(request):
    return render(request,'Home/feature.html')

def about(request):
    return render(request,'Home/about.html')

def contact(request):
    return render(request,'Home/contact.html')

def course(request):
    return render(request,'Home/course.html')

def enroll(request):
    return render(request,'Home/enroll.html')

from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Student, Staff, SuperAdmin
from django.contrib.auth.models import User

class login(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def import_page(self, request): 
        return render(request, 'Home/login.html')

    @action(detail=False, methods=['get'])
    def verify_college_id(self, request):
        college_id = request.GET.get("college_id")
        request.session['college_id'] = college_id
        person = ''
        
        try:
            obj = Student.objects.get(college_id = college_id)
            person = "Student"
            
        except Student.DoesNotExist:
            try:
                obj = Staff.objects.get(college_id = college_id)
                person = obj.position.role

            except Staff.DoesNotExist:
                try:
                    obj = SuperAdmin.objects.get(college_id = college_id)
                    person = obj.position.role
       
                except SuperAdmin.DoesNotExist:
                    person = "Other"
                    return JsonResponse({"person": person})        
        request.session['person'] = person
        return JsonResponse({'person': person})

    @action(detail=False, methods=['get'])
    def verify_login_details(self, request):
        college_id = request.session.get("college_id")
        person = request.session.get("person")
        username = request.GET.get("username")
        password = request.GET.get("password")
        user = ''
        
        if person == "Student":
            try:
                member = Student.objects.get(college_id = college_id)
                user = member.user
                page = "/facultyDashboard/"
            except Student.DoesNotExist:
                return JsonResponse({"error": "User Does'nt Exits with this Info."})
        else:
            try:
                if person == "Admin":
                    member = Staff.objects.get(college_id = college_id, position__role = person)
                    user = member.user
                    page = "/adminDashboard/"
                elif person == "Faculty":
                    member = Staff.objects.get(college_id = college_id, position__role = person)
                    user = member.user
                    page = "/facultyDashboard/"
                elif person == "Superadmin":
                    member = SuperAdmin.objects.get(college_id = college_id, position__role = person)
                    user = member.user
                    page = "/facultyDashboard/"
                else:
                    return JsonResponse({"error": "User Does'nt Exits with this Info."})
                
            except Staff.DoesNotExist:
                    return JsonResponse({"error": "User Does'nt Exits with this Info."})
                
        try:
            if username == user.username and password == member.password:
                return JsonResponse({"page": page})
            else:
                return JsonResponse({"error": f"Invalid Login Credentials!"})
        except Exception as e:
            return JsonResponse({"error": f"An error Occured: {str(e)}"})

from django.shortcuts import render
from .models import User
class Dashboard(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def faculty(request):
        return render(request, "Dashboard/facultyDashboard.html")
    @action(detail=False, methods=["get"])
    def student(request):
        return render(request, "Dashboard/studentDashboard.html")
    @action(detail=False, methods=["get"])
    def admin(request):
        return render(request, "Dashboard/adminDashboard.html")



# def verify_collegeID(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         try:
#             userID = data.get('userID')
#             prefix = userID[:2]
            
#             if prefix == 'AD':
#                 admin = Admin.objects.filter(college_id=userID)
#                 if admin.exists():
#                     request.session['userID'] = userID
#                     return JsonResponse({'success': "Verified"})
#                 else:
#                     return JsonResponse({'error': 'ID not exists'}) 
                
#             elif prefix == 'GK':
#                 faculty = Faculty.objects.filter(college_id=userID)
#                 if faculty.exists():
#                     request.session['userID'] = userID
#                     return JsonResponse({'success': "Verified"})
#                 else:
#                     return JsonResponse({'error': 'ID not exists'}) 

#             elif prefix == 'ST':
#                 student = Student.objects.filter(college_id=userID)
#                 if student.exists():
#                     request.session['userID'] = userID
#                     return JsonResponse({'success': "Verified"})
#                 else:
#                     return JsonResponse({'error': 'ID not exists'})   
#             else:
#                 return JsonResponse({'error': 'Invalid College ID'})  
                    
#         except Exception as e:
#             return JsonResponse({'error': f'An error Occurred: {str(e)}'})
#     else:
#         return JsonResponse({'error': 'Method Not Found'})

# def generate_device_fingerprint(request):
#     # Collect various device information
#     user_agent = request.META.get('HTTP_USER_AGENT', '')
#     accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
#     accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
    
#     # Screen resolution (client side se milega)
#     screen_resolution = request.POST.get('screen_res', '')  # JavaScript se bhejna hoga
    
#     # Timezone
#     timezone = request.POST.get('timezone', '')  # JavaScript se bhejna hoga
    
#     # Platform information
#     platform_info = {
#         'system': platform.system(),
#         'release': platform.release(),
#         'version': platform.version(),
#         'architecture': platform.architecture()[0],
#         'processor': platform.processor(),
#     }
    
#     # Network information
#     hostname = socket.gethostname()
#     mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
#                            for elements in range(0,8*6,8)][::-1])
    
#     # Combine all data
#     fingerprint_data = {
#         'user_agent': user_agent,
#         'accept_language': accept_language,
#         'accept_encoding': accept_encoding,
#         'screen_resolution': screen_resolution,
#         'timezone': timezone,
#         'platform': platform_info,
#         'hostname': hostname,
#         'mac_address': mac_address,
#     }
    
#     # Create hash
#     fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
#     device_id = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
#     return device_id

# get client_ip address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_otp_email(user_email, otp):
    # OTP log file mein save karo
    import datetime
    with open('otp_debug.log', 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {user_email} | OTP: {otp}\n")
    
    # Optional: Try to send email (agar app password kaam kare toh)
    try:
        import smtplib
        from django.conf import settings
        
        # Simple email
        subject = "EduTrack OTP Verification"
        body = f"Your OTP code is: {otp}\nThis code expires in 5 minutes. \n Don't Share OTP with anyone."
        message = f"Subject: {subject}\n\n{body}"
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, user_email, message)
        server.quit()
        print(otp)
        
    except Exception as e:
        print(f"📧 Email skipped: {str(e)}")
    return True

# def login_view(request):
#     if request.method == 'POST':
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user_id = request.session.get('userID')
#             fingerprint_id = request.POST.get('fingerprint')
#             role = request.POST.get('role')
#             ip = get_client_ip(request)
            
#             if not username or not password :
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'Please fill all the fields'
#                 })
            
#             try:
#                 if role == 'admin':
#                     admin = Admin.objects.filter(email=username)
#                     if admin.exists():
#                         admin_detail = admin.first()
#                         filter_user_id = admin_detail.college_id
                        
#                         if user_id == filter_user_id:
#                             filter_password = admin_detail.phone
#                             if filter_password == password:
#                                 # Get or create UserDetail object
#                                 user_detail, created = UserDetail.objects.get_or_create(
#                                     username=username,
#                                     defaults={
#                                         'user_id': user_id,
#                                         'password': password,
#                                         'email': username
#                                     }
#                                 )
                                
#                                 # Check device fingerprint
#                                 existing_fp = DeviceFingerprint.objects.filter(
#                                     user=user_detail,
#                                     fingerprint=fingerprint_id
#                                 ).first()
                                
#                                 if existing_fp:
#                                     # Normal login - trusted device
#                                     existing_fp.ip_address = ip
#                                     existing_fp.last_login = timezone.now()
#                                     existing_fp.is_suspicious = False
#                                     existing_fp.save()
                                    
#                                     # Set session data
#                                     request.session['username1'] = f"{admin_detail.name} {admin_detail.last_name}"
#                                     request.session['admin_college_id'] = user_id 
#                                     request.session['role'] = role
                                    
#                                     return JsonResponse({
#                                         'success': True,
#                                         'message': f'Welcome {admin_detail.name} {admin_detail.last_name}!',
#                                         'redirect_url': '/Admin/Dashboard/',
#                                         'otp_required': False
#                                     })
#                                 else:
#                                     # New/suspicious device - send OTP
#                                     otp = str(random.randint(100000, 999999))
                                    
#                                     # Create OTP with UserDetail object
#                                     OTPVerification.objects.create(
#                                         user=user_detail,
#                                         otp_code=otp,
#                                         is_verified=False
#                                     )
                                    
#                                     # Send OTP email with SSL fix
#                                     email_sent = send_otp_email(username, otp)
                                    
#                                     if email_sent:
#                                         # Store verification data in session
#                                         request.session['verify_user'] = username
#                                         request.session['verify_role'] = role
#                                         request.session['verify_fingerprint'] = fingerprint_id
#                                         request.session['verify_ip'] = ip
                                        
#                                         return JsonResponse({
#                                             'success': True,
#                                             'message': 'OTP sent to your email',
#                                             'redirect_url': '/verify_otp/',
#                                             'otp_required': True
#                                         })
#                                     else:
#                                         return JsonResponse({
#                                             'success': False,
#                                             'error': 'Failed to send OTP. Please try again.'
#                                         })
#                             else:
#                                 return JsonResponse({
#                                     'success': False,
#                                     'error': 'Invalid Password'
#                                 })
#                         else:
#                             return JsonResponse({
#                                 'success': False,
#                                 'error': 'Invalid College ID'
#                             })
#                     else:
#                         return JsonResponse({
#                             'success': False,
#                             'error': 'Invalid Credentials'
#                         })
                
#                 # Faculty and student roles same structure mein rahenge
#                 elif role == 'faculty':
#                     faculty = Faculty.objects.filter(email=username)
#                     if faculty.exists():
#                         faculty_detail = faculty.first()
#                         filter_user_id = faculty_detail.college_id
                        
#                         if user_id == filter_user_id:
#                             filter_password = faculty_detail.phone
#                             if filter_password == password:
#                                 user_detail, created = UserDetail.objects.get_or_create(
#                                     username=username,
#                                     defaults={
#                                         'user_id': user_id,
#                                         'password': password,
#                                         'email': username
#                                     }
#                                 )
                                
#                                 existing_fp = DeviceFingerprint.objects.filter(
#                                     user=user_detail,
#                                     fingerprint=fingerprint_id
#                                 ).first()
                                
#                                 if existing_fp:
#                                     request.session['username2'] = f"{faculty_detail.name} {faculty_detail.last_name}"
#                                     request.session['faculty_college_id'] = user_id 
#                                     request.session['role'] = role
                                    
#                                     return JsonResponse({
#                                         'success': True,
#                                         'message': f'Welcome {faculty_detail.name} {faculty_detail.last_name}!',
#                                         'redirect_url': '/Faculty/Dashboard/',
#                                         'otp_required': False
#                                     })
#                                 else:
#                                     otp = str(random.randint(100000, 999999))
#                                     OTPVerification.objects.create(
#                                         user=user_detail,
#                                         otp_code=otp,
#                                         is_verified=False
#                                     )
                                    
#                                     email_sent = send_otp_email(username, otp)
                                    
#                                     if email_sent:
#                                         request.session['verify_user'] = username
#                                         request.session['verify_role'] = role
#                                         request.session['verify_fingerprint'] = fingerprint_id
#                                         request.session['verify_ip'] = ip
                                        
#                                         return JsonResponse({
#                                             'success': True,
#                                             'message': 'OTP sent to your email',
#                                             'redirect_url': '/verify_otp/',
#                                             'otp_required': True
#                                         })
#                                     else:
#                                         return JsonResponse({
#                                             'success': False,
#                                             'error': 'Failed to send OTP. Please try again.'
#                                         })
#                             else:
#                                 return JsonResponse({
#                                     'success': False,
#                                     'error': 'Invalid Password'
#                                 })
#                         else:
#                             return JsonResponse({
#                                 'success': False,
#                                 'error': 'Invalid College ID'
#                             })
#                     else:
#                         return JsonResponse({
#                             'success': False,
#                             'error': 'Invalid Credentials'
#                         })
                
#                 elif role == 'student':
#                     student = Student.objects.filter(email=username)
#                     if student.exists():
#                         student_detail = student.first()
#                         filter_user_id = student_detail.college_id
                        
#                         if user_id == filter_user_id:
#                             filter_password = student_detail.phone
#                             if filter_password == password:
#                                 user_detail, created = UserDetail.objects.get_or_create(
#                                     username=username,
#                                     defaults={
#                                         'user_id': user_id,
#                                         'password': password,
#                                         'email': username
#                                     }
#                                 )
                                
#                                 existing_fp = DeviceFingerprint.objects.filter(
#                                     user=user_detail,
#                                     fingerprint=fingerprint_id
#                                 ).first()
                                
#                                 if existing_fp:
#                                     request.session['username3'] = f"{student_detail.name} {student_detail.last_name}"
#                                     request.session['student_college_id'] = user_id 
#                                     request.session['role'] = role
                                    
#                                     return JsonResponse({
#                                         'success': True,
#                                         'message': f'Welcome {student_detail.name} {student_detail.last_name}!',
#                                         'redirect_url': '/Student/Dashboard/',
#                                         'otp_required': False
#                                     })
#                                 else:
#                                     otp = str(random.randint(100000, 999999))
#                                     OTPVerification.objects.create(
#                                         user=user_detail,
#                                         otp_code=otp,
#                                         is_verified=False
#                                     )
                                    
#                                     email_sent = send_otp_email(username, otp)
                                    
#                                     if email_sent:
#                                         request.session['verify_user'] = username
#                                         request.session['verify_role'] = role
#                                         request.session['verify_fingerprint'] = fingerprint_id
#                                         request.session['verify_ip'] = ip
                                        
#                                         return JsonResponse({
#                                             'success': True,
#                                             'message': 'OTP sent to your email',
#                                             'redirect_url': '/verify_otp/',
#                                             'otp_required': True
#                                         })
#                                     else:
#                                         return JsonResponse({
#                                             'success': False,
#                                             'error': 'Failed to send OTP. Please try again.'
#                                         })
#                             else:
#                                 return JsonResponse({
#                                     'success': False,
#                                     'error': 'Invalid Password'
#                                 })
#                         else:
#                             return JsonResponse({
#                                 'success': False,
#                                 'error': 'Invalid College ID'
#                             })
#                     else:
#                         return JsonResponse({
#                             'success': False,
#                             'error': 'Invalid Credentials'
#                         })
                
#             except Exception as e:
#                 return JsonResponse({
#                     'success': False,
#                     'error': f'An error occurred: {str(e)}'
#                 })
        
#         else:
#             messages.error(request, "Invalid request method")
#             return redirect('login')
    
#     return render(request, 'Home/login.html')

# def verify_otp_view(request):
#     if request.method == 'GET':
#         username = request.session.get('verify_user')
#         return render(request, 'verify_otp.html', {'user_email': username})
    
#     elif request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         username = request.session.get('verify_user')
#         role = request.session.get('verify_role')
#         fingerprint = request.session.get('verify_fingerprint')
#         ip = request.session.get('verify_ip')
        
#         if not username or not entered_otp:
#             messages.error(request, "Invalid OTP verification request")
#             return redirect('login')
        
#         try:
#             print(f"Verifying OTP: {entered_otp} for user: {username}")
            
#             user_detail = UserDetail.objects.get(username=username)
            
#             otp_record = OTPVerification.objects.filter(
#                 user=user_detail,
#                 otp_code=entered_otp, 
#                 is_verified=False
#             ).order_by('-created_at').first()
            
#             print(f"OTP record found: {otp_record}")
            
#             if otp_record:
#                 if not otp_record.is_expired():
#                     otp_record.is_verified = True
#                     otp_record.save()
                    
#                     DeviceFingerprint.objects.create(
#                         user=user_detail,
#                         fingerprint=fingerprint,
#                         ip_address=ip,
#                         last_login=timezone.now(),
#                         is_suspicious=False
#                     )
                    
#                     if role == 'admin':
#                         admin = Admin.objects.get(email=username)
#                         request.session['username1'] = f"{admin.name} {admin.last_name}"
#                         request.session['admin_college_id'] = request.session.get('userID')
#                         request.session['role'] = role
#                         redirect_url = '/Admin/Dashboard/'
                        
#                     elif role == 'faculty':
#                         faculty = Faculty.objects.get(email=username)
#                         request.session['username2'] = f"{faculty.name} {faculty.last_name}"
#                         request.session['faculty_college_id'] = request.session.get('userID')
#                         request.session['role'] = role
#                         redirect_url = '/Faculty/Dashboard/'
                        
#                     elif role == 'student':
#                         student = Student.objects.get(email=username)
#                         request.session['username3'] = f"{student.name} {student.last_name}"
#                         request.session['student_college_id'] = request.session.get('userID')
#                         request.session['role'] = role
#                         redirect_url = '/Student/Dashboard/'
                    
#                     request.session.pop('verify_user', None)
#                     request.session.pop('verify_role', None)
#                     request.session.pop('verify_fingerprint', None)
#                     request.session.pop('verify_ip', None)
                    
#                     messages.success(request, "OTP verified successfully!")
#                     return redirect(redirect_url)
                    
#                 else:
#                     messages.error(request, "OTP has expired. Please login again.")
#                     otp_record.delete()
#                     return redirect('login')
#             else:
#                 messages.error(request, "Invalid OTP. Please try again.")
#                 return render(request, 'verify_otp.html', {'user_email': username})
                
#         except UserDetail.DoesNotExist:
#             messages.error(request, "User not found. Please login again.")
#             return redirect('login')
#         except Exception as e:
#             messages.error(request, f"An error occurred: {str(e)}")
#             return redirect('login')


# from django.views.decorators.csrf import csrf_exempt




from rest_framework.viewsets import ModelViewSet
from newapp.pagination import CommonPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action

# FOR STAFF
from .serializers import StaffSerializer, PositionMiniSerializer, DepartmentMiniSerializer
from .models import Staff, Position
class StaffAPI(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['get'])
    def import_page(self, request):
        person = request.session.get("person")
        if not person:
            person = "Other"
            
        context = {
            "person": person
            }
        return render(request, "admin/Add/staffAdd.html", context)

    @action(detail=False, methods=['get'])
    def import_bulk_page(self, request):
        return render(request, "admin/Bulk/staffBulk.html")

    @action(detail=False, methods=['get'])
    def departments(self, request):
        departments = Department.objects.all().exclude(name = "SuperAdmin")
        departments = DepartmentMiniSerializer(departments, many=True)
        return JsonResponse({"departments": departments.data})

    @action(detail=False, methods=['get'])
    def positions(self, request):
        department = request.GET.get("dept_id")
        occ_positions = Staff.objects.filter(department=department).values_list("position_id", flat=True)
        available_positions = Position.objects.exclude(rank=1).exclude(id__in=occ_positions)
        serializer = PositionMiniSerializer(available_positions, many=True)
        return JsonResponse({"positions": serializer.data})

    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        department = request.GET.get("dept_id")
        occ_positions = Staff.objects.filter(department=department).values_list("position_id", flat=True)
        available_positions = Position.objects.exclude(rank=1).exclude(id__in=occ_positions)
        serializer = PositionMiniSerializer(available_positions, many=True)
        return JsonResponse({"positions": serializer.data})
    
# FOR STUDENT
from .serializers import StudentSerializer
from .models import Student
class StudentAPI(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def import_page(self, request):
        return render(request, "admin/Add/studentAdd.html")

    @action(detail=False, methods=["get"])
    def courses(self, request):
        context = {
            "courses": Options().CourseOptions()
            }
        return JsonResponse(context)

# FOR DEPARTMENT
from .serializers import DepartmentSerializer
from rest_framework.decorators import action
from .models import Department
from .service import Details
class DepartmentAPI(ModelViewSet):
    queryset = Department.objects.all().order_by("id")
    serializer_class = DepartmentSerializer
    pagination_class = CommonPagination
    
    search_fields = ['name', 'code', 'type']     

    @action(detail=False, methods=['get'])
    def import_page(self, request):
        return render(request, "admin/Creation/departmentCreation.html")

    @action(detail=False, methods=['get'])
    def details(self, request):
        courses = Course.objects.count()
        departments = Department.objects.count()
        staff = Staff.objects.count()
        students = Student.objects.count()
        context = {
            "courses": courses,
            "departments": departments,
            "staff": staff,
            "student": students
        }
        return JsonResponse(context)

# FOR COURSE
from .serializers import CourseSerializer, DepartmentMiniSerializer
from .models import Course
class CourseAPI(ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    pagination_class = CommonPagination
    search_fields = ['name', 'code', 'type']     

    @action(detail=False, methods=['get'])
    def import_page(self, request):
        return render(request, "admin/Creation/courseCreation.html")

    @action(detail=False, methods=['get'])
    def details(self, request):
        courses = Course.objects.count()
        departments = Department.objects.count()
        staff = Staff.objects.count()
        students = Student.objects.count()

        department = Department.objects.all().exclude(type = "Administrative")
        department = DepartmentMiniSerializer(department, many=True)
        
        context = {
            "courses": courses,
            "departments": departments,
            "staff": staff,
            "students": students,
            "dept_options": department.data
        }
        return JsonResponse(context)

# FOR POSITION
from .serializers import PositionSerializer
from .models import Position
class PositionAPI(ModelViewSet):
    queryset = Position.objects.all().order_by("id")
    serializer_class = PositionSerializer
    pagination_class = CommonPagination
    search_fields = ['name', 'role', 'type', 'rank']     

    @action(detail=False, methods=['get'])
    def import_page(self, request):
        return render(request, "admin/Creation/positionCreation.html")

# FOR FEE STRUCTURE
from .models import FeeStructure
from .serializers import FeeStrctureSerializers
class FeeStructureAPI(ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStrctureSerializers

    @action(detail=False, methods=["get"])
    def import_page(self, request):
        context = {
            "courses": Options().CourseOptions()
            }
        return render(request, "admin/Creation/feeStructureCreation.html", context)
    
    @action(detail=False, methods=["post"])
    def bulk(self, request):
        semester = request.data.get("semester")
        due_date = request.data.get("due_date")
        course_list = request.data.get("course_list")

        count = 0

        for i in course_list:
            student = Student.objects.filter(semester = semester, course_id = int(i)).order_by('-id').first()
            if not student:
                continue
            batch = str(student.doj.year)
            obj = FeeStructure.objects.filter(course_id=int(i), semester=semester, batch = batch).first()

            if not obj:
                FeeStructure.objects.create(course_id=int(i),semester=semester, due_date=due_date, batch = batch)
                count += 1

        message = ""

        if count != 0:
            message = f"Out of {len(course_list)} only {count}"

        return JsonResponse({"message": f"{message} Structure are Created Successfully!"})
    
# COMMON
from django.db.models import Q
class Common(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def semester(self, request):
        course_id = request.GET.get("course_id")
        semesters = Course.objects.get(id = course_id).semesters
        return JsonResponse({"semesters": semesters})
    
    @action(detail=False, methods=["get"])
    def search_course(self, request):
        query = request.GET.get("q")

        courses = Course.objects.filter(
            Q(name__icontains = query)|
            Q(code__icontains = query)|
            Q(level__icontains = query)|
            Q(department__name__icontains = query)
            )

        data = list(courses.values("id", "name", "level"))
        return JsonResponse({"data": data})
        
    





        

# FOR CREATING THE LABS
import pandas as pd
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Lab
from .serializers import LabSerializers, LabExcelImportSerializers
class LabAPI(ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializers
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['post'], url_path='import-excel', serializer_class=LabExcelImportSerializers)
    def import_excel(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']
        df = pd.read_excel(file)

        df.columns = df.columns.str.strip()
        df = df.dropna(how='all')

        data = df.to_dict(orient='records')

        new_records = []
        skipped = 0

        for row in data:
            try:
                department_name = str(row.get('department')).strip()

                department = Department.objects.filter(
                            Q(name__iexact=department_name) |
                            Q(code__iexact=department_name)
                            ).first()
                
                if not department:
                    skipped += 1
                    continue

                # duplicate check
                if Lab.objects.filter( number=row['number'], name=row['name'], type=row['type'], department=department).exists():
                    skipped += 1
                    continue

                new_records.append({ "name": row['name'], "number": row['number'], "type": row['type'], "facility": row.get('facility', ''),
                "capacity": row.get('capacity', 0), "status": row.get('status', 'Available'), "floor": row.get('floor', 0), "department": department.id })

            except Exception:
                skipped += 1
                continue

        if new_records:
            lab_serializer = LabSerializers(data=new_records, many=True)
            lab_serializer.is_valid(raise_exception=True)
            lab_serializer.save()

        return Response({ "message": "Excel imported successfully", "added": len(new_records), "skipped": skipped }, status=status.HTTP_201_CREATED)
  
    @action(detail=False, methods=['get'])
    def import_page(self, request):
        college_id = request.session.get("college_id")
    
        context = {
            "detail": Details("SuperAdmin", college_id).detail(),
            "departments": Options().DeptOptions("Academic")
            }
        return render(request, "admin/Creation/labCreation.html", context)


# FOR CREATING THE LECTURES
from .serializers import LectureSerializers
from .models import Lecture
from .utils import time_per_lecture, interval_time

class lectureAPI(ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializers

    @action(detail=False, methods=['get'])
    def import_page(self, request):
        college_id = request.session.get("college_id")
        context = {
            "detail": Details("SuperAdmin", college_id).detail(),
            "courses": Options().CourseOptions()
            }
        return render(request, "admin/Creation/lectureCreation.html", context)

    @action(detail=False, methods=['get'])
    def lecture_details(self, request):
        try:
            course_id = request.GET.get("course_id")
            course = Course.objects.get(id = course_id)
            serializer = CourseSerializer(course)
            lectureTime, start, at = time_per_lecture(True)
            intervalOccur, intervalTime = interval_time(True)

            context = {
            'data': serializer.data,
            'lectureTime': lectureTime,
            'intervalOccur': intervalOccur,
            'intervalTime': intervalTime,
            'start': start,
            'at': at
            }
            return JsonResponse(context)
        
        except Exception as e : 
            return JsonResponse({'error': f"An Error Occured: {str(e)}!"})

    @action(detail=False, methods=['post'])
    def create_lectures(self, request):
        data = request.data
        new_record = []
        added = 0
        skipped = 0
        for row in data:
            course = row['course']
            semester = row['semester']
            name = row['name']
            lecture = Lecture.objects.filter(course = course, semester = semester, name = name)
            if lecture.exists():
                skipped += 1
                continue
            new_record.append(row)
            added += 1
            
        if new_record:   
            lecture_serializer = LectureSerializers(data=new_record, many=True)
            lecture_serializer.is_valid(raise_exception=True)
            lecture_serializer.save()

        return JsonResponse(
            {"message": "Lecture Created Successfully!", "added": len(new_record), "skipped":skipped},
            status=status.HTTP_201_CREATED
        )
        
# FOR CREATING THE SCHEDULES
from .models import Schedule, Lecture
from .serializers import ScheduleSerilizer
from .signals import daysName
from .utils import schedule
from .service import set_date_formate
from django.db.models import Count
from .pagination import standardPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .service import Details
from .serializers import CourseMiniSerializer

class scheduleAPI(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerilizer
    pagination_class = standardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["id", "faculty", "lecture__semester", "lecture__course"]
    search_fields = ["lab", "faculty"]
    ordering = ["id", "lecture", "day_name"]
    
    @action(detail=False, methods=['get'])
    def import_page(self, request):
        college_id = request.session.get("college_id")
        course = Course.objects.all().order_by("id")
        serializers = CourseMiniSerializer(course, many=True)
        context = {
            "detail": Details("SuperAdmin", college_id).detail(),
            "courses": serializers.data
            }
        return render(request, "admin/Creation/scheduleCreation.html", context)

    @action(detail=False, methods=['get'])
    def import_student_page(self, request):
        college_id = request.session.get("college_id")
        context = {
            "detail" :Details("Student", college_id).detail(),            
        }
        return render(request, "student/studentSchedule.html", context)

    @action(detail=False, methods=['get'])
    def course_details(self, request):
        try:
            course_id = request.GET.get('course_id')  
            course = Course.objects.get(id = course_id)
            serializers = CourseSerializer(course)
            return JsonResponse({"data": serializers.data})
        except Exception as e:
            return JsonResponse({"error": f"An Error Occured : {str(e)} !"})
        
    @action(detail=False, methods=['get'])
    def schedule_details(self, request):
      try:
        course_id = request.GET.get("course_id")
        semester = request.GET.get("semester")
        subjects = Subject.objects.filter(course = course_id, semester = semester)
        serializers = SubjectMiniSerializers(subjects, many=True)           
        context = {
            "subjects": serializers.data
            }
        return JsonResponse(context)
        
      except Exception as e:
          return JsonResponse({"error": f"An Error Occured : {str(e)}!"})

    @action(detail=False, methods=['get'])
    def slots_details(self, request):
      try:
        course_id = request.GET.get("course_id")
        semester = request.GET.get("semester")

        days = daysName(schedule(True))
        short_days = [day[:3] for day in days]

        objects = Lecture.objects.filter(course = course_id, semester = semester, type = "lecture")

        lectures = []
        for lec in objects:
            lectures.append({"id": lec.id, "slot": f"{set_date_formate(lec.start_time)}-{set_date_formate(lec.end_time)}"})

        countList = []
        for day in days:
            count = Schedule.objects.filter(lecture__course = course_id, lecture__semester = semester, day_name = day, available = False)
            countList.append(f"{count.count()}/{objects.count()}")
         
        scheduleData = []
        for i in objects:
            data_list = []
            for j in days:
                slot = Schedule.objects.filter(lecture = i.id, day_name = j).first()
                
                if slot:
                    if slot.available:
                        data_list.append({"status": True, "id": slot.id, "subjectId": slot.subject.id if slot.subject and not slot.available else 0})

                    else:
                        data_list.append({"status": False, "id": slot.id, "subjectId": slot.subject.id if slot.subject and not slot.available else 0})
                    
                else:
                    data_list.append({"status": False, "id": slot.id, "subjectId": slot.subject.id if slot.subject and not slot.available else 0})
                    
            scheduleData.append(data_list)
            
        context = {
            "days": short_days,
            "lecture": lectures,
            "scheduleData": scheduleData,
            "countList": countList
            }

        return JsonResponse(context)
      except Exception as e:
          return JsonResponse({"error": f"An Error Occured : {str(e)}!"})

    @action(detail=False, methods=['get'])
    def faculty_slot_details(self, request):
      try:
        faculty_id = request.GET.get("faculty_id") 
        lab_id = request.GET.get("lab_id")
        
        days = daysName(schedule(True))
        facultyData = []
        labData = []
        lecture = Lecture.objects.values('course').annotate(total=Count('id')) .order_by("-total").first()

        max_lectures = lecture['total']
        for lec in range(1, max_lectures+1):
            data_list = []
            lab_data_list = []
            for day in days:
                # for faculty
                if faculty_id != "":
                    f = Schedule.objects.filter(faculty = faculty_id ,day_name=day, lecture__name = f"Lecture {lec}").first()
                    if f: 
                        if f.available:           
                            data_list.append({"status": True, "id": f.id})
                        else:
                            data_list.append({"status": False, "id": f.id})              
                    else:
                        data_list.append({"status": True, "id": 0})
                else:
                    data_list.append({"status": False, "id": 0})

                # for labs 
                if lab_id != "": 
                    l = Schedule.objects.filter(lab = lab_id ,day_name=day, lecture__name = f"Lecture {lec}").first()
                    if l: 
                        if l.available:           
                            lab_data_list.append({"status": True, "id": l.id})
                        else:
                            lab_data_list.append({"status": False, "id": l.id})              
                    else:
                        lab_data_list.append({"status": True, "id": 0})
                else:
                    lab_data_list.append({"status": False, "id": 0})
            facultyData.append(data_list)
            labData.append(lab_data_list)

        context = {
            "facultyData": facultyData,
            "labData": labData,
            }

        return JsonResponse(context)
      except Exception as e:
          return JsonResponse({"error": f"An Error Occured : {str(e)}!"})

    @action(detail=False, methods=['post'])
    def reset(self, request):
        try:
            data = request.data
            course_id = data.get("course_id")
            semester = data.get("semester")
            schedule_data =Schedule.objects.all()
            
            if course_id :
                schedule_data = schedule_data.filter(lecture__course = course_id)

            if semester :
                schedule_data = schedule_data.filter(lecture__semester = semester)
      
            schedule_data.update( faculty = None, subject = None, lab = None, available = True)
            return JsonResponse({"success": f"Objects Reset SuccessFully!"})
  
        except Exception as e:
            return JsonResponse({"error": f"An Error Occurred: {str(e)}"})

def studentFine(request):
    role = request.session.get('role')
    return render(request,'student/studentFine.html',{'role':role})

def studentSendNotice(request):
    role = request.session.get('role')
    return render(request,'student/studentSendNotice.html',{'role':role})

def studentNotes(request):
    role = request.session.get('role')
    return render(request,'student/studentNotes.html',{'role':role})

def chatHistory(request):
    role = request.session.get('role')
    return render(request,'main/chatHistory.html',{'role':role})



# FOR STUDENT ASSIGNMENT
def faculty_student_assignment(request):
    return render(request, 'faculty/studentAssignment.html')

def studentAssignment(request):
    return render(request,'student/studentAssignment.html')

def studentSchedule(request):
    return render(request, 'student/studentSchedule.html')

def studentResultView(request):
    return render(request,'student/studentResultView.html')

# FOR creating subjects 
from .models import Subject
from rest_framework.viewsets import ModelViewSet
from .serializers import SubjectSerializers, SubjectMiniSerializers
from rest_framework.decorators import action
from .service import Options
class subjectCreation(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers

    @action(detail= False, methods=['get'])
    def import_page(self,request):
        college_id = request.session.get("college_id")
        context = {
            "detail": Details("SuperAdmin", college_id).detail(),
            "courses": Options().CourseOptions(),
            "departments": Options().DeptOptions("Academic")
            }
        return render(request, 'admin/Creation/subjectCreation.html', context)

    @action(detail= False, methods=['get'])
    def import_content_page(self,request):
        college_id = request.session.get("college_id")
        context = {
            "detail": Details("SuperAdmin", college_id).detail(),
            "courses": Options().CourseOptions()
            }
        return render(request, 'admin/Creation/contentCreation.html', context)
    
    @action(detail=False, methods=['get'])
    def course_details(self, request):
        try:
            course_id = request.GET.get('course_id')  
            course = Course.objects.get(id = course_id)
            serializers = CourseSerializer(course)
            return JsonResponse({"data": serializers.data})
        except Exception as e:
            return JsonResponse({"error": f"An Error Occured : {str(e)} !"})

    @action(detail=False, methods=['get'])
    def subject_details(self, request):
        try:
            course_id = request.GET.get('course_id')
            semester = request.GET.get('semester')
            subjects = Subject.objects.filter(course = course_id, semester = semester)
            serializer = SubjectMiniSerializers(subjects, many = True)
            return JsonResponse({"data": serializer.data})
        except Exception as e:
            return JsonResponse({"error": f"An Error Occured : {str(e)} !"}) 

    @action(detail= False, methods=['post'])
    def subject_create(self, request):
        data = request.data
        new_record = []
        added = 0
        skipped = 0
        for row in data:
            course = row['course']
            semester = row['semester']
            department = row['department']
            name = row['name']
            subject = Subject.objects.filter(course = course, semester = semester, department = department, name = name)
            if subject.exists():
                skipped += 1
                continue
            new_record.append(row)
            added += 1
            
        if new_record: 
            serializers = SubjectSerializers(data=new_record, many=True)
            serializers.is_valid(raise_exception=True)
            serializers.save()
        return JsonResponse({"success": "Subjects Created SuccessFully!", "data": data})


# # for faculty attendance system 
# # attendance/views.py
# from django.shortcuts import render
# from .utils import get_client_ip, is_college_wifi, personal_college_pin, valid_timing_for_qr_code
# from django.views.decorators.cache import never_cache
# from django.views.decorators.csrf import csrf_exempt

# # for wifi ip verification
# @csrf_exempt
# @never_cache
# def check_wifi_ip(request, Person):
#     ip = get_client_ip(request)
#     allowed = is_college_wifi(ip)
#     print(ip)
#     if Person == 'Faculty':
#         college_id = request.session.get('faculty_college_id')
#     elif Person == 'Admin':
#         college_id = request.session.get('admin_college_id')
#     elif Person == 'Student':
#         college_id = request.session.get('student_college_id')

#     context = {
#         "ip": ip,
#         "allowed": allowed,
#         'college_id':college_id,
#         'Person':Person,
#         'request_name':'Block'
#     }
#     now = datetime.now()
#     date = now.date()
#     attendance_detail = Faculty_and_Admin_Attedance.objects.filter(collegeID = college_id, date = date, type = Person)
#     if not attendance_detail.exists():
#         html_page = 'main/attendance/check_wifi.html'
#     else :
#         html_page = 'main/attendance/block.html'
#         context['message'] = 'Your Today Attendance Had Been Marked!'
        
#     # html_page = 'faculty/attendance/block.html'
#     # if allowed : 
#     context.pop('request_name')
#     return render(request, html_page, context)

# # for college pin verification
# @csrf_exempt
# @never_cache
# def college_pin_checking(request):
#     if request.method == 'POST':
#         try:  
#             data = json.loads(request.body) 
#             college_id = data.get('college_id')
#             Person = data.get('Person')
#             pinInput = data.get('pinInput')
#             if Person == 'Faculty':
#                 pin = personal_college_pin(True, 'Faculty')
#                 if pin != pinInput :   
#                     return JsonResponse({'error':f'Your Pin is not Correct!'})
#                 else:   
#                     return JsonResponse({'success':'Pin Match Successfully'})  
#             elif Person == 'Admin':
#                 pin = personal_college_pin(True, 'Admin')
#                 if pin != pinInput :   
#                     return JsonResponse({'error':f'Your Pin is not Correct!'})
#                 else:   
#                     return JsonResponse({'success':'Pin Match Successfully'})
#             elif Person == 'Student':
#                 pin = personal_college_pin(True, 'Student')
#                 if pin != pinInput :   
#                     return JsonResponse({'error':f'Your Pin is not Correct!'})
#                 else:   
#                     return JsonResponse({'success':'Pin Match Successfully'})   
                     
#         except Exception as e:
#             return JsonResponse({'error':f'An Error Occured {str(e)}!'})
#     else:
#         return JsonResponse({'error':'An Error Occured : Invalid Request!'})

# # FOR FACULTY AND ADMIN
# @csrf_exempt
# @never_cache
# def scan_qr_Code(request, person):
#     return render(request, 'main/attendance/scanning.html', {'person': person})

# # FOR STUDENT
# @csrf_exempt
# @never_cache
# def otp_process(request):
#     return render(request, 'main/attendance/OTP_process.html')

# for QR Code Creating
import qrcode
import time
import uuid
import os
from django.conf import settings
from io import BytesIO
import base64
from .models import QR_code
from datetime import datetime, timedelta

def generate_random_token():
    import string
    import secrets
    digits = string.digits
    return ''.join(secrets.choice(digits) for _ in range(40))

def qr_data_generator(timestamp, token, data):
    qr_data = f"ts={timestamp}&token={token}&data={data}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Generate base64 image
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Convert to base64 for embedding in HTML
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    qr_data_uri = f"data:image/png;base64,{qr_base64}"
    
    return qr_data, qr_data_uri

# from .utils import background_leave_time
# from django.utils.timezone import now
# from datetime import timedelta
# @csrf_exempt
# @never_cache
# def generate_QR_code(request):
#     # current timestamp
#     timestamp = int(time.time())
    
#     # unique token
#     token = uuid.uuid4().hex

#     # QR data - format: timestamp=...&token=...&data=...
#     data = generate_random_token()
    
#     now_time = datetime.now()
#     current_date = now_time.date()
#     current_time = now_time.time()

#     new_time = now_time + timedelta(minutes=30)
#     formated_time = new_time.strftime("%H:%M:%S")
    
#     qr_code = QR_code.objects.filter(date = current_date)

#     if qr_code.exists():
#         qr_code = qr_code.first()
#         current_time = datetime.strptime(str(current_time), '%H:%M:%S.%f')
#         set_time = datetime.strptime(str(qr_code.time), '%H:%M:%S.%f')
#         start = True
#         seconds = int(valid_timing_for_qr_code(start))*60
#         time_seconds = int(seconds) - int((current_time - set_time).total_seconds())     
#         qr_data, qr_data_uri = qr_data_generator(qr_code.timestamp, qr_code.token, qr_code.random_data)
#         if time_seconds < 0:
#             time_seconds = 0
#             qr_data = '.........................'
#         context =  {
#         "qr_data": qr_data,  # Full QR string
#         "generated_time":qr_code.date + ' ' + qr_code.time,
#         "qr_image": qr_data_uri,  # Pass base64 image
#         "random_data": data,  # Random 40 digits
#         "token": token,  # UUID token
#         "time_seconds":time_seconds
#         }

#     elif not qr_code.exists():
#         start = True
#         time_seconds = int(valid_timing_for_qr_code(start))*60
#         QR_code.objects.create(date = current_date, time = current_time, timestamp = timestamp, token = token, random_data = data, expired = False, expiry_time = str(formated_time))
#         qr_data, qr_data_uri = qr_data_generator(timestamp, token, data)
#         context =  {
#         "qr_data": qr_data,  # Full QR string
#         "generated_time": timestamp,
#         "qr_image": qr_data_uri,  # Pass base64 image
#         "random_data": data,  # Random 40 digits
#         "token": token,  # UUID token
#         "time_seconds":time_seconds
#         }

#     if request.method == 'POST':
#         leave_time = background_leave_time(True)
#         try:
#             data = json.loads(request.body)
#             completed = data.get('completed')
#             qr_code_expiry = QR_code.objects.get(date = current_date)
#             qr_code_expiry.expired = True
#             qr_code_expiry.save()
#             if completed:
#                 admin = []
#                 faculty = []
#                 message = ''
#                 if Admin.objects.exists(): 
#                     admin = Admin.objects.values_list('college_id', flat=True)
#                     for i in admin:
#                         single_admin = Faculty_and_Admin_Attedance.objects.filter(collegeID = i, date = current_date)
#                         if not single_admin.exists():     
#                             leave =  Leave.objects.filter(college_id = i, start_date__lte = current_date, end_date__gte = current_date)  
#                             if not leave.exists():
#                                 Faculty_and_Admin_Attedance.objects.create(collegeID = i ,status = 'Absent', type= 'Admin', timing = current_time, date = current_date, leave_time = 0.0)
                                
#                             if len(message) == 0:
#                                 message += 'Admin'

#                 if Faculty.objects.exists():
#                     faculty = Faculty.objects.values_list('college_id', flat=True)
#                     for j in faculty:
#                         single_faculty = Faculty_and_Admin_Attedance.objects.filter(collegeID = j, date = current_date)
#                         if not single_faculty.exists(): 
#                             leave =  Leave.objects.filter(college_id = j, start_date__lte = current_date, end_date__gte = current_date)  
#                             if not leave.exists():
#                                 Faculty_and_Admin_Attedance.objects.create(collegeID = j ,status = 'Absent', type= 'Faculty', timing = current_time, date = current_date, leave_time = 0.0)
                                
#                             if len(message) != 0:
#                                 message += ' and Faculty'
#                             else:
#                                 message +='Faculty'

#                 if len(message)!= 0 :
#                     message += ' Attendance Marked!'
#                 return JsonResponse({'success':f'{message}'}) 
                        
#         except Exception as e:
#             return JsonResponse({'error': f'An Error Occured: {str(e)}!'})
     
#     return render(request, "main/attendance/QR_code.html", context)

# # for genrating the OTP for student Attendance
# @csrf_exempt
# def  otp_creation(request):
#     return render(request, 'main/attendance/OTP.html')

# # QR verification function
# @csrf_exempt
# def verify_qr(request):
#     if request.method == "POST":
#         try:
#             import json
#             data = json.loads(request.body)
#             qr_data = data.get("qr_data", "")
#             now = datetime.now()
#             current_time = now.time()
#             current_date = now.date()
            
#             # QR code database se fetch karo
#             qr_code = QR_code.objects.filter(date=current_date)
            
#             if not qr_data:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": "No QR data received"
#                 })
            
#             # Agar database me QR code nahi hai
#             if not qr_code.exists():
#                 return JsonResponse({
#                     "status": "error",
#                     "message": "No QR code generated for today"
#                 })
            
#             qr_code = qr_code.first()
#             db_data = qr_code.random_data
#             token = qr_code.token
#             qr_time = qr_code.time
            
#             # Parse QR data
#             params = {}
#             for item in qr_data.split("&"):
#                 if "=" in item:
#                     key, value = item.split("=", 1)
#                     params[key] = value
            
#             # Check if required parameters exist
#             if "ts" not in params:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": "Missing timestamp in QR code"
#                 })
            
#             # Get timestamp
#             try:
#                 ts = int(params.get("ts", "0"))
#             except ValueError:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": "Invalid timestamp in QR"
#                 })
            
#             # Time calculation - fixed
#             current_time_obj = datetime.strptime(str(current_time), '%H:%M:%S.%f')
#             set_time_obj = datetime.strptime(str(qr_time), '%H:%M:%S.%f')
            
#             time_diff = int((current_time_obj - set_time_obj).total_seconds())
            
#             # Valid time check
#             valid_time = int(valid_timing_for_qr_code(True)) * 60
            
#             # Context dictionary initialize karo
#             context = {
#                 "timestamp": ts,
#                 "token": token,
#                 "data": db_data,
#                 "scanned_at": str(current_time)
#             }
            
#             # Time remaining calculation
#             if time_diff > 0:
#                 remaining = valid_time - time_diff
#                 if remaining < 0:
#                     remaining = 0
#                 hour = remaining // 3600
#                 minutes = (remaining % 3600) // 60
#                 seconds = remaining % 60
#                 context["time_remaining"] = f'{hour:02d}:{minutes:02d}:{seconds:02d}'
#             else:
#                 context["time_remaining"] = "00:00:00"
            
#             # Expiry check
#             if time_diff > valid_time:
#                 hour_passed = time_diff // 3600
#                 minutes_passed = (time_diff % 3600) // 60
#                 seconds_passed = time_diff % 60
#                 return JsonResponse({
#                     "status": "error",
#                     "message": f"QR Code expired ({hour_passed:02d}:{minutes_passed:02d}:{seconds_passed:02d} seconds ago)"
#                 })
            
#             # Extract data from QR
#             param_token = params.get("token", "N/A")
#             param_random_data = params.get("data", "N/A")
            
#             # Verify QR data
#             if (str(token) == param_token) and (str(db_data) == param_random_data):
#                 context['message'] = 'Attendance Marked Successfully!'
#                 context['status'] = 'success'
#             else:
#                 context['message'] = 'You are Scanning Wrong QR Code!'
#                 context['status'] = 'error'
            
#             return JsonResponse(context)
            
#         except json.JSONDecodeError:
#             return JsonResponse({
#                 "status": "error",
#                 "message": "Invalid JSON data"
#             })
#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse({
#                 "status": "error",
#                 "message": f"Server error: {str(e)}"
#             })
    
#     return JsonResponse({
#         "status": "error", 
#         "message": "Invalid request method. Use POST."
#     })
# from .models import Faculty_and_Admin_Attedance
# from. models import Attendance
# @csrf_exempt
# @never_cache
# def personal_code_verification(request, Person):
#     if Person == 'Faculty':
#         college_id = request.session.get('faculty_college_id')
#     elif Person == 'Admin':
#         college_id = request.session.get('admin_college_id')
#     elif Person == 'Student':
#         college_id = request.session.get('student_college_id')
#     if request.method == 'POST':
#         try:  
#             data = json.loads(request.body) 
#             college_id = data.get('college_id')
#             Person = data.get('Person')
#             pinInput = data.get('pinInput')
#             now = datetime.now()
#             timing = now.time()
#             date = now.date()

#             if Person == 'Faculty':
#                 faculty = Faculty.objects.get(college_id = college_id)
#                 personal_pin = faculty.personal_pin
#                 if pinInput == personal_pin:
#                     faculty_attendance = Faculty_and_Admin_Attedance.objects.filter(collegeID = college_id, type= Person, date = date)
#                     if not faculty_attendance.exists():
#                         Faculty_and_Admin_Attedance.objects.create(collegeID = college_id, status = 'Present', type= Person, timing = timing, date = date, leave_time = 0.0)
#                         return JsonResponse({'success':f'{faculty.name} {faculty.last_name} your Attendance Marked Successfully!'})
#                     else:
#                         return JsonResponse({'error':f'Your Today Attendance had been Marked!'})
#                 else:
#                     return JsonResponse({'error':'Your Pin is InCorrect!'})

#             elif Person == 'Admin':
#                 admin = Admin.objects.get(college_id = college_id)
#                 personal_pin = admin.personal_pin
#                 if pinInput == personal_pin:
#                     admin_attendance = Faculty_and_Admin_Attedance.objects.filter(collegeID = college_id, type= Person, date = date)
#                     if not admin_attendance.exists():
#                         Faculty_and_Admin_Attedance.objects.create(collegeID = college_id, status = 'Present', type= Person, timing = timing, date = date, leave_time = 0.0)
#                         return JsonResponse({'success':f'{admin.name} {admin.last_name} your Attendance Marked Successfully!'})
#                     else:
#                         return JsonResponse({'error':f'Your Today Attendance had been Marked!'})
#                 else:
#                     return JsonResponse({'error':'Your Pin is InCorrect!'})
                
#             elif Person == 'Student':
#                 student = Student.objects.get(college_id = college_id)
#                 personal_pin = student.personal_pin
#                 if pinInput == personal_pin:
#                     student_attendance = Attendance.objects.filter(college_id = college_id, date = date)
#                     if not student_attendance.exists():
#                         Attendance.objects.create(college_id = college_id, status = 'Present', time = timing, date = date, leave_time = 0.0)
#                         return JsonResponse({'success':f'{student.name} {student.last_name} your Attendance Marked Successfully!'})
#                     else:
#                         return JsonResponse({'error':f'Your Today Attendance had been Marked!'})
#                 else:
#                     return JsonResponse({'error':'Your Pin is InCorrect!'})

#         except Exception as e:
#             return JsonResponse({'error':f'An Error Occured {str(e)}!'})  
#     context = {
#         'college_id':college_id,
#         'Person':Person,
#         }
#     return render(request, 'main/attendance/biometric_verification.html',context)

# @csrf_exempt
# @never_cache
# def personal_code_creation(request,Person):
#     if Person == 'Faculty':
#         college_id = request.session.get('faculty_college_id')
#     elif Person == 'Admin':
#         college_id = request.session.get('admin_college_id')
#     elif Person == 'Student':
#         college_id = request.session.get('student_college_id')
        
#     if request.method == 'POST':
#         try:  
#             data = json.loads(request.body) 
#             college_id = data.get('college_id')
#             Person = data.get('Person')
#             pinInput = data.get('pinInput')

#             if Person == 'Faculty':
#                 faculty = Faculty.objects.get(college_id = college_id)
#                 faculty.personal_pin = str(pinInput)
#                 faculty.save()
#                 return JsonResponse({'success':f'{faculty.name} {faculty.last_name} your Personal Pin Created Successfully!'})

#             elif Person == 'Admin':
#                 admin = Admin.objects.get(college_id = college_id)
#                 admin.personal_pin = str(pinInput)
#                 admin.save()
#                 return JsonResponse({'success':f'{admin.name} {admin.last_name} your Personal Pin Created Successfully!'})

#             if Person == 'Student':
#                 student = Student.objects.get(college_id = college_id)
#                 student.personal_pin = str(pinInput)
#                 student.save()
#                 return JsonResponse({'success':f'{student.name} {student.last_name} your Personal Pin Created Successfully!'})

#         except Exception as e:
#             return JsonResponse({'error':f'An Error Occured {str(e)}!'})        
#     context = {
#         'college_id':college_id,
#         'Person':Person,
#         }
#     return render(request, 'main/attendance/personal_code_creation.html',context)

# from .serializers import LeaveSerializer
# import json
# from datetime import datetime
# from django.utils import timezone
# from .pagination import LeavePagination
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from .utils import leaves_limit

# def leave_request_making(request, Person):
#     role = request.session.get('role')
    
#     if Person == 'Faculty':
#         college_id = request.session.get('faculty_college_id')
#         detail = Faculty.objects.get(college_id=college_id)
#         name = f'{detail.name} {detail.last_name}'
#         # position = f'{detail.position.name-{detail.position.level}'
#         department = f'{detail.department.name}'

#     if Person == 'Admin':
#         college_id = request.session.get('admin_college_id')
#         detail = Admin.objects.get(college_id=college_id)
#         name = f'{detail.name} {detail.last_name}'
#         # position = f'{detail.position.name-{detail.position.level}'
#         department = f'{detail.department.name}'
        
#     leaves = Leave.objects.filter(college_id=college_id)
#     total_applied = leaves.count()
#     pending = leaves.filter(status = 'Pending').count()
#     approved = leaves.filter(status = 'Approved').count()
#     rejected = leaves.filter(status = 'Rejected').count()
#     leave_days = leaves_limit(True)
#     used_days = approved
#     percentage = (used_days/leave_days)*100
#     leaves = leaves.order_by("applied_on")[:5]

#     if request.method == 'POST':
#       try:
#         form_data = json.loads(request.body)
#         college_id = form_data.get('college_id')
        
        
#         if college_id and college_id[0:2] == 'GK':
#             try:
#                 user = Faculty.objects.get(college_id=college_id)
#                 # Get ContentType object
#                 content_type_obj = ContentType.objects.get_for_model(user)
#                 # Use the ID (pk) instead of object
#                 content_type_id = content_type_obj.id
#             except Faculty.DoesNotExist:
#                 return JsonResponse({'error': 'Faculty not found'}, status=404)
#         else:
#             return JsonResponse({'error': 'Invalid college ID format'}, status=400)
        
#         # Convert string dates to Date objects
#         try:
#             start_date = datetime.strptime(form_data.get('startDate'), '%Y-%m-%d').date() if form_data.get('startDate') else None
#             end_date = datetime.strptime(form_data.get('endDate'), '%Y-%m-%d').date() if form_data.get('endDate') else None
#         except ValueError as e:
#             return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
#         # Map form fields to model fields - use content_type_id instead of content_type_obj
#         leave_data = {
#             'content_type': content_type_id,  # CHANGED: Use ID instead of object
#             'college_id': form_data.get('college_id', '').strip(),
#             'subject': form_data.get('leaveSubject', '').strip(),
#             'start_date': start_date,
#             'end_date': end_date,
#             'department': user.department.id,
#             'total_days': int(form_data.get('totalDays', 0)),
#             'leave_type': form_data.get('leaveType', '').strip(),
#             'contact_during_leave': form_data.get('contactNumber', '').strip(),
#             'reason': form_data.get('leaveReason', '').strip(),
#             'status': 'Pending',
#             'leave_time': float(form_data.get('leaveTime', 0))
#         }
        
#         serializer = LeaveSerializer(data=leave_data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'success': 'Leave application submitted successfully!'}, status=201)
#         else:
#             print(serializer.errors)
#             return JsonResponse({'error': serializer.errors}, status=400)
            
#       except json.JSONDecodeError as e:
#         return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#       except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return JsonResponse({'error': str(e)}, status=500)
    
#     context = {
#         'role': role,
#         'college_id': college_id,
#         'name': name,
#         # 'position': position,
#         'department': department,
#         'leaves': leaves, 
#         'total_applied': total_applied,
#         'pending': pending,
#         'approved': approved,
#         'rejected': rejected,
#         'leave_days': leave_days,
#         'used_days': used_days,
#         'percentage': percentage
#     }
#     return render(request, 'main/attendance/leave.html', context)

# @api_view(['GET'])
# def leave_details(request):
#     if request.method == 'GET':
#         try:
#             college_id = request.GET.get('college_id')
#             queryset = Leave.objects.filter(college_id = college_id).order_by("-applied_on")
#             search = request.GET.get("search")
#             if search:
#                 queryset = queryset.filter(
#                     Q(leave_type__icontains = search) |
#                     Q(subject__icontains = search) |
#                     Q(start_date__icontains = search)|
#                     Q(end_date__icontains = search) |
#                     Q(status__icontains = search)
#                     )
#             status = request.GET.get("status")
#             if status:
#                 queryset = queryset.filter(status = status)
#             paginator = LeavePagination()
#             paginated_queryset = paginator.paginate_queryset(queryset, request)
#             serializer = LeaveSerializer(paginated_queryset, many=True)
#             return paginator.get_paginated_response(serializer.data)     
            
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)         
            
# def admin_leave_page(request):
#     role = request.session.get('role')
#     admin_college_id = request.session.get('admin_college_id')
#     now = datetime.now()
#     admin_ct = ContentType.objects.get_for_model(Admin)
#     faculty_ct = ContentType.objects.get_for_model(Faculty)
#     today_leaves = Leave.objects.filter(applied_on=now.date())
#     today_leaves = today_leaves.filter(content_type__in=[admin_ct, faculty_ct])
#     pending_leaves = today_leaves.filter(status='Pending').count()
#     this_month_leaves = Leave.objects.filter(applied_on__month=now.month, applied_on__year=now.year)
#     this_month_leaves = this_month_leaves.filter(content_type__in=[admin_ct, faculty_ct])
#     this_month_approved_leaves = this_month_leaves.filter(status='Approved')
#     approval_rate = (this_month_approved_leaves.count()/this_month_leaves.count())*100

#     total_leaves = Leave.objects.all()
#     total_leaves = total_leaves.filter(content_type__in=[admin_ct, faculty_ct])
#     total_pending = total_leaves.filter(status = 'Pending').count()
#     total_approved = total_leaves.filter(status = 'Approved').count()
#     total_rejected = total_leaves.filter(status = 'Rejected').count()

#     departments = Department.objects.all().order_by('id')

#     context = {
#         'role':role,
#         'college_id':admin_college_id,
#         'today_leaves':today_leaves.count(),
#         'pending_leaves':pending_leaves,
#         'this_month_leaves':this_month_leaves.count(),
#         'approval_rate':approval_rate,
#         'total_leaves':total_leaves.count(),
#         'total_pending':total_pending,
#         'total_approved':total_approved,
#         'total_rejected':total_rejected,
#         'departments':departments
#         }

#     return render(request, 'admin/admin_leave_checking.html', context)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.utils.dateparse import parse_date
# @api_view(['GET'])
# def admin_leave_api(request):
#     if request.method == 'GET':
#         try:
#             # Yeh line change karo - pehle hi order_by add karo
#             queryset = Leave.objects.all().order_by('applied_on')  # <-- IMPORTANT

#             search = request.GET.get('search')
#             if search:
#                queryset = queryset.filter(
#                    Q(college_id__icontains = search)|
#                    Q(leave_type__icontains = search)|
#                    Q(status__icontains = search)
#                    )

#             # filteration
#             status = request.GET.get('status')
#             department = request.GET.get('department')
#             from_date = request.GET.get('from_date')
#             to_date = request.GET.get('to_date')
            
#             if status:
#                 queryset = queryset.filter(status__iexact = status)

#             if department:
#                 admin_college_ids = Admin.objects.filter(department_id=department).values_list('college_id', flat=True)
#                 faculty_college_ids = Faculty.objects.filter(department_id=department).values_list('college_id', flat=True)
#                 queryset = queryset.filter(college_id__in=list(admin_college_ids) + list(faculty_college_ids))

#             if from_date and to_date:
#                       # Django ka built-in parse_date use karo
#                     from_date_obj = parse_date(from_date)
#                     to_date_obj = parse_date(to_date)
    
#                     if from_date_obj and to_date_obj:
#                      # Simple date range filter
#                         queryset = queryset.filter(applied_on__date__range=[from_date_obj, to_date_obj])
#             # pagination
#             paginator = LeavePagination()
#             paginated_queryset = paginator.paginate_queryset(queryset, request)
#             serializer = LeaveSerializer(paginated_queryset, many=True)
#             return paginator.get_paginated_response(serializer.data)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

# @api_view(['GET', 'PATCH', 'DELETE', 'PUT'])   
# def admin_leave_api_view(request, id):
#     if request.method == 'GET':
#         try:       
#             leave = Leave.objects.get(id=id)
#             serializer = LeaveSerializer(leave)
#             return JsonResponse(serializer.data)
#         except Leave.DoesNotExist:
#             return JsonResponse({'error': "No Leave Found !"})
#         except Exception as e:
#             return JsonResponse({'error': f"An Error Occured: {str(e)} !"})

#     if request.method in ['PATCH', 'PUT']:
#         try:
#             leave = Leave.objects.get(id=id)
#             data = request.data.copy()
            
#             # If updating status, use admin_response field
#             if 'status' in data:
#                 data['admin_response'] = data['status']
                
#             serializer = LeaveSerializer(leave, data=data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse({'success': "Leave response Updated Successfully!"})
#             return JsonResponse({'error': serializer.errors}, status=400)
            
#         except Leave.DoesNotExist:
#             return JsonResponse({'error': "No Leave Found !"})
#         except Exception as e:
#             return JsonResponse({'error': f"An Error Occured: {str(e)} !"})

#     if request.method == 'DELETE':
#         try:
#             leave = Leave.objects.get(id=id)
            
#             # Check if leave can be deleted (only pending leaves can be deleted)
#             if leave.status != 'Pending':
#                 return JsonResponse({'error': "Only pending leaves can be cancelled!"}, status=400)
                
#             cancellation_reason = request.data.get('cancellation_reason', '')
#             leave.delete()
#             return JsonResponse({'success': "Leave Cancelled Successfully!"})
#         except Leave.DoesNotExist:
#             return JsonResponse({'error': "No Leave Found !"})
#         except Exception as e:
#             return JsonResponse({'error': f"An Error Occured: {str(e)} !"})









# redis practise

