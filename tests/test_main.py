import pytest
from monitor.monitoring import func
def test_answer():
    assert func(3) == 5
