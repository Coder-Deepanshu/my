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

def personal_college_pin_for_faculty(order):
    if order:
        pin = '57575'
    else:
        pin = ''
    return pin

def personal_college_pin_for_admin(order):
    if order:
        pin = '98128'
    else:
        pin = ''
    return pin

def valid_timing_for_qr_code(start):
    if start:
        time_in_minutes = 30
    else:
        time_in_minutes = 0
    return time_in_minutes
