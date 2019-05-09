from monitor import app
import requests, re, socket, json

def ping(url, prefix="https://"):
    
    if check_valid_url(url) != 'ERROR':
        return prefix + check_valid_url(url)
    else:
        return 'https://www.inspiredprogrammer.com'


def monitor_website(url):
    try:
        r = requests.head(url, timeout=2, stream=True, allow_redirects=True)

        if r.status_code == 200:
            # return r.url | r.status_code | r.reason | server_ip | latency | server_location | isdown
            server_ip = get_server_ip(url)
            server_location = get_server_location(server_ip)
            latency = check_latency(url)
            #return 'url=%r, status_code=%r, status_reason=%r, server_ip=%r, server_latency=%r, server_loaction=%r, isdown=%r' % (r.url, r.status_code, r.reason, server_ip, latency, server_location, False)
            return r.url, r.status_code, r.reason, server_ip, latency, server_location, False
        elif r.status_code != 200:
            server_ip = get_server_ip(url)
            server_location = get_server_location(server_ip)
            latency = check_latency(url)
            #return 'url=%r, status_code=%r, status_reason=%r, server_ip=%r, server_latency=%r, server_loaction=%r, isdown=%r' % (r.url, r.status_code, r.reason, server_ip, latency, server_location, True)
            return r.url, r.status_code, r.reason, server_ip, latency, server_location, True
    except Exception as e:
        if "Timeout" in repr(e):
            server_ip = get_server_ip(url)
            server_location = get_server_location(server_ip)
            #return 'url=%r, status_code=%r, status_reason=%r, server_ip=%r, server_latency=%r, server_loaction=%r, isdown=%r' % (url, 'NONE', 'NONE', server_ip, 'NONE', server_location, True)
            return url, 'NONE', 'NONE', server_ip, 'NONE', server_location, True



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
        return requests.head(url).elapsed.total_seconds()
    except Exception as e:
        if "Timeout" in repr(e):
            return 'Timeout error'


def get_server_ip(url):
    host = check_valid_url(url)
    return socket.gethostbyname(host)


def get_server_location(ip):
        IPSTACK_KEY = app.config['IPSTACK_API_KEY']
        geo_ip = requests.get('http://api.ipstack.com/' + ip + "?access_key=" + IPSTACK_KEY)
        resp = json.loads(geo_ip.text)
        loc_obj = resp['location']
        #return resp['region_name']
        return resp['city'], loc_obj['country_flag']

def tracert(): #TODO tracert
    pass

def func(x):
    return x
