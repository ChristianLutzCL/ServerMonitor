import requests


def monitor_website(url):
    r = requests.get(url)
    
    if r.status_code == 200:
        print(r.status_code)
        return r.url + " | " + str(r.status_code)
    elif r.status_code != 200:
        print("RESPONSE FAILED")
        return "RESPONSE FAILED"
