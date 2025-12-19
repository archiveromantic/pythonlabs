Завдання 1: Аналізатор лог-файлів



def analyze_log_file(log_file_path):
    stats = {}
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.split('"')
                if len(parts) > 2:
                    status_part = parts[2].strip().split()
                    if status_part:
                        status_code = status_part[0]
                        if status_code in stats:
                            stats[status_code] += 1
                        else:
                            stats[status_code] = 1
    except FileNotFoundError:
        print(f"Error: The file {log_file_path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading {log_file_path}.")
    
    return stats

file_path = "apache_logs.txt"
log_stats = analyze_log_file(file_path)
print(log_stats)
