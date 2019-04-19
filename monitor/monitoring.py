from monitor import app
import requests, re, socket, json

def ping(url, prefix="https://"):

    if check_valid_url(url) != 'ERROR':
        return prefix + check_valid_url(url)
    else:
        return 'https://www.inspiredprogrammer.com'


def monitor_website(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(r.status_code)
            # return r.url, r.status_code, r.reason, isdown
            return r.url, r.status_code, r.reason, False 
        elif r.status_code != 200:
            print(r.status_code)
            return r.url, r.status_code, r.reason, True 
    except:
        return url, 'none', 'none', True


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


def check_latency(url):
    try:
        return requests.get(url).elapsed.total_seconds()
    except:
        return 'Timeout error'


def get_server_ip(url):
    host = check_valid_url(url)
    return socket.gethostbyname(host)


def get_server_location(ip):
        IPSTACK_KEY = app.config['IPSTACK_API_KEY']
        geo_ip = requests.get('http://api.ipstack.com/' + ip + "?access_key=" + IPSTACK_KEY)
        resp = json.loads(geo_ip.text)

        return resp['region_name']


def tracert(): #TODO tracert
    pass