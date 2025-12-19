Завдання 2: Генератор хешів файлів



import hashlib

def generate_file_hashes(*file_paths):
    hash_results = {}
    
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                sha256_hash = hashlib.sha256(file_content).hexdigest()
                hash_results[file_path] = sha256_hash
        except FileNotFoundError:
            print(f"Помилка: Файл {file_path} не знайдено.")
        except IOError:
            print(f"Помилка: Не вдалося прочитати файл {file_path}.")
            
    return hash_results

files_to_check = ["apache_logs.txt", "missing_file.txt"]
file_hashes = generate_file_hashes(*files_to_check)
print(file_hashes)
