from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # urls for login
    path('', views.home, name='home'),
    path('Feature/', views.feature, name='feature'),
    path('Success-Stories/', views.success_stories, name='success_stories'),
    path('Contact-Details/', views.contact, name='contact'),
    path('Course-Details/', views.pricing, name='pricing'),
    path('Demo-Book/', views.demo, name='demo'),
    path('Enroll/', views.enroll, name='enroll'),
    path('Home/Enroll/', views.new_enroll, name='new_enroll'),
    path('Home/Login-In/', views.login_view, name='login'),
    path('Log-Out/', views.logout_view, name='logoutdoor'),

    # urls for dashboards
    path('Admin/Dashboard/', views.dashboard_view, name='dashboard'),
    path('Faculty/Dashboard/', views.dashboard1, name='dashboard1'),
    path('Student/Dashboard/', views.dashboard2, name='dashboard2'), 

    # urls for student functions
    path("Admin-Dashboard/Student-Management/", views.student_functions, name="student_function"),
    path('students/', views.student_filter_page,name='students'),
    path('get_course_details/', views.get_course_details),
    path('filter_students/', views.filter_students),
    path('student/<int:id>/delete/', views.delete_students, name='delete_student'),
    path('bulk_update_students/', views.bulk_update_students, name='bulk_update_students'),

    # urls for faculty functions 
    path("Admin-Dashboard/Faculty-Management/", views.faculty_functions, name="faculty_functions"),
    path("Super-Admin/Admin-Management/", views.admin_functions, name="admin_functions"),

    # urls for profile
    path("Dashboard/Profile/", views.profile_details, name="profile_details"),

    # for id card
    path("Dashboard/ID-Card", views.id_card, name="id_card"),
    path('Login-In/Forgot-Password/', views.forget_password, name='forgot_password'),
    path('admin-adding-page/', views.admin_adding_page, name='admin_adding_page'),
    path('admin-card/', views.admin_card, name='admin_card'),
    
    path('profile_upload/', views.profile_upload, name='profile_upload'),
    
    # for attendance management student-faculty
    path('Faculty/Dashboard/Student-Attendance', views.student_filtering_page, name='student_filtering_page'),
    path('get_details/', views.get_details, name='get_details'),
    path('filtering_students/', views.filtering_students, name='filtering_students'),
    path('save_attendance/', views.save_attendance, name='save_attendance'),
    path('Student/Dashboard/Attendance/', views.student_attendance_view, name='student_attendance_view'),
    path('get_student_attendance/', views.get_student_attendance, name='get_student_attendance'),
    path('Student/Dashboard/Fees/', views.student_fees_view, name='student_fees_view'),
    
    # Fee Management URLs
    path('fee-management/', views.admin_fee_management, name='admin_fee_management'),
    path('student-fee-details/<str:student_id>/', views.student_fee_details, name='student_fee_details'),
    path('process-fee-payment/', views.process_fee_payment, name='process_fee_payment'),
    path('adjust_extra_payments/', views.adjust_extra_payments, name='adjust_extra_payments'),
    path('get_receipt_data/<str:receipt_number>/', views.get_receipt_data, name='get_receipt_data'),

# for chatting management between faculty and student
    path('chat_home/', views.chat_home, name='chat_home'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),

    # for send message and gwt messages
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/<int:room_id>/', views.get_messages, name='get_messages'),
    # for sending info about faculty
    path('Student/Dashboard/Chat-Faculty', views.get_faculty_details, name='get_faculty_details'),
    path('faculty_filtering/', views.faculty_filtering, name='faculty_filtering'),
    path('toggle_follow/', views.toggle_follow, name='toggle_follow'),
    # for sending info about student
    path('faculty/students/', views.faculty_student_list, name='faculty_student_list'),
    path('send_course_details/', views.send_course_details, name='send_course_details'),
    path('faculty/students/', views.student_filter_details, name='student_list_partial'),
    # urls.py
    path('delete_chat/<int:room_id>/', views.delete_chat, name='delete_chat'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)