from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Student, Faculty, Course, Attendance,Admin, FeeStructure, FeePayment,StudentBalance # Import the new Attendance model
from django.http import JsonResponse
import json # For handling JSON data from AJAX requests
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from decimal import Decimal

# function of front page 
def home(request):
    return render(request,'Home/home.html')

def feature(request):
    return render(request,'Home/feature.html')

def success_stories(request):
    return render(request,'Home/success_stories.html')

def contact(request):
    return render(request,'Home/contact.html')

def pricing(request):
    return render(request,'Home/pricing.html')

def demo(request):
    return render(request,'Home/demo.html')

def enroll(request):
    return render(request,'Home/enroll.html')

def new_enroll(request):
    return render(request,'Home/new_enroll.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_id=request.POST.get('userId')
        role = request.POST.get('role')
       
        if not username or not password or not role or not user_id:
            messages.error(request, "Please fill all the fields")
            return redirect('login')
        
        if role == 'admin':
            try:
                
             admin_email = Admin.objects.all().values_list('email',flat=True)
             if (username in admin_email) :
                admin_detail = Admin.objects.get(email=username)
                user_id = admin_detail.college_id
                admin_phone = admin_detail.phone
                
                if (password==admin_phone and user_id == user_id):
                    request.session['username1'] =  str(admin_detail.name) + " " + str(admin_detail.last_name)
                    request.session['admin_college_id']= user_id 
                    request.session['role'] = role
                    return redirect('dashboard')
                 
                else:
                  messages.error(request, "Invalid admin credentials")
                  return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
                
                
        elif role == 'faculty':
            try:
                faculty_email = Faculty.objects.all().values_list('email', flat=True)
                if username in faculty_email:
                    faculty_detail=Faculty.objects.get(email=username)
                    faculty_college_id=faculty_detail.college_id
                    faculty_phone=faculty_detail.phone
                    if password==faculty_phone and user_id == faculty_college_id:
                       request.session['username2'] =  faculty_detail.name
                       request.session['faculty_college_id']= faculty_college_id
                       request.session['role'] = role
                       return redirect('dashboard1')
                    else:
                       messages.error(request, "Invalid faculty credentials")
                       return redirect('login')
                else:
                    messages.error(request, "Invalid faculty credentials")
                    return redirect('login')
                    
            except Student.DoesNotExist:
                messages.error(request, "Faculty not found")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
                
        elif role == 'student':
            try:
                student_emails = Student.objects.all().values_list('email', flat=True)
                if username in student_emails:
                    student_detail=Student.objects.get(email=username)
                    student_phone=student_detail.phone
                    student_college_id=student_detail.college_id
                    if password == student_phone and user_id == student_college_id:
                      request.session['username3'] = student_detail.name
                      request.session['student_college_id'] = student_college_id
                      request.session['role'] = role
                      return redirect('dashboard2')
                    else:
                      messages.error(request, "Invalid student credentials")
                      return redirect('login')
                else:
                    messages.error(request, "Invalid student credentials")
                    return redirect('login')
                    
            except Student.DoesNotExist:
                messages.error(request, "Student not found")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
    
    return render(request, 'Home/login.html')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        college_id = request.POST.get('collegeId')
        
        if not college_id:
            return JsonResponse({
                'success': False,
                'error': 'College ID is required'
            }, status=400)
        
        try:
            # Check if college_id starts with specific prefixes
            if college_id.startswith('ST'):
                student_detail = Student.objects.get(college_id=college_id)
                return JsonResponse({
                    'success': True,
                    'username': student_detail.email,  # Using email as username
                    'user_id': student_detail.college_id,
                    'password': student_detail.phone  # Phone is being used as password
                })
            elif college_id.startswith('GK'):
                faculty_detail = Faculty.objects.get(college_id=college_id)
                return JsonResponse({
                    'success': True,
                    'username': faculty_detail.email,  # Using email as username
                    'user_id': faculty_detail.college_id,
                    'password': faculty_detail.phone  # Phone is being used as password
                })
            elif college_id.startswith('AD'):
                admin_detail = Admin.objects.get(college_id=college_id)
                return JsonResponse({
                    'success': True,
                    'username': admin_detail.email,  # Using email as username
                    'user_id': admin_detail.college_id,
                    'password': admin_detail.phone  # Phone is being used as password
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid College ID format'
                }, status=400)
                
        except Student.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Student not found with this College ID'
            }, status=404)
        except Faculty.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Faculty not found with this College ID'
            }, status=404)
        except Admin.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Admin not found with this College ID'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            }, status=500)
    
    # For GET requests or other methods
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method. Use POST.'
    }, status=400)

def admin_adding_page(request):
    role = request.session.get('role')
    username = request.session.get('User_name')
    return render(request,'admin/admin_page.html',{'username':username,'role':role})

def admin_card(request):
    role = request.session.get('role')
    username = request.session.get('User_name')
    admin_details = Admin.objects.all()
    return render(request,'admin/admin_card.html',{'username':username,'admin_details':admin_details,'role':role})

# profile details   
def profile_details(request):
    role = request.session.get('role')

    if role == 'faculty':
        faculty_id=request.session.get('faculty_college_id')
        details=Faculty.objects.get(college_id=faculty_id)
        return render(request,'main/profile.html',{'faculty':details,'role':role})
    elif role == 'student':
        student_id=request.session.get('student_college_id')
        details=Student.objects.get(college_id=student_id)
        return render(request,'main/profile.html',{'student':details,'role':role})
    elif role == 'admin':
        admin_id=request.session.get('admin_college_id')
        details=Admin.objects.get(college_id=admin_id)
        return render(request,'main/profile.html',{'admin':details,'role':role})

# for uploading picture 
def profile_upload(request):
    role = request.session.get('role')
    if role == 'student':
        try:
            student = Student.objects.get(college_id=request.session.get('student_college_id'))
        except Student.DoesNotExist:
            return redirect('dashboard2')
        
        if request.method == 'POST' and 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
            student.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile_details')
        
    elif role == 'faculty':
        try:
            faculty = Faculty.objects.get(college_id=request.session.get('faculty_college_id'))
        except Faculty.DoesNotExist:
            return redirect('dashboard1')
        
        if request.method == 'POST' and 'profile_picture' in request.FILES:
            faculty.profile_picture = request.FILES['profile_picture']
            faculty.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile_details')
    elif role == 'admin':
        try:
            admin = Admin.objects.get(college_id=request.session.get('admin_college_id'))
        except Admin.DoesNotExist:
            return redirect('dashboard')
        
        if request.method == 'POST' and 'profile_picture' in request.FILES:
            admin.profile_picture = request.FILES['profile_picture']
            admin.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile_details')
    
# for id card
def id_card(request):
    role=request.session.get('role')
    context = {}
    context['role'] = role
    
    try:
        # Check user type and add appropriate details to context
        if role == 'student':
            student = Student.objects.get(college_id=request.session.get('student_college_id'))
            context['detail'] = student
            context['user_type'] = 'Student'
        elif role == 'faculty':
            faculty = Faculty.objects.get(college_id=request.session.get('faculty_college_id'))
            context['detail'] = faculty
            context['user_type'] = 'Faculty'
        elif role == 'admin':
            admin = Admin.objects.get(college_id=request.session.get('admin_college_id'))
            context['detail'] = admin
            context['user_type'] = 'Admin'
            
    except (Student.DoesNotExist, Faculty.DoesNotExist,Admin.DoesNotExist):
        return redirect('logoutdoor')
    
    return render(request, 'main/id_card.html', context)

# for admin dashboard
def dashboard_view(request):
    # Check if the user is logged in
    role = request.session.get('role')
    username = request.session.get('username1')
    college_id = request.session.get('admin_college_id')
    if username:
        return render(request, 'dashboard/dashboard.html', {'username': username,'college_id':college_id,'role':role})
    else:
        return redirect('login') 

# for faculty dashboard
def dashboard1(request):
    # Check if the user is logged in
    role = request.session.get('role')
    username = request.session.get('username2')  # Retrieve username from session
    if username:
        return render(request, 'dashboard/dashboard1.html', {'username': username,'role':role})
    else:
        return redirect('login')  # Redirect to login if not logged in

# for student dashboard
def dashboard2(request):
    # Check if the user is logged in
    role = request.session.get('role')
    username = request.session.get('username3')
    college_id = request.session.get('student_college_id')
    detail = Student.objects.get(college_id = college_id)  # Retrieve username from session
    if username:
        return render(request, 'dashboard/dashboard2.html', {'username': username,'detail':detail,'role':role, 'college_id':college_id})
    else:
        return redirect('login') 

# for logout from account
def logout_view(request):
    # Clear session data
    request.session.flush()
    return redirect('login')

