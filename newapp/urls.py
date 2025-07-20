from django.contrib import admin
from django.urls import path
from newapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logoutdoor'),
    # path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    # path('generate-csv/', views.generate_csv, name='generate_csv'),
    path("student/", views.student_functions, name="student"),
    path('dashboard1/', views.dashboard1, name='dashboard1'),
    path('dashboard2/', views.dashboard2, name='dashboard2'),
    path('add_faculty/', views.add_faculty, name='add_faculty'),
    path('delete-faculty/', views.delete_faculty, name='delete_faculty'),
    path('confirm-delete-faculty/<int:faculty_id>/', views.confirm_delete_faculty, name='confirm_delete_faculty'),
    path('view_faculty/', views.view_faculty, name='view_faculty'),
    path('admin_attendance/', views.admin_attendance, name='admin_attendance'),
    path('save-attendance/', views.save_attendance, name='save_attendance'),
    path('faculty_attendance/', views.faculty_attendance, name='faculty_attendance'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)