class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Покласти гроші на рахунок"""
        if amount <= 0:
            raise ValueError("Сума поповнення має бути більше нуля")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Зняти гроші з рахунку"""
        if amount <= 0:
            raise ValueError("Сума зняття має бути більше нуля")
        if amount > self.balance:
            raise ValueError("Недостатньо коштів")
        self.balance -= amount
        return self.balance

    def add_interest(self, rate):
        """Нарахувати відсотки (rate у відсотках, наприклад, 10 для 10%)"""
        if rate < 0:
            raise ValueError("Відсоткова ставка не може бути від'ємною")
        interest = self.balance * (rate / 100)
        self.balance += interest
        return self.balance

    def get_balance(self):
        """Отримати поточний баланс"""
        return self.balance
