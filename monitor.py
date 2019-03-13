import requests


def monitor_website(url):
    r = requests.get(url, timeout=5)
    
    if r.status_code == 200:
        print(r.status_code)
        return "RESPONSE OK "
    elif r.status_code != 200:
        print("RESPONSE FAILED")
        return "RESPONSE FAILED"
