Завдання
Статистика продажів. Створіть список словників, де кожен словник представляє продаж з ключами: "продукт", "кількість", "ціна". Напишіть функцію, яка обчислює загальний дохід для кожного продукту та повертає словник, де ключі - це назви продуктів, а значення - загальний дохід. Створіть список продуктів, що принесли дохід більший ніж 1000.


sales_data = [
    {"продукт": "Телефон", "кількість": 2, "ціна": 400},
    {"продукт": "Ноутбук", "кількість": 1, "ціна": 1200},
    {"продукт": "Телефон", "кількість": 1, "ціна": 400},
    {"продукт": "Мишка", "кількість": 10, "ціна": 50},
    {"продукт": "Клавіатура", "кількість": 5, "ціна": 100}
]

def calculate_revenue(sales):
    revenue = {}
    
    for sale in sales:
        item = sale["продукт"]
        total = sale["кількість"] * sale["ціна"]
        revenue[item] = revenue.get(item, 0) + total
            
    return revenue

total_revenue = calculate_revenue(sales_data)
high_revenue_products = []

for product in total_revenue:
    if total_revenue[product] > 1000:
        high_revenue_products.append(product)

print(total_revenue)
print(high_revenue_products)
