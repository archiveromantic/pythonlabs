Завдання 3: Фільтрація IP-адрес з файлу



def filter_ips(input_file_path, output_file_path, allowed_ips):
    found_ips = {}
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.split()
                if parts:
                    ip_address = parts[0]
                    if ip_address in allowed_ips:
                        if ip_address in found_ips:
                            found_ips[ip_address] += 1
                        else:
                            found_ips[ip_address] = 1
                            
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
        return
    except IOError:
        print(f"Error: An error occurred while reading {input_file_path}.")
        return

    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            for ip, count in found_ips.items():
                file.write(f"{ip} - {count}\n")
        print(f"Results successfully written to {output_file_path}")
        
    except IOError:
        print(f"Error: Could not write to file {output_file_path}.")

input_file = "apache_logs.txt"
output_file = "filtered_ips.txt"

allowed_ips_list = [
    "109.74.151.149",
    "107.170.40.204",
    "100.43.83.137",
    "23.21.22.111" 
]

filter_ips(input_file, output_file, allowed_ips_list)

try:
    print("\nContent of the output file:")
    with open(output_file, 'r') as f:
        print(f.read())
except FileNotFoundError:
    print("Output file not created.")
