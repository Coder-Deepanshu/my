from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # urls for login
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logoutdoor'),
    # urls for dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard1/', views.dashboard1, name='dashboard1'),
    path('dashboard2/', views.dashboard2, name='dashboard2'), 
    # urls for student functions
    path("student/", views.student_functions, name="student"),
    path('students/', views.student_filter_page,name='students'),
    path('get_course_details/', views.get_course_details),
    path('filter_students/', views.filter_students),
    path('student/<int:id>/delete/', views.delete_students, name='delete_student'),
    path('bulk_update_students/', views.bulk_update_students, name='bulk_update_students'),
    # urls for faculty functions 
    path("faculty_functions/", views.faculty_functions, name="faculty_functions"),
    # urls for profile
    path("profile_details/", views.profile_details, name="profile_details"),
    # for id card
    path("id_card/", views.id_card, name="id_card"),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    path('add-new-admin/', views.add_new_admin, name='add_new_admin'),
    path('profile_upload/', views.profile_upload, name='profile_upload'),
    # for attendance management student-faculty
    path('student_filtering_page/', views.student_filtering_page, name='student_filtering_page'),
    path('get_details/', views.get_details, name='get_details'),
    path('filtering_students/', views.filtering_students, name='filtering_students'),
    path('save_attendance/', views.save_attendance, name='save_attendance'),
    path('student_attendance_view', views.student_attendance_view, name='student_attendance_view'),
    path('get_student_attendance/', views.get_student_attendance, name='get_student_attendance'),
    path('admin_student_fees_view', views.admin_student_fees_view, name='admin_student_fees_view'),
    path('admin/students/fees/<str:student_id>/', views.admin_update_fees, name='admin_update_fees'),
    path('fee_structures_view/', views.fee_structures_view, name='fee_structures_view'),
    path('admin/fee-structures/add/', views.add_fee_structure, name='add_fee_structure'),
    path('student_fees_view/', views.student_fees_view, name='student_fees_view'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)