from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Student, Faculty, Course, Attendance,Admin # Import the new Attendance model
from django.http import JsonResponse
import json # For handling JSON data from AJAX requests
from django.shortcuts import render, redirect

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
            admin_email = Admin.objects.all().values_list('email',flat=True)
            if username in admin_email :
                admin_detail = Admin.objects.get(email=username)
                user_id = admin_detail.college_id
                admin_phone = admin_detail.phone
                if (password==admin_phone and user_id == user_id):
                    request.session['username1'] =  admin_detail.name
                    request.session['admin_college_id']= user_id
                    request.session['role'] = role
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid admin credentials")
                    return redirect('login')
                
            elif username =='Deepanshu' and user_id =='AD20250' and password == '12345' :
                    request.session['username1'] =  username
                    request.session['admin_college_id']= user_id
                    request.session['role'] = role
                    return redirect('dashboard')

            else:
                messages.error(request, "Invalid admin credentials")
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
    username = request.session.get('User_name')
    return render(request,'admin/admin_page.html',{'username':username})

def admin_card(request):
    username = request.session.get('User_name')
    admin_details = Admin.objects.all()
    return render(request,'admin/admin_card.html',{'username':username,'admin_details':admin_details})

# profile details   
def profile_details(request):
    role = request.session.get('role')
    if role == 'faculty':
        faculty_id=request.session.get('faculty_college_id')
        details=Faculty.objects.get(college_id=faculty_id)
        return render(request,'profile.html',{'faculty':details})
    elif role == 'student':
        student_id=request.session.get('student_college_id')
        details=Student.objects.get(college_id=student_id)
        return render(request,'profile.html',{'student':details})
    elif role == 'admin':
        admin_id=request.session.get('admin_college_id')
        details=Admin.objects.get(college_id=admin_id)
        return render(request,'profile.html',{'admin':details})

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
    
    return render(request, 'id_card.html', context)

# for admin dashboard
def dashboard_view(request):
    # Check if the user is logged in
    username = request.session.get('username1')
    college_id = request.session.get('admin_college_id')
    if username:
        return render(request, 'dashboard.html', {'username': username,'college_id':college_id})
    else:
        return redirect('login') 

# for faculty dashboard
def dashboard1(request):
    # Check if the user is logged in
    username = request.session.get('username2')  # Retrieve username from session
    if username:
        return render(request, 'dashboard1.html', {'username': username})
    else:
        return redirect('login')  # Redirect to login if not logged in

# for student dashboard
def dashboard2(request):
    # Check if the user is logged in
    username = request.session.get('username3')
    college_id = request.session.get('student_college_id')
    detail = Student.objects.get(college_id = college_id)  # Retrieve username from session
    if username:
        return render(request, 'dashboard2.html', {'username': username,'detail':detail})
    else:
        return redirect('login') 

# for logout from account
def logout_view(request):
    # Clear session data
    request.session.flush()
    return redirect('login')

# for single students operations 
def student_functions(request):
    context = {}

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
                    course=request.POST.get("course"),
                    level=request.POST.get("education"),
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

#  for multiple student filtering
from django.template.loader import render_to_string

from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from .models import Course, Student

def student_filter_page(request):
    try:
        # Get all courses from Course model (not from Student records)
        courses = Course.objects.all().values_list('name', flat=True)
        students = Student.objects.all()
        return render(request, 'student/student_filter.html', {'courses': courses, 'students': students})
    except Exception as e:
        messages.error(request, f"Error loading courses: {str(e)}")
        return render(request, 'student/student_filter.html', {'courses': []})

