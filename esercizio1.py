import os 
import re
import sys
from collections import defaultdict

def get_shebang(file_path):
    """Legge la prima riga del file per determinare lo shebang."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            match = re.match(r'#!\s*(\S+)', first_line)
            return match.group(1) if match else "Unknown"
    except (OSError, UnicodeDecodeError):
        return "Unknown"
    
def count_executables_by_shebang(directory):
    """Conta i file eseguibili nella directory, raggruppandoli per interprete."""
    shebang_counts = defaultdict(int)
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            if os.access(file_path, os.X_OK) and os.path.isfile(file_path):
                shebang = get_shebang(file_path)
                shebang_counts[shebang] += 1
    
    return shebang_counts

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Errore: La directory specificata non esiste.")
        sys.exit(1)
    
    counts = count_executables_by_shebang(directory)
    for shebang, count in counts.items():
        print(f"{shebang}: {count}")

if __name__ == "__main__":
    main()
