from app.calculations import add

def test_add():
    print("testing add function")
    assert 8 == add(5,3)
test_add()