def get_course_details(request):
    try:
        course_name = request.GET.get('course_name')
        if not course_name:
            return JsonResponse({'error': 'Course name is required'}, status=400)
    
        course = Course.objects.get(name=course_name)
        return JsonResponse({
            'years': list(range(1, course.no_of_years + 1)),
            'semesters': list(range(1, course.no_of_semesters + 1))
        })
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def filter_students(request):
    filters = {
        'course': request.GET.get('course', 'all'),
        'year': request.GET.get('year', 'all'),
        'semester': request.GET.get('semester', 'all'),
        'college_id': request.GET.get('college_id', '')
    }

    students = Student.objects.all()
    
    if filters['course'] != 'all':
        students = students.filter(course=filters['course'])
    if filters['year'] != 'all':
        students = students.filter(year=filters['year'])
    if filters['semester'] != 'all':
        students = students.filter(semester=filters['semester'])
    if filters['college_id']:
        students = students.filter(college_id__icontains=filters['college_id'])

    html = render_to_string('student/student_result_partial.html', {'students': students})
    return JsonResponse({'html': html})

@csrf_exempt
def bulk_update_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids[]')
        
        # Prepare update data - only include fields that have values
        update_data = {}
        fields_to_update = ['father_name',
            'course', 'year', 'semester', 
            'address', 'city', 'state', 'country'
        ]
        
        for field in fields_to_update:
            if request.POST.get(field):
                if field in ['year', 'semester']:
                    update_data[field] = int(request.POST.get(field))
                else:
                    update_data[field] = request.POST.get(field)
        
        if not update_data:
            return JsonResponse({'error': 'No fields to update'}, status=400)
            
        try:
            # Only update if we have both student IDs and data to update
            if student_ids and update_data:
                Student.objects.filter(id__in=student_ids).update(**update_data)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'No students selected or no data to update'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt
def delete_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids[]')
        try:
            Student.objects.filter(id__in=student_ids).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# for  faculty management
from django.db import models
def faculty_functions(request):
    context = {}
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
                    position=request.POST.get("position"),
                    gender=request.POST.get("gender"),
                    department=request.POST.get("department"),
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
                    position=request.POST.get("position"),
                    gender=request.POST.get("gender"),
                    department=request.POST.get("department"),
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

# 
# # 
# 
# # 
#            Attendance System Code
# # 
# 
# # 
# 
# for attendance management student-faculty
from django.utils import timezone
def student_filtering_page(request):
    try:
        courses = Course.objects.all().values_list('name', flat=True)
        return render(request, 'faculty_filtering.html', {'courses': courses})
    except Exception as e:
        messages.error(request, f"Error loading courses: {str(e)}")
        return render(request, 'faculty_filtering.html', {'courses': []})

def get_details(request):
    try:
        course_name = request.GET.get('course_name')
        if not course_name or course_name == 'all':
            return JsonResponse({'error': 'Please select a valid course'}, status=400)
            
        # Get the course - make sure name matching is case-insensitive
        course = Course.objects.filter(name__iexact=course_name).first()
        if not course:
            return JsonResponse({'error': f'Course "{course_name}" not found'}, status=404)
            
        return JsonResponse({
            'years': list(range(1, course.no_of_years + 1)),
            'semesters': list(range(1, course.no_of_semesters + 1)),
            'lectures': list(range(1, course.lecture + 1))
        })
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
# for filtering student details at faculty portal 
def filtering_students(request):
    if not request.session.get('faculty_college_id'):
        messages.error(request, "Please login as faculty first")
        return redirect('login')
        
    filters = {
        'course': request.GET.get('course', 'all'),
        'year': request.GET.get('year', 'all'),
        'semester': request.GET.get('semester', 'all'),
        'college_id': request.GET.get('college_id', '')
    }

    students = Student.objects.all()
    
    if filters['course'] != 'all':
        students = students.filter(course=filters['course'])
    if filters['year'] != 'all':
        students = students.filter(year=filters['year'])
    if filters['semester'] != 'all':
        students = students.filter(semester=filters['semester'])
    if filters['college_id']:
        students = students.filter(college_id__icontains=filters['college_id'])

    html = render_to_string('student/student_table.html', {'students': students})
    return JsonResponse({'html': html})
