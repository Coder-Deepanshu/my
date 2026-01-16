# attendance/utils.py
import ipaddress

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_college_wifi(ip):
    # College Wi-Fi IP Range
    college_network = ipaddress.ip_network("152.59.90.0/24")
    return ipaddress.ip_address(ip) in college_network

def personal_college_pin(order, user):
    pin = ''
    if order:
        if user == 'Admin':        
             pin = '98128'
        elif user == 'Faculty':        
             pin = '98128'
        elif user == 'Student':        
             pin = '98128'
    return pin

def valid_timing_for_qr_code(start):
    if start:
        time_in_minutes = 1 # in minutes
    else:
        time_in_minutes = 0
    return time_in_minutes

# utils.py me
def special_login_detail(start):  # ✅ sepecial -> special
    # username = ''
    # password = ''
    if start:
        username = 'Deepanshu'
        password = '98128601'
    return username, password

def special_login_permission(start):
    permission = 'Block'  # Default
    if start:
        permission = 'Access'
    return permission

def leaves_limit(start):
    total = 0
    if start:
        total = 15

    return total

def background_leave_time(start):
    time = 0
    if start:
        time = 1
    return time