from .models import StudentDocuments, AdminDocuments, FacultyDocuments
# for single students operations 
def student_functions(request):
    context = {}
    role = request.session.get('role')
    context['role'] = role
    context['course'] = Course.objects.all()
    context['level'] = Level.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        # Add student
        if action == "add":
            try:
                # Generate college ID
                max_id = Student.objects.aggregate(max_id=models.Max('college_id'))['max_id']
                
                if max_id is None:
                    college_id = 'ST20250'  # Initial ID
                else:
                    try:
                        # Extract numeric part and increment
                        numeric_part = int(max_id[2:])  # Remove 'ST' prefix
                        college_id = f'ST{numeric_part + 1}'
                    except (ValueError, IndexError):
                        college_id = 'ST20250'  # Fallback if format is wrong
                
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                
                # Convert tenth and twelfth percent to Decimal
                tenth_percent = Decimal(request.POST.get("tenthgpa", 0))
                twelfth_percent = Decimal(request.POST.get("twelthgpa", 0))
                
                # Convert adhar_no to BigInteger
                adhar_no = int(request.POST.get("adharno", 0))
                
                Student.objects.create(
                    college_id=college_id,
                    name=request.POST.get("name"),
                    last_name=request.POST.get("lastName"),
                    father_name=request.POST.get("fathername"),
                    mother_name=request.POST.get('mothername'),
                    occupation=request.POST.get('occupation'),
                    income=request.POST.get('income'),
                    email=email,
                    phone=phone,
                    other_phone_no=request.POST.get("otherphone"),
                    gender=request.POST.get("gender"),
                    course_id=request.POST.get("course"),
                    level_id=request.POST.get("education"),
                    birthday=request.POST.get("birthday"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    state=request.POST.get("state"),
                    state_code=request.POST.get("zipcode"),
                    date_of_joining=request.POST.get("startDate"),
                    tenth_percent=tenth_percent,
                    twelfth_percent=twelfth_percent,
                    adhar_no=adhar_no,
                    pan_no=request.POST.get("panno"),
                    family_id=request.POST.get("familyid"),
                    family_id_phone_no=request.POST.get("familyidphone"),
                    category=request.POST.get("caste"),
                    nationality=request.POST.get("nationality"),
                    religion=request.POST.get("religion"),
                    martial_status=request.POST.get("martialstatus"),
                    user_id=college_id, 
                    username=email,
                    password=phone,
                    semester=1,  # Default value
                    year=1,     # Default value
                    country="India"  # Default value
                )
                detail = Student.objects.get(college_id = college_id)
                StudentDocuments.objects.create(student = detail ,pic1 = None, pic2 = None, pic3 = None,
                pic4 = None, pic5 = None, pic6 = None, pic7 = None, pic8 = None, pic9 = None)
                messages.success(request, f"Student added successfully with ID: {college_id}!")
                return redirect(reverse('student_function') + '?success=true')  # Redirect to avoid form resubmission
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        # View student
        elif action == "view":
            college_id = request.POST.get("college_id")
            try:
                student = Student.objects.get(college_id=college_id)
                context["student"] = student
            except Student.DoesNotExist:
                messages.error(request, "No student found with this college ID.")

        # Delete student
        elif action == "delete":
            college_id = request.POST.get("college_id")
            try:
                student = Student.objects.get(college_id=college_id)
                student.delete()
                messages.success(request, "Student deleted successfully.")
                return redirect('student_function')  # Redirect to avoid form resubmission
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

        # Alter student
        elif action == "alter":
            try:
                student = Student.objects.get(college_id=request.POST.get("college_id"))
                student.name = request.POST.get("name")
                student.last_name = request.POST.get("lastName")
                student.father_name = request.POST.get("father_name")
                student.mother_name = request.POST.get("mother_name")
                student.email = request.POST.get("email")
                student.phone = request.POST.get("phone")
                student.other_phone_no = request.POST.get("other_phone")
                student.address = request.POST.get("address")
                student.city = request.POST.get("city")
                student.state = request.POST.get("state")
                student.state_code = request.POST.get("state_code")
                student.save()
                messages.success(request, "Student details updated successfully.")
                return redirect('student_function')  # Redirect to avoid form resubmission
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    return render(request, "student/student_page.html", context)
# for  faculty management
from django.db import models
def faculty_functions(request):
    context = {}
    role = request.session.get('role')
    context['role'] = role
    context['position'] = Position.objects.filter(role = 'Faculty')
    context['department'] = Department.objects.filter(type = 'Faculty')
    if request.method == "POST":
        action = request.POST.get("action")

        # Add faculty
        if action == "add":
            try:
                # Auto-generate employee ID
                max_id = Faculty.objects.aggregate(max_id=models.Max('college_id'))['max_id']
                
                if max_id is None:
                    college_id = 'GK20250'  # Initial ID
                else:
                    try:
                        # Extract numeric part and increment
                        numeric_part = int(max_id[2:])  # Remove 'GK' prefix
                        college_id = f'GK{numeric_part + 1}'
                    except (ValueError, IndexError):
                        college_id = 'GK20250'  # Fallback if format is wrong
                email = request.POST.get("email")
                phone =  request.POST.get("phone") 
                adhar_no = int(request.POST.get("adharno", 0))       
                # Create faculty with all required fields
                Faculty.objects.create(
                    college_id=college_id,
                    name=request.POST.get("name"),
                    last_name=request.POST.get("lastName"),
                    father_name=request.POST.get("fathername"),
                    mother_name=request.POST.get("mothername"),
                    email=email,
                    phone=phone,
                    other_phone_no=request.POST.get("otherphone"),
                    position_id=request.POST.get("position"),
                    gender=request.POST.get("gender"),
                    department_id=request.POST.get("department"),
                    qualification=request.POST.get("qualification"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    state=request.POST.get("state"),
                    state_code=request.POST.get("zipcode"),
                    date_of_joining=request.POST.get("startDate"),
                    experience=request.POST.get("experience"),
                    birthday=request.POST.get("birthday"),
                    category=request.POST.get("caste"),
                    nationality=request.POST.get("nationality", "Indian"),
                    religion=request.POST.get("religion"),
                    adhar_no=adhar_no,
                    pan_no=request.POST.get("panno"),
                    martial_status=request.POST.get("martialstatus"),
                    user_id=college_id, 
                    username=email,
                    password=phone,
                    country='India'
                )
                detail = Faculty.objects.get(college_id = college_id)
                FacultyDocuments.objects.create(faculty = detail ,pic1 = None, pic2 = None, pic3 = None,
                pic4 = None, pic5 = None)
                messages.success(request, F"Faculty added successfully with ID: {college_id}!")
            except Exception as e:
                messages.error(request, f"Error adding faculty: {str(e)}")

        # View faculty
        elif action == "view":
            college_id = request.POST.get("college_id")
            try:
                faculty = Faculty.objects.get(college_id=college_id)
                context["faculty"] = faculty
            except Faculty.DoesNotExist:
                messages.error(request, "No faculty found with this ID.")
            except Exception as e:
                messages.error(request, f"Error viewing faculty: {str(e)}")

        # Delete faculty
        elif action == "delete":
            college_id = request.POST.get("college_id")
            try:
                faculty = Faculty.objects.get(college_id=college_id)
                faculty.delete()
                messages.success(request, "Faculty deleted successfully.")
            except Faculty.DoesNotExist:
                messages.error(request, "Faculty not found.")
            except Exception as e:
                messages.error(request, f"Error deleting faculty: {str(e)}")

        # Alter faculty
        elif action == "alter":
            college_id = request.POST.get("college_id")
            try:
                faculty = Faculty.objects.get(college_id=college_id)
                
                # Update all fields
                faculty.name = request.POST.get("name")
                faculty.last_name = request.POST.get("lastName")
                faculty.father_name = request.POST.get("father_name")
                faculty.mother_name = request.POST.get("mother_name")
                faculty.email = request.POST.get("email")
                faculty.phone = request.POST.get("phone")
                faculty.other_phone_no = request.POST.get("other_phone")
                faculty.address = request.POST.get("address")
                faculty.city = request.POST.get("city")
                faculty.state = request.POST.get("state")
                faculty.state_code = request.POST.get("state_code") 
                faculty.save()
                messages.success(request, "Faculty details updated successfully.")
            except Faculty.DoesNotExist:
                messages.error(request, "Faculty not found.")
            except Exception as e:
                messages.error(request, f"Error updating faculty: {str(e)}")

    return render(request, "faculty/faculty_page.html", context)


# For admin management 
from django.contrib.auth.models import User
# for functions related to admin
def admin_functions(request):
    context = {}
    role = request.session.get('role')
    context['role'] = role
    context['position'] = Position.objects.filter(role = 'Admin')
    context['department'] = Department.objects.filter(type = 'Admin')

    if request.method == "POST":
        action = request.POST.get("action")

        # Add admin
        if action == "add":
            try:
                # Auto-generate employee ID
                max_id = Admin.objects.aggregate(max_id=models.Max('college_id'))['max_id']
                
                if max_id is None:
                    college_id = 'AD20251'  # Initial ID
                else:
                    try:
                        # Extract numeric part and increment
                        numeric_part = int(max_id[2:])  # Remove 'GK' prefix
                        college_id = f'AD{numeric_part + 1}'
                    except (ValueError, IndexError):
                        college_id = 'AD20251'  # Fallback if format is wrong
                email = request.POST.get("email")
                phone =  request.POST.get("phone")  
                adhar_no = int(request.POST.get("adharno", 0))       
                # Create admin with all required fields
                Admin.objects.create(
                    college_id=college_id,
                    name=request.POST.get("name"),
                    last_name=request.POST.get("lastName"),
                    father_name=request.POST.get("fathername"),
                    mother_name=request.POST.get("mothername"),
                    email=email,
                    phone=phone,
                    other_phone_no=request.POST.get("otherphone"),
                    position_id=request.POST.get("position"),
                    gender=request.POST.get("gender"),
                    department_id=request.POST.get("department"),
                    qualification=request.POST.get("qualification"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    state=request.POST.get("state"),
                    state_code=request.POST.get("zipcode"),
                    country=request.POST.get("country", "India"),
                    date_of_joining=request.POST.get("startDate"),
                    experience=request.POST.get("experience"),
                    birthday=request.POST.get("birthday"),
                    category=request.POST.get("caste"),
                    nationality=request.POST.get("nationality", "Indian"),
                    religion=request.POST.get("religion"),
                    adhar_no=adhar_no,
                    pan_no=request.POST.get("panno"),
                    martial_status=request.POST.get("martialstatus"),
                    user_id=college_id, 
                    username=email,
                    password=phone,
                )
                User.objects.create_user(username=email,password=phone,is_staff=True,is_superuser=True)
                detail = Admin.objects.get(college_id = college_id)
                AdminDocuments.objects.create(admin = detail ,pic1 = None, pic2 = None, pic3 = None,
                pic4 = None, pic5 = None)
                messages.success(request, f"Admin added successfully with ID {college_id}!")
            except Exception as e:
                messages.error(request, f"Error adding admin: {str(e)}")

        # View admin
        elif action == "view":
            college_id = request.POST.get("college_id")
            try:
                admin = Admin.objects.get(college_id=college_id)
                context["admin"] = admin
            except Admin.DoesNotExist:
                messages.error(request, "No admin found with this ID.")
            except Exception as e:
                messages.error(request, f"Error viewing admin: {str(e)}")

        # Delete admin
        elif action == "delete":
            college_id = request.POST.get("college_id")
            try:
                admin = Admin.objects.get(college_id=college_id)
                admin_profile = get_object_or_404(User,username=college_id)

                admin_profile.delete()
                admin.delete()
                messages.success(request, "Admin deleted successfully.")
            except Admin.DoesNotExist:
                messages.error(request, "Admin not found.")
            except Exception as e:
                messages.error(request, f"Error deleting admin: {str(e)}")

        # Alter admin
        elif action == "alter":
            college_id = request.POST.get("college_id")
            try:
                admin = Admin.objects.get(college_id=college_id)
                
                # Update all fields
                admin.name = request.POST.get("name")
                admin.last_name = request.POST.get("lastName")
                admin.father_name = request.POST.get("father_name")
                admin.mother_name = request.POST.get("mother_name")
                admin.email = request.POST.get("email")
                admin.phone = request.POST.get("phone")
                admin.other_phone_no = request.POST.get("other_phone")
                admin.address = request.POST.get("address")
                admin.city = request.POST.get("city")
                admin.state = request.POST.get("state")
                admin.state_code = request.POST.get("state_code")
                
                admin.save()
                messages.success(request, "Admin details updated successfully.")
            except Admin.DoesNotExist:
                messages.error(request, "Admin not found.")
            except Exception as e:
                messages.error(request, f"Error updating admin: {str(e)}")

    return render(request, "admin/admin_page.html", context)

#  for multiple student filtering
from django.template.loader import render_to_string
from django.core.paginator import Paginator
def course_details(request, template):
    role = request.session.get('role')

    try:
        # Get all courses from Course model (not from Student records)
        if template != 'chat/page2.html':
            courses = Course.objects.all().values_list('name', 'level__name', 'course_id')
            students = Student.objects.all()
            page_obj = None
            data = []
            # for fit the course in data
            for i in courses:
                data.append({'name': str(i[0]) + ' with ' + str(i[1]), 'course_id':i[2]})
                
            if template == 'feeStructureCreation.html':
                values = FeeStructure.objects.all().order_by("structure_id")
                paginator = Paginator(values, 1)  # Changed from 1 to reasonable number
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
                
                # for ajax working
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    data = []
                    for i in page_obj:
                        data.append({
                            'structure_id': i.structure_id, 
                            'course': i.course, 
                            'year': i.year, 
                            'semester': i.semester, 
                            'due_date': i.due_date.strftime("%Y-%m-%d"), 
                            'batch': i.batch, 
                            'amount': i.amount
                        })
                    return JsonResponse({
                        "data1": data, 
                        "has_next": page_obj.has_next(), 
                        "has_prev": page_obj.has_previous(),
                        "page_number": page_obj.number, 
                        "total_pages": paginator.num_pages  # Fixed variable name
                    })
                    
            return render(request, template, {
                'data': data, 
                'students': students, 
                'role': role, 
                'page_obj': page_obj
            })
        else:
            courses = Course.objects.all().values_list('name', flat=True)
            faculty = Faculty.objects.get(college_id=request.session['faculty_college_id'])
            students = Student.objects.filter(followed_faculty=faculty)
            return render(request, 'chat/page2.html', {
                'faculty': faculty,
                'courses': courses, 
                'students': students, 
                'role': role  # Removed duplicate 'role' parameter
            })

    except Exception as e:
        messages.error(request, f"Error loading courses: {str(e)}")
        return render(request, template, {
            'courses': [],
            'students': [], 
            'faculty': [], 
            'role': role,
            'page_obj': []  # Added missing page_obj for error case
        })
        
def get_courses_details(request):
   
    try:
      if request.method == 'POST':
        data = json.loads(request.body)
        course_name = data.get('course_name')
        if not course_name or course_name == 'all':
            return JsonResponse({'error': 'Please select a valid course'}, status=400)
            
        # Get the course - make sure name matching is case-insensitive
        course = Course.objects.filter(name__iexact=course_name).first()
        if not course:
            return JsonResponse({'error': f'Course "{course_name}" not found'}, status=404)
            
        return JsonResponse({
            'years': list(range(1, course.no_of_years + 1)),
            'semesters': list(range(1, course.no_of_semesters + 1)),
        })
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
def filtered_students(request, template):
    try:
        filters = {
            'course': request.GET.get('course', 'all'),
            'year': request.GET.get('year', 'all'),
            'semester': request.GET.get('semester', 'all'),
            'college_id': request.GET.get('college_id', '')
        }
        
        # Check which template we're using to determine the base queryset
        if template != 'chat/student_list_partial.html':
            students = Student.objects.all()
            
        else:
            faculty = Faculty.objects.get(college_id=request.session['faculty_college_id'])
            students = Student.objects.filter(followed_faculty=faculty)
        
        # Apply filters
        if filters['course'] != 'all':
            students = students.filter(course=filters['course'])
        if filters['year'] != 'all':
            students = students.filter(year=filters['year'])
        if filters['semester'] != 'all':
            students = students.filter(semester=filters['semester'])
        if filters['college_id']:
            students = students.filter(college_id__icontains=filters['college_id'])
            
        if template == 'bulkActions/student/studentFilterResult.html':
            # Pagination
            page = request.GET.get('page', 1)
            paginator = Paginator(students, 5)  # Show 10 students per page
        
            try:
                 students_page = paginator.page(page)
            except PageNotAnInteger:
                 students_page = paginator.page(1)
            except EmptyPage:
                students_page = paginator.page(paginator.num_pages)
            
            html = render_to_string(template, {'students': students_page})
            # Generate pagination HTML
            pagination_html = ''
            if paginator.num_pages > 1:
                pagination_html = '<div class="pagination">'
                if students_page.has_previous():
                    pagination_html += f'<button class="page-link" data-page="1"><i class="fas fa-angle-double-left"></i></button>'
                    pagination_html += f'<button class="page-link" data-page="{students_page.previous_page_number()}"><i class="fas fa-angle-left"></i></button>'
            
                for i in range(1, paginator.num_pages + 1):
                    if i == students_page.number:
                        pagination_html += f'<button class="page-link active" data-page="{i}">{i}</button>'
                    else:
                        pagination_html += f'<button class="page-link" data-page="{i}">{i}</button>'
            
                if students_page.has_next():
                    pagination_html += f'<button class="page-link" data-page="{students_page.next_page_number()}"><i class="fas fa-angle-right"></i></button>'
                    pagination_html += f'<button class="page-link" data-page="{paginator.num_pages}"><i class="fas fa-angle-double-right"></i></button>'
            
                pagination_html += '</div>'
            
            return JsonResponse({
               'html': html,
               'pagination': pagination_html,
               'total_pages': paginator.num_pages
        })
            
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    html = render_to_string(template, {'students': students})
    return JsonResponse({'html': html})


def filtered_student(request):
    try:
        filters = {
            'course': request.GET.get('course', 'all'),
            'year': request.GET.get('year', 'all'),
            'semester': request.GET.get('semester', 'all'),
            'college_id': request.GET.get('college_id', '')
        }
        
    
    
        students = Student.objects.all()
       
        
        # Apply filters
        if filters['course'] != 'all':
            students = students.filter(course=filters['course'])
        if filters['year'] != 'all':
            students = students.filter(year=filters['year'])
        if filters['semester'] != 'all':
            students = students.filter(semester=filters['semester'])
        if filters['college_id']:
            students = students.filter(college_id__icontains=filters['college_id'])
            
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(students, 5)  # Show 10 students per page
        
        try:
            students_page = paginator.page(page)
        except PageNotAnInteger:
            students_page = paginator.page(1)
        except EmptyPage:
            students_page = paginator.page(paginator.num_pages)
            
        html = render_to_string('student/student_result_partial.html', {'students': students_page})
        
        
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
import json

def get_student_details(request):    
    try:
        college_id = request.GET.get('college_id')
        student = Student.objects.get(college_id=college_id)
        
        student_data = {
            'college_id': student.college_id,
            'name': student.name,
            'last_name': student.last_name,
            'father_name': student.father_name,
            'mother_name': student.mother_name,
            'email': student.email,
            'phone': student.phone,
            'course': student.course,
            'level': student.level,
            'year': student.year,
            'semester': student.semester,
            'birthday': student.birthday.strftime('%Y-%m-%d') if student.birthday else '',
            'address': student.address,
            'city': student.city,
            'state': student.state,
            'state_code': student.state_code if hasattr(student, 'state_code') else '',
            'date_of_joining': student.date_of_joining.strftime('%Y-%m-%d') if student.date_of_joining else '',
            'profile_picture': student.profile_picture.url if student.profile_picture else ''
        }
        
        return JsonResponse({'success': True, 'student': student_data})
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})

def update_student(request): 
    try:
        college_id = request.POST.get('college_id')
        student = Student.objects.get(college_id=college_id)
        
        # Update fields
        student.name = request.POST.get('name')
        student.last_name = request.POST.get('last_name')
        student.father_name = request.POST.get('father_name')
        student.mother_name = request.POST.get('mother_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.course = request.POST.get('course')
        student.year = int(request.POST.get('year'))
        student.semester = int(request.POST.get('semester'))
        student.address = request.POST.get('address')
        
        student.save()
        
        return JsonResponse({'success': True, 'message': 'Student updated successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})

def bulk_update_students(request): 
    try:
        student_ids = request.POST.get('student_ids', '').split(',')
        students = Student.objects.filter(college_id__in=student_ids)
        
        updated_count = 0
        for student in students:
            # Only update fields that have values
            if request.POST.get('course'):
                student.course = request.POST.get('course')
            if request.POST.get('year'):
                student.year = int(request.POST.get('year'))
            if request.POST.get('semester'):
                student.semester = int(request.POST.get('semester'))
            
            student.save()
            updated_count += 1
        
        return JsonResponse({'success': True, 'message': f'{updated_count} students updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})

def delete_student(request):
    try:
        college_id = request.POST.get('college_id')
        student = Student.objects.get(college_id=college_id)
        student.delete()
        
        return JsonResponse({'success': True, 'message': 'Student deleted successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})

def bulk_delete_students(request):
    try:
        student_ids = request.POST.get('student_ids', '').split(',')
        students = Student.objects.filter(college_id__in=student_ids)
        deleted_count = students.count()
        students.delete()
        
        return JsonResponse({'success': True, 'message': f'{deleted_count} students deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})

def export_students(request):
    try:
        student_ids = request.POST.get('student_ids', '').split(',')
        students = Student.objects.filter(college_id__in=student_ids)
        
        # Create CSV response
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['College ID', 'Name', 'Email', 'Phone', 'Course', 'Year', 'Semester', 'Father Name', 'Address'])
        
        for student in students:
            writer.writerow([
                student.college_id,
                f"{student.name} {student.last_name}",
                student.email,
                student.phone,
                student.course,
                student.year,
                student.semester,
                student.father_name,
                student.address
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Error exporting students: {str(e)}")
        return redirect('studentBulkManagement')




# for attendance management student-faculty
from django.utils import timezone
@csrf_exempt
def save_attendance(request):
    if not request.session.get('faculty_college_id'):
        return JsonResponse({'error': 'Please login as faculty first'}, status=403)
        
    if request.method == 'POST':
        try:
            lecture = request.POST.get('lecture')
            date = request.POST.get('date')
            attendance_data = json.loads(request.POST.get('attendance'))
            course_name = request.POST.get('course')
            
            if not lecture or not date or not attendance_data or not course_name:
                return JsonResponse({'error': 'Missing required data'}, status=400)
                
            faculty = Faculty.objects.get(college_id=request.session['faculty_college_id'])
            course = Course.objects.get(code=course_name)
            
            saved_count = 0
            duplicate_entries = []
            new_entries = []
            
            for record in attendance_data:
                student = Student.objects.get(id=record['student_id'])
                
                # Check if attendance already exists
                existing_attendance = Attendance.objects.filter(
                    student=student,
                    course=course,
                    lecture_number=lecture,
                    date=date
                ).first()
                
                if existing_attendance:
                    # Record duplicate entry
                    duplicate_entries.append({
                        'student_id': student.id,
                        'student_name': student.name,
                        'existing_status': existing_attendance.status,
                        'new_status': record['status'].capitalize()
                    })
                    continue
                
                # Create new attendance record
                Attendance.objects.create(
                    student=student,
                    course=course,
                    lecture_number=lecture,
                    date=date,
                    faculty=faculty,
                    department=student.course.department if hasattr(student.course, 'department') else '',
                    status=record['status'].capitalize(),
                    timing=timezone.now()
                )
                
                new_entries.append({
                    'student_id': student.id,
                    'student_name': student.name,
                    'status': record['status'].capitalize()
                })
                saved_count += 1
                
            response_data = {
                'success': True,
                'message': f'Attendance saved successfully for {saved_count} students',
                'saved_count': saved_count,
                'new_entries': new_entries,
                'duplicate_entries': duplicate_entries
            }
            
            if duplicate_entries:
                response_data['warning'] = f'Found {len(duplicate_entries)} duplicate attendance records that were not saved'
                
            return JsonResponse(response_data)
            
        except Student.DoesNotExist:
            return JsonResponse({'error': 'One or more students not found'}, status=404)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

from datetime import datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect
from newapp.models import Student, Attendance  # Yahan 'newapp' use karo (apne app ka naam)

def student_attendance_view(request):
    role = request.session.get('role')
    if not request.session.get('student_college_id'):
        messages.error(request, "Please login as student first")
        return redirect('login')
        
    try:
        student = Student.objects.get(college_id=request.session['student_college_id'])
        # Get distinct years from attendance records
        years = Attendance.objects.filter(student=student).dates('date', 'year').distinct()
        years = [year.year for year in years]
        
        current_year = datetime.now().year
        
        return render(request, 'student/student_attendance_view.html', {
            'student': student,
            'years': years,
            'current_year': current_year,
            'role': role
        })
        
    except Student.DoesNotExist:
        messages.error(request, "Student not found")
        return redirect('dashboard2')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('dashboard2')

def get_student_attendance(request):
    try:
        student_id = request.GET.get('student_id')
        month = request.GET.get('month', 'all')
        year = request.GET.get('year', 'all')
        status = request.GET.get('status', 'all')
        course = request.GET.get('course', 'all')
        
        student = Student.objects.get(id=student_id)
        attendance = Attendance.objects.filter(student=student)
        
        if course != 'all':
            attendance = attendance.filter(course__name=course)
        if month != 'all':
            attendance = attendance.filter(date__month=month)
        if year != 'all':
            attendance = attendance.filter(date__year=year)
        if status != 'all':
            attendance = attendance.filter(status=status)
            
        attendance = attendance.order_by('-date', 'lecture_number')

        # pagination
        paginator = Paginator(attendance, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # Calculate summary
        total_lectures = attendance.count()
        present = attendance.filter(status='Present').count()
        absent = attendance.filter(status='Absent').count()
        
        attendance_percentage = 0
        if total_lectures > 0:
            attendance_percentage = round((present / total_lectures) * 100, 2)
            
        # Get distinct years again for the template
        years = Attendance.objects.filter(student=student).dates('date', 'year').distinct()
        years = [year.year for year in years]
        
        return render(request, 'student/student_attendance_view.html', {
            'page_obj': page_obj,
            'summary': {
                'total_lectures': total_lectures,
                'present': present,
                'absent': absent,
                'attendance_percentage': attendance_percentage
            },
            'student': student,
            'years': years,
            'current_year': datetime.now().year,
            'role': request.session.get('role')
        })
        
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('student_attendance_view')

# FOR FEES MANAGEMENT OF STUDENT

#  for student, for viewing fees
# for student, for viewing fees
def student_fees_view(request, college_id, number):
    role = request.session.get('role')
    if number == 'P1':
        college_id = college_id
        template = 'student/student_fee_detail.html'
        value = 'tem1'
    else:
        college_id = college_id
        template = 'student/student_fees_view.html'
        value = 'tem2'
    
    try:
        student = Student.objects.get(college_id=college_id)
        course = student.course # student course name
        year = student.course.no_of_years # student course time period
        batch = student.date_of_joining.year # fetch the student starting year only 
        totalFee = float(int(course.fees_per_year)*year)
        fee = 0 # total fee in starting is zero
        paid = 0 # total fee payment in starting is zero
        pending = 0 # (if any pending payment), in starting pending payment is zero
        advance = 0 #(if student paid extra payment)
        percent = 0 # payment percentage
        

        data = [] # for showing year seperately
        s = 0 # starting point
        e = 2 # ending point
        for i in range(1, year+1):   
            for j in range(s+i, e+i):
                feeStructure = FeeStructure.objects.filter(course = course, batch = str(batch), year = str(i), semester = str(j))
                dic1 = {'year':i, 'semester':j, }
                if feeStructure.exists():
                    payment = FeePayment.objects.filter(student = student, fee_structure = feeStructure.first())
                    dueDate = feeStructure.first().due_date # due date for fee payment
                    if payment.exists():
                        # render payment history
                        paymentDetails = FeePayment.objects.filter(student = student).order_by('payment_date')
                        if value == 'tem1':
                            dic1['singlePayment'] = payment
                        # calculate amount1 and amount2
                        amount1 = float(feeStructure.first().amount) # structure amount access
                        amount2 = float(payment.first().amount_paid) # payment amount access
                        extra = float(payment.first().extra)
                        # calculate the total paid amount
                        fee += amount1
                        paid += amount2
                        percent = (amount2/amount1)*100
                        amount2 = amount2 + extra
                        if amount1 == amount2 :
                            dic1['status'] = 'Paid'
                            dic1['feeAmt'] = amount1
                            if value == 'tem1':
                                dic1['paid'] = amount2
                        elif amount1 != amount2:
                            if amount1 > amount2 :
                                due = amount1 - amount2
                                pending += due
                                dic1['status'] = 'Pending'
                                dic1['due'] = due
                                dic1['dueDate'] = dueDate
                                dic1['feeAmt'] = amount1
                                if value == 'tem1':
                                    dic1['paid'] = amount2
                            elif amount2 > amount1 :
                                overdue = amount2 - amount1
                                advance += overdue
                                dic1['status'] = 'Overdue'
                                dic1['overdue'] = overdue
                                dic1['dueDate'] = dueDate
                                dic1['feeAmt'] = amount1
                                if value == 'tem1':
                                    dic1['paid'] = amount2
                    else:
                        dic1['status'] = 'Pending'           
                        dic1['dueDate'] = dueDate
                        dic1['feeAmt'] = amount1
                else:
                    dic1['status'] = "No-fee"
                data.append(dic1)
            s+=1
            e+=1 
            
        return render(request, template, {'student':student, 'totalFee':totalFee, 'data':data, 'role':role, 'fee':fee, 'paid':paid, 'pending':pending, 'advance':advance, 'percent':percent, 'paymentDetails':paymentDetails})
                 
    except Student.DoesNotExist:
        messages.error(request, "Student not found")
        # YEH LINE ADD KARO
        return render(request, 'error.html', {'message': 'Student not found'})
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        # YEH LINE ADD KARO  
        return render(request, 'error.html', {'message': f'An error occurred: {str(e)}'})

# for admin - for payment of fees
def feePayment(request):
       
            students = Student.objects.all()
            data = []
            
            for student in students:
                batch = student.date_of_joining.year
                course = Course.objects.get(course_id=student.course.course_id)
                s = 0
                e = 2
                Amt1 = 0
                Amt2 = 0
                due = 0
                overdue = 0
                totalFee = int(course.fees_per_year * course.no_of_years)
                year = course.no_of_years
                for i in range(1, year+1):   
                    for j in range(s + i, e + i):
                        feeStructure = FeeStructure.objects.filter(
                            year=str(i), 
                            semester=str(j), 
                            batch=batch, 
                            course=course
                        )
                        
                        if feeStructure.exists():
                            fee_structure = feeStructure.first()
                            Amt1 += fee_structure.amount
                            
                            feePayment = FeePayment.objects.filter(
                                student=student, 
                                fee_structure=fee_structure
                            )
                            
                            if feePayment.exists():
                                Amt2 += feePayment.first().amount_paid                                  
                    s += 1
                    e += 1
               
                # Determine status
                if (Amt1>0) and (Amt2>0):
                    percent = (Amt2/Amt1)*100
                    if Amt1 == Amt2:
                       data.append({'status':'Paid', 'student': student, 'total':totalFee, 'paid':Amt2, 'percent':percent})
                    elif Amt1 > Amt2:
                        data.append({'status':'Due', 'student':student, 'total':totalFee, 'paid':Amt2, 'due':Amt1-Amt2, 'percent':percent})
                    elif Amt2 > Amt1:
                        data.append({'status':'Overdue', 'student':student, 'total':totalFee, 'paid':Amt2, 'overdue':Amt2-Amt1, 'percent':percent})
                elif (Amt1>0) and (Amt2 == 0):
                    data.append({'status':'Pending', 'student':student, 'total':totalFee})
                else:
                    data.append({'status':'New', 'student':student, 'total':totalFee})

            return render(request, 'admin/admin_fee_management.html',{'data':data})

from datetime import datetime
def payNow(request, college_id):
    if request.method == 'POST':
        try:
            info = json.loads(request.body)
            college_id = info.get('college_id')
            S_year = info.get('year')
            S_sem = info.get('semester')
            student = Student.objects.get(college_id = college_id)
            year = student.course.no_of_years
            s = 0
            e = 2 
            data = []
            for i in range(1, year + 1 ):   
                for j in range(s + i, e + i):
                    feeStructure = FeeStructure.objects.filter(year = str(i), semester = str(j), student = student)
                    if feeStructure.exists():
                        feePayment = FeePayment.objects.filter(fee_structure = feeStructure.first(), student = student.college_id)
                        if not feePayment.exists() and (i, j) == (S_year, S_sem):
                            feeShow = float(feeStructure.first().amount)
                            status = 'New'
                            # Generate receipt no
                            current_year = str(datetime.now().year)
                            max_receipt_no = FeePayment.objects.aggregate(max_id=models.Max('receipt_number'))['max_receipt_no']
                            
                            if max_receipt_no is None:
                                receipt_no = 'GK' + current_year + 'RC1'  # Initial ID
                            else:
                                try:
                                # Extract numeric part and increment
                                    numeric_part = int(max_receipt_no[8:])  # Remove 'ST' prefix
                                    receipt_no = f'GK{current_year}RC{numeric_part + 1}'
                                except (ValueError, IndexError):
                                    receipt_no = 'GK' + current_year + 'RC1'  # Fallback if format is wrong

                            # generate transaction id
                            max_TR_id = FeePayment.objects.aggregate(max_id=models.Max('transaction_id'))['max_TR_id']
                            
                            if max_TR_id is None:
                                TR_id = 'GK' + current_year + 'TR1'  # Initial ID
                            else:
                                try:
                                # Extract numeric part and increment
                                    numeric_part = int(max_receipt_no[8:])  # Remove 'ST' prefix
                                    TR_id = f'GK{current_year}TR{numeric_part + 1}'
                                except (ValueError, IndexError):
                                    TR_id = 'GK' + current_year + 'TR1'  # Fallback if format is wrong

                            data.append({'feeShow':feeShow, 'TR_id': TR_id, 'receipt_no':receipt_no, 'status':status})                                           
                s += 1
                e += 1
            return JsonResponse({'data':data})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Method'}, status=400)

    
# def payNow(request, college_id):
#     if request.method == 'POST':
#         try:
#             student = Student.objects.get(college_id = college_id)
#             year = student.course.no_of_years
#             s = 0
#             e = 2 
#             for i in range(1, year + 1 ):   
#                 for j in range(s + i, e + i):
#                     feeStructure = FeeStructure.objects.filter(year = str(i), semester = str(j), student = student)
#                     if feeStructure.exists():
#                         feePayment = FeePayment.objects.filter(fee_structure = feeStructure.first(), student = student.college_id)
#                         if feePayment.exists():
#                             amount1 = feeStructure.first().amount # actually payment call
#                             amount2 = feePayment.first().amount_paid # payment paid by student
#                             extra = feePayment.first().extra # extra payment
#                             amount2  = amount2 + extra
#                             if amount1 == amount2:
#                                 print("paid")
#                             else:
#                                 if amount1 > amount2 :
#                                     print("due")
#                                 elif amount2 > amount1:
#                                     print("overdue")
#                         else:
#                             print("pending")
#                     else:
#                         print("nofee")                      
#                 s += 1
#                 e += 1
#         except Exception as e:
#             return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid Method'}, status=400)

    

        
 
         
        
      







# for fee structure creation
# [[[[[[[[[[[[[Send Batch Details]]]]]]]]]]]]]
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast, Substr
def sendBatch(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course = data.get('course')
        course_detail = Course.objects.get(name = course)
        year = data.get('year')
        semester = data.get('semester')
        try:
            max_id = Student.objects.annotate(id_as_int = Cast(Substr('college_id',3),IntegerField()))
            max_id = max_id.filter(year = int(year), semester = int(semester), course = course_detail)
            if max_id.exists():
               max_id = max_id.aggregate(Max('id_as_int'))['id_as_int__max']
               max_id = 'ST' + str(max_id)
               student = Student.objects.get(college_id = str(max_id))
                # get course fees:
               fees = float((Course.objects.get(name = course).fees_per_year)/2)
               return JsonResponse({'batch':student.date_of_joining.year,'fees':fees})
            else:
                return JsonResponse({'error':'Student Does not exist with this Infomation!'},status=400)        
        except Exception as e:
            return JsonResponse({'error': f'An error Occured: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Method'}, status=400)

def createFeeStructure(request):
    if request.method == 'POST':
        try:
            # Check content type to handle both FormData and JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                # Handle form data
                data = {
                    'course': request.POST.get('course'),
                    'dueDate': request.POST.get('dueDate'),
                    'year': request.POST.get('year'),
                    'semester': request.POST.get('semester'),
                    'feeAmt': request.POST.get('feeAmt'),
                    'batch': request.POST.get('batch')
                }
            
            # Validate required fields
            required_fields = ['course', 'dueDate', 'year', 'semester', 'feeAmt', 'batch']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required'}, status=400)

            # Auto-generate structure ID
            max_id = FeeStructure.objects.aggregate(max_id=models.Max('structure_id'))['max_id']          
            if max_id is None:
                structure_id = 'FS20251'  # Initial ID
            else:
                try:
                    # Extract numeric part and increment
                    numeric_part = int(max_id[2:])  # Remove 'FS' prefix
                    structure_id = f'FS{numeric_part + 1}'
                except (ValueError, IndexError):
                    structure_id = 'FS20251'

            # Create FeeStructure object (NOT Course)
            checking = FeeStructure.objects.filter(
                course=data.get('course'),
                year=data.get('year'),
                semester=data.get('semester'),
                amount=float(data.get('feeAmt')),
                batch=data.get('batch'))

            if checking.exists():
                return JsonResponse({'error': 'Fee Structure created Already!'})
            else:
                FeeStructure.objects.create(
                structure_id=structure_id,
                course=data.get('course'),
                due_date=data.get('dueDate'),
                year=data.get('year'),
                semester=data.get('semester'),
                amount=float(data.get('feeAmt')),
                batch=data.get('batch')  # Changed from for_year to batch
            )
                return JsonResponse({'success': 'Fee Structure Created Successfully'})
            
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Method'}, status=400)

def fetchBatch(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            course = data.get('course')
            year = data.get('year')
            semester = data.get('semester')
            batch = data.get('batch')
            try:
                if not batch or batch == ''  :
                    all_detail = FeeStructure.objects.filter(course = course, year = year, semester = semester)
                    if all_detail.exists():
                        batch = all_detail.order_by('batch').values_list('batch',flat=True)
                        return JsonResponse({'batch':list(batch)})
                    else:
                        return JsonResponse({'error':'No Fee Structure Fouded with this Information!'},status = 400)
                elif batch != '':
                    all_detail = FeeStructure.objects.filter(course = course, year = year, semester = semester, batch = batch).order_by('structure_id')
                    if all_detail.exists():
                        info = []
                        for i in all_detail:
                            info.append({'structure_id':i.structure_id, 'course':i.course, 'year':i.year, 'semester':i.semester, 'due_date':i.due_date.strftime("%Y-%m-%d"), 'batch':i.batch, 'amount':i.amount})
                        return JsonResponse({'info':info})
                    else:
                        return JsonResponse({'error':'No Fee Structure Fouded with this Information!'},status = 400)
                             
            except Exception as e:
                return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Method'}, status=400)

def deleteStructure(request,structure_id):
    try:
        value_copy = structure_id
        structure = FeeStructure.objects.get(structure_id = structure_id)
        structure.delete()
        return JsonResponse({'success':f"Fee Structure Deleted Successfully with ID: {value_copy}"})
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

            

# chatting management :
from .models import Student, Faculty, ChatRoom, Message
# Update your chat_home view in views.py
def chat_home(request):
    role = request.session.get('role')
    user_id = None
    
    if role == 'student':
        user_id = request.session.get('student_college_id')
        student = Student.objects.get(college_id=user_id)
        faculty_id = request.GET.get('faculty_id')
        
        if not faculty_id:
            return redirect('faculty_filtering')  # Redirect if no faculty selected
            
        try:
            faculty = Faculty.objects.get(college_id=faculty_id)
            # Check if student follows this faculty
            if faculty not in student.followed_faculty.all():
                messages.error(request, "You must follow this faculty first")
                return redirect('faculty_filtering')
                
            return render(request, 'chat/chat1.html', {
                'current_user': student,
                'other_user': faculty,
                'role': role
            })
        except Faculty.DoesNotExist:
            messages.error(request, "Faculty not found")
            return redirect('faculty_filtering')
            
    elif role == 'faculty':
        user_id = request.session.get('faculty_college_id')
        faculty = Faculty.objects.get(college_id=user_id)
        student_id = request.GET.get('student_id')
        
        if not student_id:
            # Show faculty's student list for selection
            students = Student.objects.filter(followed_faculty=faculty)
            return render(request, 'chat/page2.html', {
                'faculty': faculty,
                'students': students,
                'role': role
            })
            
        try:
            student = Student.objects.get(college_id=student_id)
            # Check if student follows this faculty
            if faculty not in student.followed_faculty.all():
                messages.error(request, "This student doesn't follow you")
                return redirect('faculty_student_list')
                
            return render(request, 'chat/chat2.html', {
                'current_user': faculty,
                'other_user': student,
                'role': role
            })
        except Student.DoesNotExist:
            messages.error(request, "Student not found")
            return redirect('faculty_student_list')
            
    elif role == 'admin':
        # Admin chat logic remains same
        pass
    else:
        return redirect('login')

 # for get all faculty details 
@csrf_exempt
def get_faculty_details(request):
    role = request.session.get('role')

    if role == 'student':
        try:
            department = Course.objects.all()
            all_faculty = Faculty.objects.all()
            
            # Check which faculty are followed by the student
            student_id = request.session.get('student_college_id')
            followed_faculty = []
            if student_id:
                student = Student.objects.get(college_id=student_id)
                followed_faculty = student.followed_faculty.all().values_list('college_id', flat=True)
            
            return render(request, ['chat/page.html','faculty/faculty_page.html'], {
                'faculty': all_faculty,
                'department': department,
                'followed_faculty': followed_faculty
            })
        except Faculty.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Faculty not found'})

# for faculty filtering
def faculty_filtering(request):
    if not request.session.get('student_college_id'):
        messages.error(request, "Please login as student first")
        return redirect('login')
        
    filters = {
        'department': request.GET.get('department', 'all'),
        'name': request.GET.get('name', '')
    }

    faculty = Faculty.objects.all()
    
    if filters['department'] != 'all':
        faculty = faculty.filter(department=filters['department'])
    if filters['name']:
        faculty = faculty.filter(name__icontains=filters['name'])

    # Check which faculty are followed by the student
    student_id = request.session.get('student_college_id')
    followed_faculty = []
    if student_id:
        student = Student.objects.get(college_id=student_id)
        followed_faculty = student.followed_faculty.all().values_list('college_id', flat=True)

    html = render_to_string('chat/faculty_list_partial.html', {
        'faculty_detail': faculty,
        'followed_faculty': followed_faculty
    })
    return JsonResponse({'html': html})

# for handling following functions
from django.urls import reverse 
@csrf_exempt
def toggle_follow(request):
    if request.method == 'POST':
        try:
            faculty_id = request.POST.get('faculty_id')
            student_id = request.session.get('student_college_id')
            
            if not student_id:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Student not logged in',
                    'redirect': reverse('login')
                })
            
            faculty = Faculty.objects.get(college_id=faculty_id)
            student = Student.objects.get(college_id=student_id)
            
            if faculty in student.followed_faculty.all():
                student.followed_faculty.remove(faculty)
                is_following = False
                message = 'Successfully unfollowed faculty'
            else:
                student.followed_faculty.add(faculty)
                is_following = True
                message = 'Successfully followed faculty'
                
            return JsonResponse({
                'status': 'success',
                'is_following': is_following,
                'faculty_id': faculty_id,
                'message': message
            })
            
        except Faculty.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'Faculty not found'
            }, status=404)
        except Student.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'Student not found',
                'redirect': reverse('login')
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request method'
    }, status=400)

# for sending all info about all students for faculty portal ----not working filtering
def faculty_student_list(request):
    if not request.session.get('faculty_college_id'):
        messages.error(request, "Please login as faculty first")
        return redirect('login')
    
    try:
   
        faculty = Faculty.objects.get(college_id=request.session['faculty_college_id'])
        students = Student.objects.filter(followed_faculty=faculty)
     
        
        return render(request, 'chat/page2.html', {
            'faculty': faculty,
            'students': students,
       
            'role': 'faculty'
        })
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty not found")
        return redirect('login')
# for sending courses details
def send_course_details(request):
    course_name = request.GET.get('course')
    try:
        course = Course.objects.get(name=course_name)
        return JsonResponse({
            'no_of_years': course.no_of_years,
            'no_of_semesters': course.no_of_semesters
        })
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

# for student filtering
def student_filter_details(request):
    if not request.session.get('faculty_college_id'):
        return JsonResponse({'status': 'error', 'message': 'Please login as faculty first'})
        
    try:
        faculty = Faculty.objects.get(college_id=request.session['faculty_college_id'])
        students = Student.objects.filter(followed_faculty=faculty)
        
        filters = {
            'course': request.GET.get('course', 'all'),
            'year': request.GET.get('year', 'all'),
            'semester': request.GET.get('semester', 'all'),
            'college_id': request.GET.get('college_id', '')
        }

        if filters['course'] != 'all':
            students = students.filter(course=filters['course'])
        if filters['year'] != 'all':
            students = students.filter(year=filters['year'])
        if filters['semester'] != 'all':
            students = students.filter(semester=filters['semester'])
        if filters['college_id']:
            students = students.filter(college_id__icontains=filters['college_id'])

        html = render_to_string('chat/student_list_partial.html', {
            'students': students
        })
        return JsonResponse({'html': html})
        
    except Faculty.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Faculty not found'})
    

# for create chat room
from .models import ChatRoom, Message, Student, Faculty
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)
@csrf_exempt
def create_chat_room(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            participant1 = data.get('participant1')
            participant2 = data.get('participant2')
            
            # Check if room already exists
            room = ChatRoom.objects.filter(
                Q(participant1=participant1, participant2=participant2) |
                Q(participant1=participant2, participant2=participant1)
            ).first()

            if not room:
                room = ChatRoom.objects.create(
                    name=f"Chat between {participant1} and {participant2}",
                    participant1=participant1,
                    participant2=participant2
                )

            return JsonResponse({
                'status': 'success',
                'room_id': str(room.id),
                'message': 'Chat room ready'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
# for gwt messages
@csrf_exempt
def get_messages(request, room_id):
    try:
        current_user = request.GET.get('current_user')
        if not current_user:
            return JsonResponse({'status': 'error', 'message': 'current_user parameter missing'}, status=400)

        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Chat room not found'}, status=404)

        # Verify user is participant
        if current_user not in [chat_room.participant1, chat_room.participant2]:
            return JsonResponse({'status': 'error', 'message': 'Not a participant'}, status=403)

        # Get last message ID if provided
        last_message_id = request.GET.get('last_message_id')
        
        # Get messages after last_message_id if provided, otherwise get all
        if last_message_id:
            messages = Message.objects.filter(
                chat_room=chat_room,
                id__gt=last_message_id
            ).order_by('timestamp')
        else:
            messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')

        # Mark messages as delivered
        Message.objects.filter(
            chat_room=chat_room,
            is_delivered=False,
        ).exclude(sender_id=current_user).update(is_delivered=True)

        # Get typing status from cache
        other_user = chat_room.participant2 if chat_room.participant1 == current_user else chat_room.participant1
        is_typing = cache.get(f'typing_{room_id}_{other_user}', False)

        # Get other user's online status
        other_user_status = get_user_status(other_user)

        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'sender': msg.sender_id,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'is_delivered': msg.is_delivered,
                'is_read': msg.is_read
            })

        return JsonResponse({
            'status': 'success',
            'messages': messages_data,
            'is_typing': is_typing,
            'other_user_status': other_user_status
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
# for get user status 
def get_user_status(user_identifier):
    try:
        if user_identifier.startswith('faculty_'):
            faculty_id = user_identifier.replace('faculty_', '')
            faculty = Faculty.objects.get(college_id=faculty_id)
            return {
                'online': faculty.online_status,
                'last_seen': faculty.last_seen.strftime('%Y-%m-%d %H:%M') if faculty.last_seen else None
            }
        elif user_identifier.startswith('student_'):
            student_id = user_identifier.replace('student_', '')
            student = Student.objects.get(college_id=student_id)
            return {
                'online': student.online_status,
                'last_seen': student.last_seen.strftime('%Y-%m-%d %H:%M') if student.last_seen else None
            }
    except Exception as e:
        logger.error(f"Error getting user status for {user_identifier}: {str(e)}")
        return None
# for sending message
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            sender_id = data.get('sender_id')
            content = data.get('content', '').strip()
            
            if not all([room_id, sender_id, content]):
                return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

            try:
                chat_room = ChatRoom.objects.get(id=room_id)
            except ChatRoom.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)

            if sender_id not in [chat_room.participant1, chat_room.participant2]:
                return JsonResponse({'status': 'error', 'message': 'Not a participant'}, status=403)

            message = Message.objects.create(
                chat_room=chat_room,
                sender_id=sender_id,
                content=content,
                is_delivered=True
            )

            # Update last activity for the chat room
            chat_room.last_activity = timezone.now()
            chat_room.save()

            return JsonResponse({
                'status': 'success',
                'message_id': str(message.id),
                'timestamp': message.timestamp.isoformat()
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

# for updating typing status---------not working
@csrf_exempt
def update_typing_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            user_id = data.get('user_id')
            is_typing = data.get('is_typing', False)
            
            # Store typing status in cache (expires after 5 seconds)
            cache.set(f'typing_{room_id}_{user_id}', is_typing, timeout=5)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

# for update the read remark-------not working
@csrf_exempt
def mark_messages_as_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            reader_id = data.get('reader_id')
            
            if not all([room_id, reader_id]):
                return JsonResponse(
                    {'status': 'error', 'message': 'Missing required fields'},
                    status=400
                )

            # Mark messages as read where reader is not the sender
            updated_count = Message.objects.filter(
                chat_room_id=room_id,
                is_read=False
            ).exclude(sender_id=reader_id).update(
                is_read=True,
                read_at=timezone.now()
            )
            
            return JsonResponse({
                'status': 'success',
                'updated_count': updated_count
            })
        except Exception as e:
            logger.exception("Error marking messages as read")
            return JsonResponse(
                {'status': 'error', 'message': str(e)}, 
                status=400
            )
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request'}, 
        status=400
    )

# for delete chat 
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import logging

@csrf_exempt
def delete_chat(request, room_id):
    if request.method == 'DELETE':
        try:
            # Get user identifier from request body
            data = json.loads(request.body)
            current_user_identifier = data.get('user_identifier')
            
            if not current_user_identifier:
                return JsonResponse({
                    'status': 'error',
                    'message': 'User identifier not provided'
                }, status=400)

            chat_room = get_object_or_404(ChatRoom, id=room_id)
            
            # Verify user is a participant in this chat
            if current_user_identifier not in [chat_room.participant1, chat_room.participant2]:
                return JsonResponse({
                    'status': 'error',
                    'message': 'You are not authorized to delete this chat'
                }, status=403)
            
            # Delete all messages first
            Message.objects.filter(chat_room=chat_room).delete()
            
            # Then delete the chat room
            chat_room.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Chat deleted successfully'
            })
            
        except Exception as e:
            logger.error(f"Error deleting chat: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to delete chat. Please try again.'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Department, Faculty, Student, Course
from .form import DepartmentForm

def department_creation(request):
    # Always get departments list for the template
    role = request.session.get('role')
    details = Department.objects.all().order_by("department_id")
    paginator = Paginator(details, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_department = Department.objects.count()
    total_faculty = Faculty.objects.count()
    enrolled_students = Student.objects.count()
    total_course = Course.objects.count()
    programs = Course.objects.all().order_by('code')
    # Handle AJAX requests first
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for department in page_obj:
            data.append({
                "department_id": department.department_id,
                "name": department.name,
                "code": department.code,
                "type": department.type,
                "faculty_count": department.faculty_count,
                "programs_count": department.programs_count,
                "student_capacity": department.student_capacity
                
            })
        return JsonResponse({
            "details": data,
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "page_number": page_obj.number,
            "total_pages": paginator.num_pages
        })
    
    if request.method == 'POST':
        action = request.POST.get('form_name')
        
        if action == 'departmentCreation':
            try:
                max_id = Department.objects.aggregate(max_id=models.Max('department_id'))['max_id']
                
                if max_id is None:
                    department_id = 'DEP-0'  # Initial ID
                else:
                    try:
                        # Extract numeric part and increment
                        numeric_part = int(max_id[4:])  # Remove 'ST' prefix
                        department_id = f'DEP-{numeric_part + 1}'
                    except (ValueError, IndexError):
                        department_id = 'DEP-0'  # Fallback if format is wrong

                code = request.POST.get('code')
                if Department.objects.filter(code=code).exists():
                    messages.error(request, f"Department with code '{code}' already exists!")
                else:
                    Department.objects.create(
                        department_id = department_id,
                        name=request.POST.get('name'),
                        code=code,
                        type=request.POST.get('type'),
                        description=request.POST.get('description'),
                        programs_count=request.POST.get('programe'),
                        faculty_count=request.POST.get('facultyCount'),
                        student_capacity=request.POST.get('studentCapacity'),
                    )
                    messages.success(request, "Department Created Successfully!")
                    # Redirect to prevent form resubmission on refresh
                    return redirect('department_creation')
            except Exception as e:
                messages.error(request, f"Error adding department: {str(e)}")
    
    # Always return the render with details
    return render(request, 'department.html', {
        "page_obj": page_obj,
        'total_department': total_department,
        'total_faculty': total_faculty,
        'enrolled_students': enrolled_students,
        'total_course': total_course,
        'programs': programs,
        'role':role
    })

from django.shortcuts import get_object_or_404
class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department.html"
    success_url = reverse_lazy("department_creation")
    
    # Override get_object to use department_id instead of pk
    def get_object(self, queryset=None):
        department_id = self.kwargs.get('pk')
        return get_object_or_404(Department, department_id=department_id)

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = "department.html"
    success_url = reverse_lazy("department_creation")
    
    # Override get_object to use department_id instead of pk
    def get_object(self, queryset=None):
        department_id = self.kwargs.get('pk')
        return get_object_or_404(Department, department_id=department_id)


# course craetion
from .models import Department, Course,Level
from django.db.models import Q

def course_creation(request):
    role = request.session.get('role')
    action = request.POST.get('form_name')
    query = request.POST.get('q')
    details = Course.objects.all().order_by('created_at')
    if query : 
        details = details.filter(
        Q(name__icontains=query)|
        Q(code__icontains=query)|
        Q(department__name=query)|
        Q(level__name=query)
        )    
    paginator = Paginator(details,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for course in page_obj:
            data.append({
                "name": course.name,
                "department": course.department.name,
                "code": course.code,
                "no_of_years": course.no_of_years,
                "no_of_semesters": course.no_of_semesters,
                "student_capacity": course.student_capacity,
                "level":course.level.name, 
                
            })
        return JsonResponse({
            "details": data,
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "page_number": page_obj.number,
            "total_pages": paginator.num_pages
        })        
    try:
        # Get lists for both GET and POST requests
        department_list = Department.objects.filter(type='Faculty')
        level_list = Level.objects.all()
        
        if request.method == 'POST':
            action = request.POST.get('form_name')
            if action == 'courseCreation':
                try:
                    # Get and convert form data
                    duration = int(request.POST.get('courseDuration'))
                    capacity = int(request.POST.get('studentCapacity'))
                    fees = float(request.POST.get('courseFees'))
                    # Auto-generate employee ID
                    max_id = Course.objects.aggregate(max_id=models.Max('course_id'))['max_id']
                
                    if max_id is None:
                        course_id = 'GK-C-01'  # Initial ID
                    else:
                        try:
                            # Extract numeric part and increment
                            numeric_part = int(max_id[5:])  # Remove 'GK' prefix
                            course_id = f'GK-C-{numeric_part + 1}'
                        except (ValueError, IndexError):
                            course_id = 'GK-C-01'  
                    
                    # Create course with foreign key IDs
                    Course.objects.create(
                        course_id = course_id,
                        image = request.POST.get('cousreImage'),
                        name=request.POST.get('courseName'),
                        department_id=request.POST.get('courseDepartment'),  # Use _id field
                        no_of_years=duration,
                        no_of_semesters=duration * 2,
                        code=request.POST.get('courseCode'),
                        description=request.POST.get('courseDescription'),
                        student_capacity=capacity,
                        level_id=request.POST.get('courseLevel'),  # Use _id field
                        fees_per_year=fees,
                        no_of_lecture = request.POST.get('courseLecture')
                    )
                    messages.success(request, f"Course Created Successfully with {course_id}!")
                    return redirect("course_creation")
                except ValueError:
                    messages.error(request, "Invalid number format in form data")
                except Exception as e:
                    messages.error(request, f"Error adding course: {str(e)}")
            
    except Exception as e:
        messages.error(request, f"Error loading page: {str(e)}")
    return render(request, 'course_creation.html', {
            'department_list': department_list,
            'level_list': level_list,
            'details':details,
            'role':role,
            "page_obj": page_obj, 
            "course":details,
            "query":query
        })
    
# Created Positions
from .models import Position, Department

def position_creation(request):
    role = request.session.get('role')
    details = Position.objects.all().order_by('position_id')
    paginator = Paginator(details,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for position in page_obj:
            data.append({
                "position_id":position.position_id,
                "name": position.name,
                "department": position.department.name,
                "type": position.type,
                "salary": position.salary,
                "role": position.role,
                "level":position.level, 
                
            })
        return JsonResponse({
            "details": data,
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "page_number": page_obj.number,
            "total_pages": paginator.num_pages
        })     
    try:
        # Get lists for both GET and POST requests
        faculty_department_list = Department.objects.filter(type='Faculty')
        admin_department_list = Department.objects.filter(type='Admin')
        
        if request.method == 'POST':
            action = request.POST.get('form_name')
            if action == 'adminPositionForm':
                try:
                    # Get form data
                    position_name = request.POST.get('adminPosition')
                    department_id = request.POST.get('adminDepartment')
                    level = request.POST.get('adminLevel')
                    
                    # Check if position already exists
                    existing_position = Position.objects.filter(
                        name=position_name,
                        department_id=department_id,
                        level=level,
                        role='Admin'
                    ).first()
                    
                    if existing_position:
                        messages.error(request, f"Admin position '{position_name}' already exists in this department with the same level!")
                    else:
                        # Get and convert form data
                        salary_str = request.POST.get('adminSalary')
                        # Clean salary string - remove any non-numeric characters
                        salary_str = ''.join(filter(str.isdigit, salary_str))
                        salary = int(salary_str) if salary_str else 0
                        
                        role_filter = Position.objects.filter(role='Admin')
                        
                        # Check if any admin positions exist
                        if not role_filter.exists():
                            position_id = 'GKP-AD-1'  # Initial ID
                        else:
                            max_id = role_filter.aggregate(max_id=models.Max('position_id'))['max_id']
                            
                            if max_id is None:
                                position_id = 'GKP-AD-1'
                            else:
                                try:
                                    # Extract numeric part and increment
                                    numeric_part = int(max_id.split('-')[-1])  # Get the last part after splitting by '-'
                                    position_id = f'GKP-AD-{numeric_part + 1}'
                                except (ValueError, IndexError):
                                    position_id = 'GKP-AD-1'
                        
                        # Handle both possible field names for requirement
                        requirement = request.POST.get('adminRequirment') or request.POST.get('adminRequirement')
                        if not requirement:
                            messages.error(request, "Requirement field is required")
                            raise ValueError("Requirement field is required")
                        
                        # Create position with foreign key IDs
                        Position.objects.create(
                            position_id=position_id,
                            name=position_name,
                            type=request.POST.get('adminType'),
                            department_id=department_id,
                            level=level,
                            salary=salary,
                            role='Admin',
                            specialization=request.POST.get('adminSpecialization'),
                            requirment=requirement,
                            responsibility=request.POST.get('adminResponsibility'),
                        )
                        messages.success(request, "Admin Position Created Successfully!")
                        return redirect('position_creation')  # Redirect to prevent form resubmission
                    
                except ValueError as e:
                    if "Requirement field is required" in str(e):
                        # Already handled by error message above
                        pass
                    else:
                        messages.error(request, "Invalid number format in form data")
                except Exception as e:
                    messages.error(request, f"Error adding position: {str(e)}")

            elif action == 'facultyPositionForm':
                try:
                    # Get form data
                    position_name = request.POST.get('facultyPosition')
                    department_id = request.POST.get('facultyDepartment')
                    level = request.POST.get('facultyLevel')
                    
                    # Check if position already exists
                    existing_position = Position.objects.filter(
                        name=position_name,
                        department_id=department_id,
                        level=level,
                        role='Faculty'
                    ).first()
                    
                    if existing_position:
                        messages.error(request, f"Faculty position '{position_name}' already exists in this department with the same level!")
                    else:
                        # Get and convert form data
                        salary_str = request.POST.get('facultySalary')
                        # Clean salary string - remove any non-numeric characters
                        salary_str = ''.join(filter(str.isdigit, salary_str))
                        salary = int(salary_str) if salary_str else 0
                        
                        role_filter = Position.objects.filter(role='Faculty')
                        
                        # Check if any faculty positions exist
                        if not role_filter.exists():
                            position_id = 'GKP-FA-1'  # Initial ID
                        else:
                            max_id = role_filter.aggregate(max_id=models.Max('position_id'))['max_id']
                            
                            if max_id is None:
                                position_id = 'GKP-FA-1'
                            else:
                                try:
                                    # Extract numeric part and increment
                                    numeric_part = int(max_id.split('-')[-1])  # Get the last part after splitting by '-'
                                    position_id = f'GKP-FA-{numeric_part + 1}'
                                except (ValueError, IndexError):
                                    position_id = 'GKP-FA-1'
                        
                        # Handle both possible field names for requirement
                        requirement = request.POST.get('facultyRequirment') or request.POST.get('facultyRequirement')
                        if not requirement:
                            messages.error(request, "Requirement field is required")
                            raise ValueError("Requirement field is required")
                        
                        # Create position with foreign key IDs
                        Position.objects.create(
                            position_id=position_id,
                            name=position_name,
                            type=request.POST.get('facultyType'),
                            department_id=department_id,
                            level=level,
                            role='Faculty',
                            salary=salary,
                            specialization=request.POST.get('facultySpecialization'),
                            requirment=requirement,
                            responsibility=request.POST.get('facultyResponsibility'),
                        )
                        messages.success(request, "Faculty Position Created Successfully!")
                        return redirect('position_creation')  # Redirect to prevent form resubmission
                    
                except ValueError as e:
                    if "Requirement field is required" in str(e):
                        # Already handled by error message above
                        pass
                    else:
                        messages.error(request, "Invalid number format in form data")
                except Exception as e:
                    messages.error(request, f"Error adding position: {str(e)}")
        
        # Return with context for both GET and POST
        return render(request, 'position.html', {
            'faculty_department_list': faculty_department_list,
            'admin_department_list': admin_department_list,
            'details': details,
            'role':role,
            'page_obj':page_obj
        })
            
    except Exception as e:
        messages.error(request, f"Error loading page: {str(e)}")
        return render(request, 'position.html', {
            'faculty_department_list': [],
            'admin_department_list': [],
            'details': [],
            'role':[],
            'page_obj':[]
        })

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




from django.db.models import Max
from .models import History, Student, Faculty, Admin
from django.shortcuts import render, get_object_or_404
import json

def historySender(request, type):
    role = request.session.get('role')
    data = []
    
    if type == 'Admin':
        
        history = History.objects.filter(reciver_type__iexact='Admin').values("updatedTo")
        history = history.annotate(latest_time=Max("updatedAt")).values_list("updatedTo", "latest_time")
        for i in history:
            try:
                detail = Admin.objects.get(college_id=str(i[0]))
                name = str(detail.name + " " + detail.last_name)
                data.append({
                    "name": name, 
                    "college_id": detail.college_id, 
                    "department": detail.department.name, 
                    "position": detail.position.name, 
                    "last_update": i[1]
                })
            except Admin.DoesNotExist:
                continue
                
    elif type == 'Faculty':
        history = History.objects.filter(reciver_type__iexact='Faculty').values("updatedTo")
        history = history.annotate(latest_time=Max("updatedAt")).values_list("updatedTo", "latest_time")
        for i in history:
            try:
                detail = Faculty.objects.get(college_id=str(i[0]))
                name = str(detail.name + " " + detail.last_name)
                data.append({
                    "name": name, 
                    "college_id": detail.college_id, 
                    "department": detail.department.name, 
                    "position": detail.position.name, 
                    "last_update": i[1]
                })
            except Faculty.DoesNotExist:
                continue
                
    elif type == 'Student':
        history = History.objects.filter(reciver_type__iexact='Student').values("updatedTo")
        history = history.annotate(latest_time=Max("updatedAt")).values_list("updatedTo", "latest_time")
        for i in history:
            try:
                detail = Student.objects.get(college_id=str(i[0]))
                name = str(detail.name + " " + detail.last_name)
                data.append({
                    "name": name, 
                    "college_id": detail.college_id, 
                    "course": detail.course.name, 
                    "level": detail.course.code, 
                    "last_update": i[1]
                })
            except Student.DoesNotExist:
                continue
    
    return render(request, 'main/history.html', {
        'role': role, 
        'type': type, 
        'data': data
    })
   
def get_updatedToDetails(request,college_id):
    id_prefix = str(college_id[0:2])
    details = None
    if id_prefix == 'AD':
        try:
           details = Admin.objects.get(college_id = college_id)
           name = str(details.name + " " + details.last_name) 
           return JsonResponse({"name":name, "college_id":details.college_id, 
             "row4":details.position.name, "row3":details.department.name})
           
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin not found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif id_prefix == 'GK':
        try:
           details = Faculty.objects.get(college_id = college_id)
           name = str(details.name + " " + details.last_name)
           return JsonResponse({"name":name, "college_id":details.college_id, 
             "row4":details.position.name, "row3":details.department.name})
           
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif id_prefix == 'ST': 
        try:
            details = Student.objects.get(college_id = college_id)
            name = str(details.name + " " + details.last_name)
            course = details.course.name
            
            return JsonResponse({"name":name, "college_id":details.college_id, 
             "row3":course, "row4":details.course.code})
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

from django.db.models import F
def getHistory(request,college_id):
    id_prefix = str(college_id[0:2])
    details = None
    if id_prefix == 'ST':
        try:
            details = Student.objects.get(college_id = college_id)
            name = str(details.name + " " + details.last_name)
            course = str(details.course.name + " - " + details.course.level.name + f" - ({details.course.department.name})")
            year = details.date_of_joining.year
            end_year = int(year) + int(details.course.no_of_years)
            batch = str(str(year) + " - " + str(end_year))
            # getting history:
            history = list(History.objects.filter(updatedTo = college_id, reciver_type = 'Student').values('history_id','position','updatedFrom','updatedAt','updatedTo','content','type'))
            return JsonResponse({"name":name, "college_id":details.college_id, 
             "Row3":course, "Row4":batch, "history": history})
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    elif id_prefix == 'AD':
        try:
           details = Admin.objects.get(college_id = college_id)
           name = str(details.name + " " + details.last_name) 
           history = list(History.objects.filter(updatedTo = college_id, reciver_type = 'Admin').values('history_id','position','updatedFrom','updatedAt','updatedTo','content','type'))
           return JsonResponse({"name":name, "college_id":details.college_id, 
             "Row4":str(details.position.name) + " - " + str(details.position.position_id), "Row3":str(details.department.name) + " - " + str(details.department.department_id),
            'history':history})
           
        except Admin.DoesNotExist:
            return JsonResponse({"error": "Admin not found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif id_prefix == 'GK':
        try:
           details = Faculty.objects.get(college_id = college_id)
           name = str(details.name + " " + details.last_name)
           history = list(History.objects.filter(updatedTo = college_id, reciver_type = 'Faculty').values('history_id','position','updatedFrom','updatedAt','updatedTo','content','type'))
           return JsonResponse({"name":name, "college_id":details.college_id, 
             "Row4":str(details.position.name) + " - " + str(details.position.position_id), "Row3":str(details.department.name) + " - " + str(details.department.department_id),
            'history': history})
           
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def deleteHistory(request,college_id):
    prefix_id = college_id[0:2]
    if prefix_id == 'ST':
        try:
            copy_id = college_id
            history = History.objects.filter(updatedTo = college_id)
            history.delete()
            return JsonResponse({'success': f'{copy_id} History Deleted Successfully!'})
        except Exception as e:
           return JsonResponse({'error':f"An error occurred: {str(e)}"})

from .models import StudentDocuments, AdminDocuments, FacultyDocuments
# for uploading documents of faculty,student and admin
def document(request, type):
    user_id = None
    detail = None
    role = request.session.get('role')
    batch = None
    
    try:
        if type == 'Student':
            user_id = request.session.get('student_college_id')
            detail = Student.objects.get(college_id=user_id)
            permission = detail.permission
            if permission == True:
                permission = 'Yes'
            else: 
                permission = 'No'
            
            # Get or create documents object
            documents, created = StudentDocuments.objects.get_or_create(student=detail)
            
            year = detail.date_of_joining.year
            end_year = int(year) + int(detail.course.no_of_years)
            batch = str(str(year) + " - " + str(end_year))
            
            if request.method == 'POST':
                for i in range(1, 10):
                    field_name = f"pic{i}"
                    uploaded_file = request.FILES.get(field_name)  # Changed to request.FILES
                    if uploaded_file:
                        setattr(documents, field_name, uploaded_file)
                documents.save()
                messages.success(request, "Document Uploaded Successfully!")
                
        elif type == 'Faculty':
            user_id = request.session.get('faculty_college_id')
            detail = Faculty.objects.get(college_id=user_id)
            documents, created = FacultyDocuments.objects.get_or_create(faculty=detail)
            
            if request.method == 'POST':
                for i in range(1, 6):  # Faculty has only 5 documents
                    field_name = f"pic{i}"
                    uploaded_file = request.FILES.get(field_name)  # Changed to request.FILES
                    if uploaded_file:
                        setattr(documents, field_name, uploaded_file)
                documents.save()
                messages.success(request, "Document Uploaded Successfully!")
                
        elif type == 'Admin':
            user_id = request.session.get('admin_college_id')
            detail = Admin.objects.get(college_id=user_id)
            documents, created = AdminDocuments.objects.get_or_create(admin=detail)
            
            if request.method == 'POST':
                for i in range(1, 6):  # Admin has only 5 documents
                    field_name = f"pic{i}"
                    uploaded_file = request.FILES.get(field_name)  # Changed to request.FILES
                    if uploaded_file:
                        setattr(documents, field_name, uploaded_file)
                documents.save()
                messages.success(request, "Document Uploaded Successfully!")
                
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        
    return render(request, 'main/document.html', {
        'type': type, 
        'detail': detail, 
        'role': role, 
        'batch': batch, 
        'documents': documents
    })


def getDocuments(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        college_id = data.get('college_id')
        documentid = data.get('documentid')
        exists = None
        prefix_id = college_id[0:2]
        
        if prefix_id == 'AD':
            detail = Admin.objects.get(college_id = college_id)
            exists = AdminDocuments.objects.filter(admin = detail).exists()
            if exists:
                return JsonResponse({'success':True})
            else : 
                return JsonResponse({'success':False})
        elif prefix_id == 'GK':
            detail = Faculty.objects.get(college_id = college_id)
            exists = FacultyDocuments.objects.filter(faculty = detail).exists()
            if exists:
                return JsonResponse({'success':True})
            else : 
                return JsonResponse({'success':False})
        else :
            detail = Student.objects.get(college_id = college_id)
            exists = StudentDocuments.objects.filter(student = detail).exists()
            if exists:
                return JsonResponse({'success':True})
            else : 
                return JsonResponse({'success':False})
            
               
def viewDocuments(request, college_id, documentid):
    role = request.session.get('role')
    try:
        prefix_id = college_id[0:2]
        docName = None
        
        if prefix_id == 'AD':
            detail = Admin.objects.get(college_id=college_id)
            documents = AdminDocuments.objects.get(admin=detail)
            docName = getattr(documents, documentid, None)
            
        elif prefix_id == 'GK':
            detail = Faculty.objects.get(college_id=college_id)
            documents = FacultyDocuments.objects.get(faculty=detail)
            docName = getattr(documents, documentid, None)
            
        else:
            detail = Student.objects.get(college_id=college_id)
            documents = StudentDocuments.objects.get(student=detail)  # Fixed: student
            docName = getattr(documents, documentid, None)
            
        if not docName:
            return render(request, 'main/viewDocument.html', {
                'error': 'Document not found'
            })
            
        return render(request, 'main/viewDocument.html', {'docName': docName,'role':role})
        
    except Exception as e:
        return render(request, 'main/viewDocument.html', {
            'error': f'Error loading document: {str(e)}'
        })
     
    
    






from django.http import JsonResponse
def get_data_fetch(request):
   return render(request,'student_list.html')
from .models import Students
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Student

# All students list
def students_list(request):
    students = list(Students.objects.values("roll_no", "name", "course"))
    return JsonResponse({"students": students})

# Single student detail
def student_detail(request, roll_no):
    try:
        student = Students.objects.get(roll_no=roll_no)
        return JsonResponse({
            "roll_no": student.roll_no,
            "name": student.name,
            "course": student.course
        })
    except Students.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)

# Bulk delete
@csrf_exempt
def delete_students(request):
    if request.method == "POST":
        data = json.loads(request.body)
        roll_nos = data.get("roll_nos", [])
        deleted_students = list(Students.objects.filter(roll_no__in=roll_nos).values("roll_no", "name", "course"))
        Students.objects.filter(roll_no__in=roll_nos).delete()
        return JsonResponse({"message": "Selected students deleted", "deleted": deleted_students})
    return JsonResponse({"error": "Invalid Request"}, status=400)


    
