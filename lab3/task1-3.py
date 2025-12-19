import sqlite3
import hashlib

DB_NAME = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            login TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(login, password, full_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_pw = hash_password(password)
    
    try:
        cursor.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)", 
                       (login, hashed_pw, full_name))
        conn.commit()
        print(f"Користувача {login} успішно додано!")
    except sqlite3.IntegrityError:
        print(f"Помилка: Користувач з логіном '{login}' вже існує.")
    finally:
        conn.close()

def update_password(login, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_pw = hash_password(new_password)
    
    cursor.execute("UPDATE users SET password = ? WHERE login = ?", (hashed_pw, login))
    
    if cursor.rowcount > 0:
        conn.commit()
        print(f"Пароль для {login} успішно оновлено.")
    else:
        print(f"Користувача {login} не знайдено.")
    
    conn.close()

def authenticate_user():
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        if user['password'] == hash_password(password):
            print(">>> Автентифікація успішна! Ласкаво просимо.")
            return True
        else:
            print(">>> Помилка: Невірний пароль.")
            return False
    else:
        print(">>> Помилка: Користувача з таким логіном не існує.")
        return False

if __name__ == "__main__":
    create_table()
    
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Додати користувача")
        print("2. Оновити пароль")
        print("3. Увійти (Автентифікація)")
        print("4. Вихід")
        
        choice = input("Оберіть дію (1-4): ")
        
        if choice == '1':
            l = input("Введіть новий логін: ")
            p = input("Введіть пароль: ")
            n = input("Введіть ПІБ: ")
            add_user(l, p, n)
        elif choice == '2':
            l = input("Введіть логін користувача: ")
            p = input("Введіть новий пароль: ")
            update_password(l, p)
        elif choice == '3':
            authenticate_user()
        elif choice == '4':
            print("Роботу завершено.")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")
