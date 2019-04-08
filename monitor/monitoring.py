import requests
import socket


def monitor_website(url):
    r = requests.get(url)

    if r.status_code == 200:
        print(r.status_code)
        return r.url, r.status_code, r.reason
    elif r.status_code != 200:
        print(r.status_code)
        return r.url, r.status_code, r.reason


def clear_url():
    pass
    

def tracert(): #TODO
    pass


def get_server_ip(url):
    return socket.gethostbyname(url)