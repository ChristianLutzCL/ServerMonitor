import requests, re, socket

def ping(url, prefix="https://"): #TODO: Rework ping function

    if not check_valid_url(url):
        return prefix + url

    return url


def monitor_website(url):
    r = requests.get(url)

    if r.status_code == 200:
        print(r.status_code)
        return r.url, r.status_code, r.reason
    elif r.status_code != 200:
        print(r.status_code)
        return r.url, r.status_code, r.reason


def check_valid_url(url):
    regex = r"((http:\/\/)|(https:\/\/)){0,1}([a-zA-Z0-9-]+\.)+([a-zA-Z])+"
    pattern = re.compile(regex)

    if not pattern.match(url):
        print("Regex check failed!")

    return pattern.match(url)
    

def tracert(): #TODO tracert
    pass


def get_server_ip(url):
    return socket.gethostbyname(url)