import pytest
from bank_account import BankAccount

def test_initial_balance_default():
    acc = BankAccount("Alex")
    assert acc.balance == 0
    assert acc.owner == "Alex"

def test_initial_balance_custom():
    acc = BankAccount("Alex", 100)
    assert acc.balance == 100

def test_deposit_valid():
    acc = BankAccount("Alex", 100)
    new_balance = acc.deposit(50)
    assert new_balance == 150
    assert acc.balance == 150

def test_deposit_negative_amount():
    acc = BankAccount("Alex", 100)
    with pytest.raises(ValueError):
        acc.deposit(-50)

def test_withdraw_valid():
    acc = BankAccount("Alex", 100)
    new_balance = acc.withdraw(40)
    assert new_balance == 60

def test_withdraw_insufficient_funds():
    acc = BankAccount("Alex", 50)
    with pytest.raises(ValueError):
        acc.withdraw(100)

def test_withdraw_negative_amount():
    acc = BankAccount("Alex", 100)
    with pytest.raises(ValueError):
        acc.withdraw(-10)

def test_add_interest_valid():
    acc = BankAccount("Alex", 100)
    acc.add_interest(10) # 10%
    assert acc.balance == 110

def test_add_interest_negative_rate():
    acc = BankAccount("Alex", 100)
    with pytest.raises(ValueError):
        acc.add_interest(-5)
