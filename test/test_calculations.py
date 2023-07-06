import pytest
from app.calculations import add, multi, min, div, BankAccount, Insufficentfund
@pytest.fixture()
def zero_bankaccount():
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("x, y, z", [
    (5,3,8), (3,2,5), (5,-6,-1), (5,-5,0)
])
def test_add(x, y, z):
    assert add(x,y) == z

def test_min():
    assert min(5,3) ==2

def test_multi():
    assert multi(5,3) == 15

def test_div():
    assert div(6,3) == 2

def test_bank_set_initial_amount(zero_bankaccount):
    assert zero_bankaccount.balance == 0

def test_bank_default_amount(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance  == 60

@pytest.mark.parametrize("dipo, withd, balance", [
    (50,30,20), (100,80,20)
])
def test_bank_trasactions(zero_bankaccount, dipo, withd, balance):
    zero_bankaccount.deposit(dipo)
    zero_bankaccount.withdraw(withd)
    assert zero_bankaccount.balance == balance

@pytest.mark.parametrize("dipo, withd, balance", [
    (50,200,20)
])
def test_bank_trasactions_expection(zero_bankaccount, dipo, withd, balance):
    with pytest.raises(Insufficentfund):
        zero_bankaccount.deposit(dipo)
        zero_bankaccount.withdraw(withd)
        assert zero_bankaccount.balance == balance