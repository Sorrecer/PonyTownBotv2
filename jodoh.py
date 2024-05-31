import hashlib

def calculate_love_percentage(name1, name2):
    # Gabungkan kedua nama dengan urutan yang konsisten
    combined_names = ''.join(sorted([name1.lower(), name2.lower()]))
    
    # Hashing kombinasi nama menggunakan SHA256
    hash_object = hashlib.sha256(combined_names.encode())
    hex_dig = hash_object.hexdigest()
    
    # Mengambil 2 karakter pertama dari hash dan mengubahnya menjadi integer
    hash_int = int(hex_dig[:2], 16)
    
    # Menghitung persentase kecocokan dari 0 hingga 100
    percentage = hash_int % 101
    
    return percentage

# Input dari pengguna
name1 = input("Masukkan nama pertama: ")
name2 = input("Masukkan nama kedua: ")

# Hitung persentase kecocokan
percentage = calculate_love_percentage(name1, name2)

# Output hasil
print(f"Kecocokan jodoh antara {name1} dan {name2} adalah {percentage}%")
