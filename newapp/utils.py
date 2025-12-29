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
    college_network = ipaddress.ip_network("117.237.2.0/24")
    return ipaddress.ip_address(ip) in college_network

def personal_college_pin(order):
    if order:
        pin = '9812860172'
    else:
        pin = ''
    return pin

