import pytest

@pytest.mark.smoke
def test_demo1():
    assert 1==1

@pytest.mark.regression
def test_demo2_shop():
    assert 1==3, "Not matched"


def test_demo3_shop():
    assert 3==3, "Not matched"
