Завдання
Інвентаризація продуктів. Створіть словник, де ключі - це назви продуктів, а значення - їх кількість на складі. Напишіть функцію, яка приймає назву продукту та кількість, і оновлює словник відповідно до додавання або видалення продуктів. Додатково: створіть список продуктів, в яких кількість менше ніж 5.


products = {
    "хліб": 10,
    "молоко": 3,
    "масло": 15,
    "яблука": 4
}

def update_stock(name, amount):
    products[name] = products.get(name, 0) + amount

update_stock("молоко", 5)
update_stock("хліб", -7)
update_stock("цукор", 2)

low_stock_list = []

for item in products:
    if products[item] < 5:
        low_stock_list.append(item)

print(products)
print(low_stock_list)
