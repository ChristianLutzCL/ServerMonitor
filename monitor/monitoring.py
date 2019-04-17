import requests, re, socket

def ping(url, prefix="https://"): #TODO: Rework ping function

    if check_valid_url(url) != 'ERROR':
        return prefix + check_valid_url(url)
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
    regex = r"([a-zA-Z0-9-]+\.)+([a-zA-Z])+"
    pattern = re.compile(regex)

    spattern = pattern.search(url)
    spgroup = spattern.group(0)

    if not spgroup:
        print("Regex check failed!")
        return 'ERROR'
    else:
        print("Regex check OK!")
        return spgroup
    

def tracert(): #TODO tracert
    pass


def get_server_ip(url):
    host = check_valid_url(url)

    return socket.gethostbyname(host)