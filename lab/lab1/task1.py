Завдання 1
Робота з текстом. Напишіть функцію, яка приймає рядок як вхідні дані та повертає словник, де ключі - це унікальні слова в рядку, а значення - кількість їх появ.Створіть та виведіть на екран список, де зберігаються слова, що зустрічаються більше 3 разів. 


def count_words(text):
    text = text.lower()
    
    for char in ".,!?-":
        text = text.replace(char, "")
        
    words = text.split()
    counts = {}
    
    for word in words:
        counts[word] = counts.get(word, 0) + 1
            
    return counts

input_text = """
Python - це чудова мова. Python дозволяє писати код швидко. 
Код на Python легко читати. Цей код працює. Код, код, код.
"""

result_dict = count_words(input_text)
frequent_words = []

for word in result_dict:
    if result_dict[word] > 3:
        frequent_words.append(word)

print(result_dict)
print(frequent_words)
