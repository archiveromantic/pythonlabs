import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

dates = []
rates = []

print("Отримую дані для побудови графіка...")

for i in range(7):
    d = datetime.now() - timedelta(days=7 - i)
    date_str_api = d.strftime("%Y%m%d")
    date_str_plot = d.strftime("%d.%m")

    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={date_str_api}&json"
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            rate = data[0]['rate']
            
            dates.append(date_str_plot)
            rates.append(rate)
    except Exception as e:
        print(f"Помилка отримання даних: {e}")

plt.figure(figsize=(10, 5))

plt.plot(dates, rates, 
         color='green',
         linestyle='-',
         marker='o',
         linewidth=2,
         label='Курс НБУ (USD)')

plt.title('Графік зміни курсу долара за останній тиждень', fontsize=14)
plt.xlabel('Дата', fontsize=12)
plt.ylabel('Курс (UAH)', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.6)

plt.legend()

plt.show()
