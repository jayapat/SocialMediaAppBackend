def add(num1: int, num2: 2):
    return num1 + num2

def multi(num1: int, num2: 2):
    return num1 * num2 

def div(num1: int, num2: 2):
    return num1 / num2

def min(num1: int, num2: 2):
    return num1 - num2

class Insufficentfund(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise Insufficentfund("balance is insufficient")
        self.balance -= amount

    def collect_interest(self, amount):
        self.balance *= 1.1