# for saving attendance details
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
            course = Course.objects.get(name=course_name)
            
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
def student_attendance_view(request):
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
            'current_year': current_year
        })
        
    except Student.DoesNotExist:
        messages.error(request, "Student not found")
        return redirect('dashboard2')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('dashboard2')
    
# for student attendance (for student viewing attendance)
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
        
        # Calculate summary
        total_lectures = attendance.count()
        present = attendance.filter(status='Present').count()
        absent = attendance.filter(status='Absent').count()
        
        attendance_percentage = 0
        if total_lectures > 0:
            attendance_percentage = round((present / total_lectures) * 100, 2)
            
        attendance_list = []
        for record in attendance:
            attendance_list.append({
                'date': record.date,
                'lecture_number': record.lecture_number,
                'course_name': record.course.name if record.course else 'N/A',
                'status': record.status,
                'faculty_name': record.faculty.name if record.faculty else 'N/A',
                'time': record.timing.strftime('%H:%M:%S') if record.timing else 'N/A'
            })
            
        return JsonResponse({
            'attendance': attendance_list,
            'summary': {
                'total_lectures': total_lectures,
                'present': present,
                'absent': absent,
                'attendance_percentage': attendance_percentage
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# FOR FEES MANAGEMENT OF STUDENT
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.db.models import DecimalField
from decimal import Decimal
from .models import Student, Course, FeeStructure, FeePayment,StudentBalance


#  for student, for viewing fees
def student_fees_view(request):
    if 'username3' not in request.session:
        return redirect('login')
    
    try:
        student = Student.objects.get(college_id=request.session['student_college_id'])
        
        # Get the Course object based on the student's course name
        try:
            course = Course.objects.get(name=student.course)
            no_of_years = course.no_of_years
        except Course.DoesNotExist:
            messages.error(request, "Course information not found")
            return redirect('dashboard2')
        
        # Get all fee structures for this course
        batch_year=student.date_of_joining.year
        course_fee_structures = FeeStructure.objects.filter(course=course)
        course_fee_structure_batchyear = course_fee_structures.filter(for_year=batch_year)
        
        # Calculate total semester fee with proper type handling and  calculate the total course fees
        total_semester_fee = course_fee_structure_batchyear.aggregate(
            total=Coalesce(
                Sum('amount', output_field=DecimalField(max_digits=10, decimal_places=2)),
                Decimal('0.00'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )['total'] or Decimal('0.00')


        if course_fee_structure_batchyear.exists():
            total_course_fees = course.fees_per_year * course.no_of_years
        else :
            total_course_fees = Decimal('0.00')
    
        # Get all payments for this student
        all_payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
        
        # Calculate total payment with proper type handling
        total_payment = all_payments.aggregate(
            total=Coalesce(
                Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2)),
                Decimal('0.00'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )['total'] or Decimal('0.00')
        
        # Calculate total due amount
        total_due_amount = total_semester_fee - total_payment
        
        # Prepare year-wise data with proper decimal handling
        year_wise_data = []
        for year in range(1, no_of_years + 1):
            # Get fee structures for this year
            batch_year = student.date_of_joining.year
            semester = (student.semester)+1

            # for batch yaer wise fees matching with fees structure
            year_fees = course_fee_structures.filter(year=year)
            year_fees_of_batchyear = year_fees.filter(for_year=batch_year)
            year_total = year_fees_of_batchyear.aggregate(
            total=Sum('amount', output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total'] or Decimal('0.00')

            # Get the due date for current semester
            current_semester_fee = year_fees_of_batchyear.filter(semester=semester).first()
            due_date = current_semester_fee.due_date if current_semester_fee else None
            
            # Get payments for this year
            year_payments = all_payments.filter(fee_structure__year=year)

            year_paid = year_payments.aggregate(
                total=Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total'] or Decimal('0.00')
            
            # Determine status
            if year_total == Decimal('0.00'):
                status = "No Fee"
            elif year_paid >= year_total:
                status = "Paid" 
            elif year_paid > Decimal('0.00'):
                status = "Partial"
            else:
                status = "Pending"
            
            year_wise_data.append({
                'year': year,
                'amount': year_total,
                'paid': year_paid,
                'due': year_total - year_paid,
                'status': status,
                'payments': year_payments,
                'due_date': due_date  # Now this will be a single date or None
            })
          
        context = {
            'student': student,
            'course': course,
            'total_semester_fees': total_semester_fee,
            'total_paid': total_payment,
            'total_due': total_due_amount,
            'total_course_fees':total_course_fees,
            'payment_percentage': float((total_payment / total_semester_fee * 100)) if total_semester_fee > Decimal('0.00') else 0,
            'year_wise_data': year_wise_data,
            'all_payments': all_payments,
        }
        
        return render(request, 'student/student_fees_view.html', context)
        
    except Student.DoesNotExist:
        messages.error(request, "Student not found")
        return redirect('dashboard2')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('dashboard2')
    
# for admin dashboard for voewing students fees
def admin_fee_management(request):
    if 'username1' not in request.session:
        return redirect('login')
    
    # Get all courses for filter dropdown
    courses = Course.objects.all()
    
    # Default filter values
    course_filter = None
    year_filter = None
    semester_filter = None
    college_id_filter = None
    
    # Check if filters are applied
    if request.method == 'GET':
        course_filter = request.GET.get('course', '')
        year_filter = request.GET.get('year', '')
        semester_filter = request.GET.get('semester', '')
        college_id_filter = request.GET.get('college_id', '')
    
    # Build the filter query
    filters = Q()
    if course_filter:
        filters &= Q(course=course_filter)
    if year_filter:
        filters &= Q(year=year_filter)
    if semester_filter:
        filters &= Q(semester=semester_filter)
    if college_id_filter:
        filters &= Q(college_id__icontains=college_id_filter)
    
    # Get filtered students
    students = Student.objects.filter(filters).order_by('college_id')
    
    # Prepare student data with fee summaries
    student_data = []
    for student in students:
        try:
            course = Course.objects.get(name=student.course)
            batch_year =  student.date_of_joining.year
            fee_structures = FeeStructure.objects.filter(course=course).filter(for_year=batch_year)
            
            # Calculate total course fee
            total_course_fee = fee_structures.aggregate(
                total=Coalesce(
                    Sum('amount', output_field=DecimalField(max_digits=10, decimal_places=2)),
                    Decimal('0.00'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )['total'] or Decimal('0.00')
            
            # Get all payments for this student
            all_payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
            
            # Calculate total payment
            total_payment = all_payments.aggregate(
                total=Coalesce(
                    Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2)),
                    Decimal('0.00'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )['total'] or Decimal('0.00')
            
            # Calculate total due amount
            if total_course_fee >= total_payment:
               total_due_amount = total_course_fee - total_payment
            
            else:
                total_due_amount = total_course_fee - total_payment #due amount which paid by student in advance 
            
            student_data.append({
                'student': student,
                'total_course_fee': total_course_fee,
                'total_paid': total_payment,
                'total_due': total_due_amount,
                'payment_percentage': float((total_payment / total_course_fee * 100)) if total_course_fee > Decimal('0.00') else 0,
            })
        except Exception as e:
            messages.error(request, f"Error processing student {student.college_id}: {str(e)}")
            continue
    
    context = {
        'courses': courses,
        'student_data': student_data,
        'selected_course': course_filter,
        'selected_year': year_filter,
        'selected_semester': semester_filter,
        'selected_college_id': college_id_filter,
    }
    
    return render(request, 'admin/admin_fee_management.html', context)

# for sending courses available to the admin dashboard
def get_course_details(request):
    if request.method == 'GET' and 'course_name' in request.GET:
        course_name = request.GET.get('course_name')
        try:
            course = Course.objects.get(name=course_name)
            
            # Get unique years and semesters from fee structures for this course
            years = FeeStructure.objects.filter(course=course).values_list('year', flat=True).distinct().order_by('year')
            semesters = FeeStructure.objects.filter(course=course).values_list('semester', flat=True).distinct().order_by('semester')
            
            return JsonResponse({
                'success': True,
                'years': list(years),
                'semesters': list(semesters),
            })
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# for sending fees details to the student detail template
from django.db.models import Sum, Q, F, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal
import time

def student_fee_details(request, student_id):
    if 'username1' not in request.session:
        return redirect('login')
    
    try:
        student = Student.objects.get(college_id=student_id)
        balance, _ = StudentBalance.objects.get_or_create(student=student)
        
        # Get the Course object
        try:
            batch_year = student.date_of_joining.year
            course = Course.objects.get(name=student.course)
            no_of_years = course.no_of_years
        except Course.DoesNotExist:
            messages.error(request, "Course information not found")
            return redirect('admin_fee_management')
        
        # Get all fee structures for this course
        course_fee_structures = FeeStructure.objects.filter(course=course, for_year=batch_year)
        
        # Calculate total course fee
        total_course_fee = course_fee_structures.aggregate(
            total=Coalesce(
                Sum('amount', output_field=DecimalField(max_digits=10, decimal_places=2)),
                Decimal('0.00'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )['total'] or Decimal('0.00')
        
        # Get all payments for this student
        all_payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
        
        # Calculate total payment
        total_payment = all_payments.aggregate(
            total=Coalesce(
                Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2)),
                Decimal('0.00'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )['total'] or Decimal('0.00')
        
        # Calculate total due amount (considering extra and advance payments)
        total_due_amount = max(total_course_fee - total_payment, Decimal('0.00'))
        
        # Prepare year-wise data
        year_wise_data = []
        for year in range(1, no_of_years + 1):
            year_fees = course_fee_structures.filter(year=year)
            year_total = year_fees.aggregate(
                total=Sum('amount', output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total'] or Decimal('0.00')
            
            year_payments = all_payments.filter(
                Q(fee_structure__year=year) | 
                Q(payment_type='ADVANCE') |
                Q(payment_type='ADJUSTMENT')
            )
            
            year_paid = year_payments.aggregate(
                total=Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2))
            )['total'] or Decimal('0.00')

            # Create list of fee structures with payment info
            fee_details = []
            for fee in year_fees:
                payments = year_payments.filter(fee_structure=fee)
                paid_amount = payments.aggregate(
                    total=Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2))
                )['total'] or Decimal('0.00')
                
                fee_details.append({
                    'fee': fee,
                    'payments': payments,
                    'paid_amount': paid_amount,
                    'is_paid': paid_amount >= fee.amount
                })

            status = "No Fee" if year_total == Decimal('0.00') else \
                     "Paid" if year_paid >= year_total else \
                     "Partial" if year_paid > Decimal('0.00') else \
                     "Pending"
            
            year_wise_data.append({
                'year': year,
                'amount': year_total,
                'paid': year_paid,
                'due': max(year_total - year_paid, Decimal('0.00')),
                'status': status,
                'payments': year_payments,
                'fee_details': fee_details,
                'extra_payments': all_payments.filter(payment_type='EXTRA', fee_structure__year=year),
                'advance_payments': all_payments.filter(payment_type='ADVANCE', fee_structure__year=year)
            })
        extra_payments = [p for p in all_payments if p.payment_type == "EXTRA"]
        advance_payments = [p for p in all_payments if p.payment_type == "ADVANCE"]
        context = {
            'student': student,
            'course': course,
            'total_course_fee': total_course_fee,
            'total_paid': total_payment,
            'total_due': total_due_amount,
            'payment_percentage': float((total_payment / total_course_fee * 100)) if total_course_fee > Decimal('0.00') else 0,
            'year_wise_data': year_wise_data,
            'all_payments': all_payments,
            'extra_payments': extra_payments,
            'advance_payments': advance_payments,
        }
        
        return render(request, 'student/student_fee_detail.html', context)
        
    except Student.DoesNotExist:
        messages.error(request, "Student not found")
        return redirect('admin_fee_management')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('admin_fee_management')

@csrf_exempt
def process_fee_payment(request):
    if 'username1' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            fee_structure_id = data.get('fee_structure_id')
            amount = Decimal(data.get('amount'))
            payment_method = data.get('payment_method')
            transaction_id = data.get('transaction_id')
            remarks = data.get('remarks', '')
            
            # Validate required fields
            if not all([student_id, fee_structure_id, amount, payment_method]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            try:
                student = Student.objects.get(college_id=student_id)
                fee_structure = FeeStructure.objects.get(id=fee_structure_id)
                balance = StudentBalance.objects.get(student=student)
            except (Student.DoesNotExist, FeeStructure.DoesNotExist, StudentBalance.DoesNotExist) as e:
                return JsonResponse({'error': str(e)}, status=404)
            
            # Check if this is an advance payment (for a future semester)
            current_semester = student.semester
            is_advance = fee_structure.semester > current_semester
            
            # Calculate how much is remaining for this fee structure
            paid_for_structure = FeePayment.objects.filter(
                student=student,
                fee_structure=fee_structure
            ).aggregate(
                total=Coalesce(
                    Sum('amount_paid', output_field=DecimalField(max_digits=10, decimal_places=2)),
                    Decimal('0.00'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )['total'] or Decimal('0.00')
            
            remaining_amount = fee_structure.amount - paid_for_structure
            
            payment_type = 'REGULAR'
            adjusted_in = None
            
            if amount > remaining_amount:
                # This is an extra payment
                extra_amount = amount - remaining_amount
                balance.extra_amount += extra_amount
                balance.save()
                
                # Create two payment records - one for regular, one for extra
                if remaining_amount > 0:
                    regular_payment = FeePayment(
                        student=student,
                        fee_structure=fee_structure,
                        amount_paid=remaining_amount,
                        payment_method=payment_method,
                        transaction_id=transaction_id,
                        receipt_number=f"RCPT-{student.college_id}-{int(time.time())}-1",
                        remarks=remarks,
                        verified_by=request.session['username1'],
                        status='Paid',
                        payment_type='REGULAR'
                    )
                    regular_payment.save()
                
                extra_payment = FeePayment(
                    student=student,
                    fee_structure=fee_structure,
                    amount_paid=extra_amount,
                    payment_method=payment_method,
                    transaction_id=transaction_id,
                    receipt_number=f"RCPT-{student.college_id}-{int(time.time())}-2",
                    remarks=f"Extra payment - {remarks}",
                    verified_by=request.session['username1'],
                    status='Paid',
                    payment_type='EXTRA'
                )
                extra_payment.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Payment processed with extra amount',
                    'receipt_numbers': [regular_payment.receipt_number, extra_payment.receipt_number],
                    'payment_date': regular_payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_extra': True
                })
            elif is_advance:
                # This is an advance payment for future semester
                balance.advance_amount += amount
                balance.save()
                
                advance_payment = FeePayment(
                    student=student,
                    fee_structure=fee_structure,
                    amount_paid=amount,
                    payment_method=payment_method,
                    transaction_id=transaction_id,
                    receipt_number=f"RCPT-{student.college_id}-{int(time.time())}",
                    remarks=f"Advance payment - {remarks}",
                    verified_by=request.session['username1'],
                    status='Paid',
                    payment_type='ADVANCE'
                )
                advance_payment.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Advance payment processed successfully',
                    'receipt_number': advance_payment.receipt_number,
                    'payment_date': advance_payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_advance': True
                })
            else:
                # Regular payment
                payment = FeePayment(
                    student=student,
                    fee_structure=fee_structure,
                    amount_paid=amount,
                    payment_method=payment_method,
                    transaction_id=transaction_id,
                    receipt_number=f"RCPT-{student.college_id}-{int(time.time())}",
                    remarks=remarks,
                    verified_by=request.session['username1'],
                    status='Paid',
                    payment_type='REGULAR'
                )
                payment.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Payment processed successfully',
                    'receipt_number': payment.receipt_number,
                    'payment_date': payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_regular': True
                })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def adjust_extra_payments(request):
    if 'username1' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            payment_id = data.get('payment_id')
            
            if not student_id or not payment_id:
                return JsonResponse({'error': 'Missing required parameters'}, status=400)
            
            # Get the payment to adjust
            extra_payment = FeePayment.objects.get(
                id=payment_id,
                student__college_id=student_id,
                payment_type='EXTRA'
            )
            
            # Find the next due payment to apply this to
            next_due_payment = FeePayment.objects.filter(
                student__college_id=student_id,
                status='Pending'
            ).order_by('fee_structure__year', 'fee_structure__semester').first()
            
            if not next_due_payment:
                return JsonResponse({'error': 'No pending payments to adjust against'}, status=400)
            
            # Create adjustment record
            adjustment = FeePayment(
                student=extra_payment.student,
                fee_structure=next_due_payment.fee_structure,
                amount_paid=extra_payment.amount_paid,
                payment_method='Adjustment',
                receipt_number=f"ADJ-{extra_payment.receipt_number}",
                remarks=f"Adjustment from extra payment {extra_payment.receipt_number}",
                verified_by=request.session['username1'],
                status='Paid',
                payment_type='ADJUSTMENT',
                adjusted_in=extra_payment
            )
            adjustment.save()
            
            # Update the extra payment to mark it as adjusted
            extra_payment.adjusted_in = adjustment
            extra_payment.save()
            
            # Update the student balance
            balance = StudentBalance.objects.get(student=extra_payment.student)
            balance.extra_amount -= extra_payment.amount_paid
            balance.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully adjusted ₹{extra_payment.amount_paid}',
                'receipt_number': adjustment.receipt_number
            })
            
        except FeePayment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)
        except StudentBalance.DoesNotExist:
            return JsonResponse({'error': 'Student balance not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# for receipt 
@csrf_exempt  # Temporary for testing, remove in production
def get_receipt_data(request, receipt_number):
    try:
        payment = FeePayment.objects.get(
            receipt_number=receipt_number,
            student__college_id=request.session.get('student_college_id')
        )
        
        return JsonResponse({
            'success': True,
            'receipt_number': payment.receipt_number,
            'student_name': payment.student.name,
            'amount_paid': str(payment.amount_paid),
            'payment_date': payment.payment_date.strftime("%d/%m/%Y"),
            'status': payment.status,
            'payment_method': payment.payment_method,
            'transaction_id': payment.transaction_id or "N/A",
            'verified_by': payment.verified_by or "Not specified",
            'remarks': payment.remarks or "None"
        })
        
    except FeePayment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Receipt not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

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
        course = Course.objects.all()
        faculty = Faculty.objects.get(college_id=request.session['faculty_college_id'])
        students = Student.objects.filter(followed_faculty=faculty)
     
        
        return render(request, 'chat/page2.html', {
            'faculty': faculty,
            'students': students,
            'courses': course,
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

from .models import Department
# department creation
def department_creation(request):
    # Always get departments list for the template
    details = Department.objects.all()
    total_department = Department.objects.count()
    total_faculty = Faculty.objects.count()
    enrolled_students = Student.objects.count()
    total_course = Course.objects.count()
    programs = Course.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('form_name')
        
        if action == 'departmentCreation':
            try:
                Department.objects.create(
                    name=request.POST.get('name'),
                    code=request.POST.get('code'),
                    type=request.POST.get('type'),
                    description=request.POST.get('description'),
                    programs_count=request.POST.get('programe'),
                    faculty_count=request.POST.get('facultyCount'),
                    student_capacity=request.POST.get('studentCapacity'),
                )
                messages.success(request, "Department Created Successfully!")
            except Exception as e:
                messages.error(request, f"Error adding department: {str(e)}")

    # Always return the render with details
    return render(request, 'department.html', {
        'details': details,
        'total_department':total_department,
        'total_faculty':total_faculty,
        'enrolled_students':enrolled_students,
        'total_course':total_course,
        'programs':programs
         })

# course craetion
from .models import Department, Course,Level

def course_creation(request):
    details = Course.objects.all()
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
                    
                    # Create course with foreign key IDs
                    Course.objects.create(
                        name=request.POST.get('courseName'),
                        department_id=request.POST.get('courseDepartment'),  # Use _id field
                        no_of_years=duration,
                        no_of_semesters=duration * 2,
                        code=request.POST.get('courseCode'),
                        description=request.POST.get('courseDescription'),
                        student_capacity=capacity,
                        level_id=request.POST.get('courseLevel'),  # Use _id field
                        fees_per_year=fees
                    )
                    messages.success(request, "Course Created Successfully!")
                    
                except ValueError:
                    messages.error(request, "Invalid number format in form data")
                except Exception as e:
                    messages.error(request, f"Error adding course: {str(e)}")
        
        # Return with context for both GET and POST
        return render(request, 'course_creation.html', {
            'department_list': department_list,
            'level_list': level_list,
            'details':details
            
        })
            
    except Exception as e:
        messages.error(request, f"Error loading page: {str(e)}")
        return render(request, 'course_creation.html', {
            'department_list': [],
            'level_list': [],
            'details':[]
        })
    
# Created Positions
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
from .models import Position, Department

def position_creation(request):
    details = Position.objects.all().select_related('department')
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
            'details': details
        })
            
    except Exception as e:
        messages.error(request, f"Error loading page: {str(e)}")
        return render(request, 'position.html', {
            'faculty_department_list': [],
            'admin_department_list': [],
            'details': []
        })


@csrf_exempt
@require_POST
def get_position_data(request):
    """Get position data for editing"""
    try:
        data = json.loads(request.body)
        position_id = data.get('position_id')
        
        position = get_object_or_404(Position, position_id=position_id)
        
        return JsonResponse({
            'success': True,
            'data': {
                'position_id': position.position_id,
                'name': position.name,
                'type': position.type,
                'department_id': position.department.id,
                'level': position.level,
                'salary': position.salary,
                'specialization': position.specialization,
                'requirment': position.requirment,
                'responsibility': position.responsibility,
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving position data: {str(e)}'
        })


@csrf_exempt
@require_POST
def update_position(request):
    """Update position data"""
    try:
        data = json.loads(request.body)
        position_id = data.get('position_id')
        
        position = get_object_or_404(Position, position_id=position_id)
        
        # Update position fields
        position.name = data.get('name')
        position.type = data.get('type')
        position.level = data.get('level')
        
        # Handle salary conversion
        try:
            salary_value = data.get('salary')
            if isinstance(salary_value, str):
                # Clean salary string - remove any non-numeric characters
                salary_str = ''.join(filter(str.isdigit, salary_value))
                position.salary = int(salary_str) if salary_str else 0
            else:
                position.salary = int(salary_value) if salary_value else 0
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'message': f'Invalid salary format: {str(e)}'
            })
        
        position.specialization = data.get('specialization')
        position.requirment = data.get('requirment')
        position.responsibility = data.get('responsibility')
        
        # Update department if provided
        department_id = data.get('department_id')
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
                position.department = department
            except Department.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid department ID'
                })
        
        position.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Position updated successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating position: {str(e)}'
        })


@csrf_exempt
@require_POST
def delete_position(request):
    """Delete a position"""
    try:
        data = json.loads(request.body)
        position_id = data.get('position_id')
        
        position = get_object_or_404(Position, position_id=position_id)
        position_name = position.name
        position.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Position "{position_name}" deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deleting position: {str(e)}'
        })