import requests, re, socket

def ping(url, prefix="https://"): #TODO: Rework ping function

    if check_valid_url(url) != 'ERROR':
        return url
    else:
        return 'https://www.inspiredprogrammer.com'


def monitor_website(url):
    r = requests.get(url)

    if r.status_code == 200:
        print(r.status_code)
        # return r.url, r.status_code, r.reason, isdown
        return r.url, r.status_code, r.reason, False 
    elif r.status_code != 200:
        print(r.status_code)
        return r.url, r.status_code, r.reason, True 


def check_valid_url(url):
    #regex = r"((http:\/\/)|(https:\/\/)){0,1}([a-zA-Z0-9-]+\.)+([a-zA-Z])+"
    regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    pattern = re.compile(regex)

    if not pattern.match(url):
        print("Regex check failed!")
        return 'ERROR'
    else:
        print("Regex check OK!")
        return url
    

def tracert(): #TODO tracert
    pass


def get_server_ip(url):
    return socket.gethostbyname(url)