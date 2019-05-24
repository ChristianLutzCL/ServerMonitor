import pytest
from monitor.monitoring import func, monitor_website, check_latency


def test_answer():
    assert func(5) == 5

def test_check_latency():
    url = 'https://monitor.inspiredprogrammer.com'
    assert check_latency(url) != 'Timeout error'

def test_monitor_website():
    url = "https://monitor.inspiredprogrammer.com"
    assert monitor_website(url) == None
