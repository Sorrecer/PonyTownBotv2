from PIL import Image
from datetime import datetime
from characterai import aiocai
import asyncio
import time, random, re, pyautogui, pytesseract, os, requests, subprocess, rpg, sys, hashlib
import pathlib
import textwrap
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import jsonpickle

###======= Bot Configuration =======###

BotName = "Rick's Bot"
Admin_name = ['I AM RICK']
apikey="AIzaSyDIdODxrZYkAnzKAic1eR3NVSG69WVSRKA"
prefix = ['+', '>', '-']
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

with open(f'conversation.txt', 'r') as file:
    h = file.read()
    if h == '':
        chat_history = []
    else:
        chat_history = jsonpickle.decode(h)
###======= Gemini Configuration =======###

prompt = ("Anda akan memulai percakapan dengan beberapa orang player di game pony town."
          "Format pesan yang dikirim oleh saya adalah: [nama] (yang orang tersebut bicarakan). "
           "respon dengan sesingkat mungkin, maksimal 1 kalimat dengan 72 karakter)"
           "gunakan aksen indonesia gaul, santai, humoris dan ramah."
           "anda dilarang mengetik /leave dan /unstuck. karena jika mengetik itu akan menghentikan program"
           "nama orang pembuatmu adalah yang bernama 'Bepsii'"
           "bepsii adalah pony putih yang terinspirasi dari pepsi. Punya sifat jahil, suka debat, dan kepo")
# prompt = "awali segala pesan dengan 'oke bepsi!'"
genai.configure(api_key=apikey)
model = genai.GenerativeModel('gemini-1.5-flash',
                              system_instruction=prompt,
                              safety_settings={
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
})
chat = model.start_chat(history = chat_history)
###======= Setup =======##


def bard(username, message):    
    respond = chat.send_message(f'[{username}] {message}')

    
    send_ceks_in_parts(respond.text.strip())
    # print(chat.history)

# try:
#     import pytesseract
# except ModuleNotFoundError:
#     os. system("pip install pytesseract")

# try:
#     import PIL
# except ModuleNotFoundError:
#     os. system("pip install pillow")

# try:
#     import pyautogui
# except ModuleNotFoundError:
#     os. system("pip install pyautogui")
###======= Setup =======###

def send_ceks_in_parts(ceks):
    max_length = 70
    # Ganti enter dengan spasi dan hapus spasi ekstra di awal/akhir teks
    # ceks = ceks.replace('\n\n\n', ' ').strip()
    # ceks = ceks.replace('\n\n', ' ').strip()
    ceks = ceks.replace('\n', ' ').strip()
    words = ceks.split()
    print(ceks)
    print(words)
    current_part = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_length:  # +1 untuk spasi yang akan ditambahkan
            current_part.append(word)
            current_length += len(word) + 1
        else:
            kirim_pesan(' '.join(current_part))
            time.sleep(3)
            current_part = [word]
            current_length = len(word) + 1
    
    # Kirim bagian terakhir jika ada kata yang tersisa
    if current_part:
        kirim_pesan(' '.join(current_part))
    time.sleep(1)


async def cai(username, char_id='yXxZ_Z_ZEjzsBaZgqfUrPToL8NzpeN-NqDTRTTEilTM'):
    bye = False
    client = aiocai.Client('335b4d5c1c3fa11ae78060646e343d8a91c434a6')

    me = await client.get_me()

    # Load the chat ID from a text file if it exists
    chat_id = load_chat_id(char_id)


    async with await client.connect() as chat:
        if chat_id:
            # Reuse the existing chat session
            # chat_session = await chat.get_chat(char_id, chat_id)
            pass
        else:
            # Create a new chat session if no chat ID is available
            chat_session, answer = await chat.new_chat(char_id, me.id)
            # Save the new chat ID for future use
            chat_id = chat_session.chat_id
            save_chat_id(char_id, chat_id)
            send_ceks_in_parts(f'"{answer.text}"')

        while not bye:
            screen = pyautogui.screenshot()
            screen = screen.crop((110, 500, 1100, 800))
            text_cmd = pytesseract.image_to_string(screen)
            # Stop chatting
            if "bye bepis" in text_cmd.lower():
                bye = True
            else:
                # Define the regex pattern
                pattern = re.compile(rf'\[{re.escape(username)}\] (.+)')
                
                # Search for the pattern in the captured text
                match = pattern.search(text_cmd)
                
                if match:
                    text = match.group(1)  # Extract the first captured group
                    
                    # Sending message to Character AI
                    message = await chat.send_message(
                        char_id, chat_id, text
                    )
                    send_ceks_in_parts(f'"{message.text}"')

    return chat_id  # Return the chat ID for future use

def load_chat_id(char_id):
    try:
        with open(f'{char_id}_chat_id.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_chat_id(char_id, chat_id):
    with open(f'{char_id}_chat_id.txt', 'w') as file:
        file.write(chat_id)

# Example usage
# last_chat_id = await cai(username='example_user')
# To continue the chat later
# await cai(username='example_user')


def steal(name1, name2):
    items = [
        "Kaos Kaki Kiri",
        "Password Wi-Fi",
        "Lampu Kulkas",
        "Camilan",
        "Harga Diri",
        "Remote TV",
        "Seprai",
        "Potongan Pizza Terakhir",
        "Bantal",
        "Pulpen",
        "Charger",
        "Kunci Rumah",
        "Gulungan Tisu Toilet",
        "Sisa Shampoo Terakhir",
        "Kesabaran",
        "Buku Harian Pribadi",
        "Mobil",
        "Motor",
        "Kacamata Hitam",
        "Sikat Gigi",
        "Resep Rahasia",
        "Jam Alarm",
        "Hoodie Favorit",
        "Ingatan",
        "Selera Humor",
        "Kata Sandi",
        "Buku Favorit",
        "Tanaman",
        "Makanan",
        "Kaos Kaki",
        "Sepatu",
        "Pakaian",
        "Beha",
        "Kolor",
        "Bulu Misterius",
        "Mainan aneh",
        "Playlist Favorit",
        "Router Wi-Fi",
        "Identitas",
        "Surat Cinta",
        "Waktu Tidur Siang",
        "Nasi Padang",
        "Sempak",
        "Duit 10rb",
        "Duit 100rb",
        "Duit 1M",
        "Duit 271T",
        "KTP",
        "SIM C",
        "Handuk",
        "Hati",
        "Kantong kresek",
        "Ginjal",
        "Perhatian",
        "Pacar",
        "BOM",
        "Beras",
        "Pepsi",
        "Tolak angin",
        "minyak kayu putih",
        "Pahala",
        "Duit 2rb",
        "Kuda",
        "Kucing",
        "Tanda Tangan",
        "Kenangan Masa Lalu",
    ]
    item = random.choice(items)
    kirim_pesan(f"{name1} telah mencuri {item} dari {name2}!")

def suit(name1, name2, suit1, suit2):
    #condition 1
    if suit1 == suit2 :
        kirim_pesan(f'seri! kedua pemain telah memilih {suit1}')
    elif (suit1 == 'gunting' and suit2 == 'kertas') or \
        (suit1 == 'batu' and suit2 == 'gunting') or \
        (suit1 == 'kertas' and suit2 == 'batu'):
        kirim_pesan(f'{suit1} vs {suit2}. {name2} kalah! {name1} menang!')
    else:
        kirim_pesan(f'{suit1} vs {suit2}. {name1} kalah! {name2} menang!')

def add_fish(name):
        with open("fish_database.txt", "r+") as file:
            lines = file.readlines()
            
            # Menghapus header dan mengiterasi baris data
            for line in lines[1:]:
                data = line.strip().split(',')
                
                if data[0].lower() == name.lower():
                    print(f"{name.capitalize()} sudah ada dalam database.")
                    return  # Keluar dari fungsi jika nama sudah ada

            # Tambahkan data baru jika nama tidak ditemukan
            new_data = f"{name},0,0,0,0,0\n"
            file.write(new_data)
            print(f"{name.capitalize()} telah ditambahkan ke database.")

def add_duit(name):
        with open("duit_database.txt", "r+") as file:
            lines = file.readlines()
            
            # Menghapus header dan mengiterasi baris data
            for line in lines[1:]:
                data = line.strip().split(',')
                
                if data[0].lower() == name.lower():
                    print(f"{name.capitalize()} sudah ada dalam database.")
                    return  # Keluar dari fungsi jika nama sudah ada

            # Tambahkan data baru jika nama tidak ditemukan
            new_data = f"{name},0\n"
            file.write(new_data)
            print(f"{name.capitalize()} telah ditambahkan ke database.")

def checkOrkay():
    with open("duit_database.txt", "r") as file:
        lines = file.readlines()
        
    # Inisialisasi variabel untuk menyimpan informasi orang dengan uang terbanyak
    richest_person = None
    max_money = -float('inf')  # Awalnya diatur ke negatif tak hingga
    
    # Lewati header dan iterasi baris data
    for line in lines[1:]:
        data = line.strip().split(',')
        money = int(data[1])  # Konversi jumlah uang ke integer
        
        if money > max_money:
            max_money = money
            richest_person = data[0]
    
    if richest_person:
        kirim_pesan(f"Orang terkaya adalah {richest_person.capitalize()} dengan duit: {max_money}")
        return richest_person, max_money

def add_catch(name, category_index, increment=1):
    # Baca file dan cari nama
    with open("fish_database.txt", "r") as file:
        lines = file.readlines()
    
    # Tulis data baru ke file sementara
    with open("fish_database.txt", "w") as file:
        for line in lines:
            data = line.strip().split(',')
            
            # Jika nama cocok, tambahkan nilai pada kategori yang sesuai
            if data[0].lower() == name.lower():
                # Tambahkan nilai
                data[category_index] = str(int(data[category_index]) + increment)

            # Tulis kembali data (baik diperbarui atau tidak)
            file.write(','.join(data) + '\n')
        print(f"Data {name.capitalize()} telah diperbarui.")

def add_gacor(name, amount):
        # Baca file dan simpan semua baris
        with open("duit_database.txt", "r") as file:
            lines = file.readlines()
        
        # Tulis data baru ke file sementara
        with open("duit_database.txt", "w") as file:
            for line in lines:
                data = line.strip().split(',')
                
                if data[0].lower() == name.lower():
                    if amount == 0:
                        data[1] = '0'
                    else:
                        data[1] = str(int(data[1]) + amount)

                # Tulis kembali data (baik diperbarui atau tidak)
                file.write(','.join(data) + '\n')
            print(f"Duit {name.capitalize()} telah diperbarui.")

def calculate_form_percentage(name1):
    wujud = [
    "Manusia",
    "Serigala",
    "Drakula",
    "Siklop",
    "Presiden Amerika Serikat",
    "Bos Mafia",
    "Hantu",
    "Smurf",
    "Badut",
    "Vampir",
    "Ayam",
    "Alien",
    "Skeleton",
    "Unicorn",
    "Putri Duyung",
    "Kraken",
    "Goblin",
    "Politisi",
    "Yeti",
    "Hamster Raksasa",
    "Kura-Kura Ninja",
    "Bajak Laut",
    "Leprechaun",
    "Naga",
    "Gnome",
    "Penjaga Pantai",
    "Mumi",
    "Centaur",
    "Elf",
    "Mekanik",
    "Troll",
    "Cyborg",
    "Manusia Serigala",
    "Peri",
    "Jin",
    "Medusa",
    "Akuntan Pajak",
    "Robot",
    "Penyihir",
    "Phoenix",
    "Griffin",
    "Pegasus",
    "Semut Raksasa",
    "Bigfoot",
    "Sphinx",
    "Kurcaci",
    "Raksasa",
    "Dinosaurus",
    "Pohon yang Berbicara",
    "Marshmallow Hidup",
    "Kucing",
    "Koboi",
    "Kraken",
    "Mbah - mbah",
    "Vampir",
    "Ikan yang Berbicara",
    "Manusia Salju Hidup",
    "Penyihir Tak Terlihat",
    "Putri Duyung",
    "Vegan",
    "Anjing yang Berbicara",
    "Labu yang Berbicara"
    ]

    # Hashing kombinasi nama menggunakan SHA256

    hash_object = hashlib.sha256((name1.lower()).encode())
    hex_dig = hash_object.hexdigest()
    
    # Mengambil 2 karakter pertama dari hash dan mengubahnya menjadi integer
    hash_int = int(hex_dig[:2], 16)
    
    # Menghitung persentase kecocokan dari 0 hingga 100
    percentage = hash_int % 61
    kirim_pesan(f'Wujud asli dari {name1} adalah : {wujud[percentage]}')


def calculate_furry_percentage(name1):
    # Hashing kombinasi nama menggunakan SHA256

    hash_object = hashlib.sha256((name1.lower()).encode())
    hex_dig = hash_object.hexdigest()
    
    # Mengambil 2 karakter pertama dari hash dan mengubahnya menjadi integer
    hash_int = int(hex_dig[:2], 16)
    
    # Menghitung persentase kecocokan dari 0 hingga 100
    percentage = hash_int % 101
    
    return percentage

def calculate_power(name1):
    powers = [
    "Mampu mendeteksi warna cat yang mengering",
    "Mengubah rasa air menjadi rasa mentimun",
    "Menyilaukan diri sendiri dengan refleksi",
    "Dapat menggerakkan satu helai rambut",
    "Mampu berbicara dengan patung",
    "Memiliki ingatan yang sempurna untuk iklan TV",
    "Mampu menyelipkan daun ke pintu tanpa suara",
    "Mengetahui semua waktu buka restoran tutup di daerah terpencil",
    "Mampu membuat udara di dalam air mineral",
    "Mengendus jejak yang tidak terlihat",
    "Mengubah nada dering menjadi lagu",
    "Mampu mengingatkan seseorang tentang topik percakapan yang terlupakan",
    "Mengubah warna cacing tanah",
    "Dapat meramalkan pola tidur kucing tetangga",
    "Menyusun ulang kata-kata tanpa mengubah maknanya",
    "Mempercepat pembusukan buah selama 5 menit",
    "Mampu membuat bola lampu berkedip sekali",
    "Menggandakan panjang waktu dalam antrean",
    "Mendeteksi keberadaan payung dalam radius 10 meter",
    "Mampu mengubah suhu air sebanyak satu derajat Celsius setiap jam",
    "Menghilangkan satu inci ketinggian bayangan",
    "Mengetahui semua nama karakter film latar belakang",
    "Membuat jendela berembun tanpa menyentuhnya",
    "Mengatur ulang rasa kacang menjadi acak",
    "Dapat membuat aroma bunga menghilang selama 2 detik",
    "Mengubah warna lembaran daun setiap musim gugur",
    "Mengidentifikasi suara plastik yang terurai",
    "Membuat noda kopi menjadi tidak terlihat selama 1 menit",
    "Mengganti warna sinar UV menjadi RGB dalam penglihatan",
    "Mampu mendengar suara dari jarak yang sangat dekat",
    "Mengetahui berat benda tanpa menimbangnya",
    "Mengubah frekuensi suara mesin cuci",
    "Menghapus jejak sidik jari digital selama 10 detik",
    "Mengetahui jumlah kacang dalam toples besar",
    "Dapat membuat gelas air tidak berbunyi saat bersentuhan dengan meja",
    "Mengubah rasa makanan yang sudah dimakan",
    "Mengetahui arah angin dalam ruangan tertutup",
    "Mampu membuat lampu lalu lintas tetap hijau lebih lama selama 1 detik",
    "Menebak jumlah halaman kosong dalam buku",
    "Menyinkronkan putaran jam tangan dengan rotasi bumi"
    "Penyembuhan Instan",             # Menyembuhkan diri atau orang lain dari luka atau penyakit dengan cepat.
    "Telekinesis",                    # Memindahkan objek dengan pikiran.
    "Invisibility",                   # Menjadi tidak terlihat kapan saja.
    "Teleportasi",                    # Memindahkan diri ke mana saja secara instan.
    "Membaca Pikiran",                # Mengetahui apa yang orang lain pikirkan.
    "Kontrol Waktu",                  # Menghentikan, mempercepat, atau memperlambat waktu.
    "Kekuatan Super",                 # Memiliki kekuatan fisik jauh di atas rata-rata manusia.
    "Membuat Perisai Energi",         # Membuat perisai yang dapat melindungi dari serangan fisik atau energi.
    "Membuat Kembali Benda Rusak",    # Memperbaiki benda yang rusak atau hancur menjadi utuh kembali.
    "Memanipulasi Elemen Alam",       # Mengendalikan elemen seperti api, air, tanah, atau angin.
    "Membaca Masa Depan",             # Mengetahui peristiwa yang akan terjadi.
    "Super Kecepatan",                # Bergerak dengan kecepatan luar biasa.
    "Kontrol Pikiran",                # Memengaruhi atau mengendalikan pikiran orang lain.
    "Kemampuan untuk Terbang",        # Terbang di udara.
    "Memanipulasi Gravitasi",         # Mengubah gravitasi untuk diri sendiri atau objek lain.
    "Daya Ingatan Fotografi",         # Mengingat segala sesuatu dengan detail yang sempurna.
    "Berkomunikasi dengan Binatang",  # Mengerti dan berbicara dengan hewan.
    "Menghentikan Penuaan",           # Menghentikan proses penuaan.
    "Mengendalikan Teknologi",        # Mengendalikan perangkat elektronik dan digital.
    "Berubah Bentuk",                 # Mengubah penampilan atau bentuk fisik menjadi orang lain atau objek.
    "Bernafas di Bawah Air",          # Bernapas tanpa kesulitan di dalam air.
    "Pemahaman Instan Semua Bahasa",  # Memahami dan berbicara semua bahasa.
    "Regenerasi Energi",              # Mengisi ulang energi atau stamina dengan cepat.
    "Penciptaan Ilusi",               # Membuat ilusi yang dapat dilihat dan dirasakan oleh orang lain.
    "Kemampuan Analisis Tinggi",      # Menganalisis situasi dengan cepat dan akurat.
    "Mengendalikan Tanaman",          # Mempercepat pertumbuhan atau memanipulasi tanaman.
    "Adaptasi Lingkungan",            # Menyesuaikan diri dengan kondisi lingkungan ekstrem.
    "Kemampuan Pemecahan Masalah",    # Menyelesaikan masalah kompleks dengan cepat.
    "Kekuatan Magnetik",              # Mengendalikan medan magnet dan logam.
    "Meningkatkan Kreativitas",       # Memunculkan ide-ide kreatif dengan cepat.
    "Kekuatan Penyembuhan Alami",     # Menyembuhkan luka atau penyakit dengan bahan-bahan alami.
    "Berkomunikasi Telepati",         # Berkomunikasi dengan orang lain tanpa suara.
    "Kontrol Suhu Tubuh",             # Mengatur suhu tubuh agar tetap nyaman dalam kondisi ekstrem.
    "Perjalanan Dimensi",             # Bepergian antara dimensi atau realitas yang berbeda.
    "Kekuatan Suara",                 # Menggunakan suara untuk menciptakan getaran atau gelombang energi.
    "Penglihatan Menembus Benda",     # Melihat melalui objek padat.
    "Menghilangkan Rasa Takut",       # Mengatasi atau menghilangkan rasa takut.
    "Mengendalikan Pikiran Sendiri",  # Mengatur emosi dan pikiran sendiri dengan sempurna.
    "Mengubah Suhu Lingkungan",       # Menurunkan atau menaikkan suhu di sekitar.
    "Penyimpanan di Dimensi Lain",    # Menyimpan objek di dimensi alternatif untuk menghemat ruang."
]
    # Hashing kombinasi nama menggunakan SHA256

    hash_object = hashlib.sha256((name1.lower()).encode())
    hex_dig = hash_object.hexdigest()
    
    # Mengambil 2 karakter pertama dari hash dan mengubahnya menjadi integer
    hash_int = int(hex_dig[:2], 16)
    
    # Menghitung persentase kecocokan dari 0 hingga 100
    percentage = hash_int % 79
    kirim_pesan(f'Kekuatan super dari {name1} adalah.....')
    time.sleep(2)
    kirim_pesan(f'{powers[percentage]}')

def calculate_gey_percentage(name1):
    # Hashing kombinasi nama menggunakan SHA256

    hash_object = hashlib.sha256((name1.lower()).encode())
    hex_dig = hash_object.hexdigest()
    
    # Mengambil 2 karakter pertama dari hash dan mengubahnya menjadi integer
    hash_int = int(hex_dig[:2], 16)
    
    # Menghitung persentase kecocokan dari 0 hingga 100
    percentage = hash_int % 101
    
    return percentage

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


def press_arrow_key(direction):
    pyautogui.keyDown(direction)
    time.sleep(0.1)
    pyautogui.keyUp(direction)

def handle_command(text_cmd, command, direction, kmna):
    match = re.search(r'\[(.*?)\](?: whispers:)? >*?' + command + r'\s+(\d+)', text_cmd)
    if match:
        username = match.group(1)
        if username in Admin_name:
            value = int(match.group(2))
            
            kirim_pesan(f"{value} langkah ke {kmna}")
            for _ in range(value):
                press_arrow_key(direction)
            kirim_pesan("")
        else:
            kirim_pesan("SIAPA LU NYURUH NYURUH??")

def split_text(text, max_length=70):
    words = text.split()
    lines = []
    current_line = ''

    for word in words:
        if len(current_line) + len(word) <= max_length:
            current_line += word + ' '
        else:
            lines.append(current_line.rstrip())
            current_line = word + ' '

    if current_line:
        lines.append(current_line.rstrip())

    return lines

import requests

import requests

def gemini(meseg):
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': apikey
    }

     # Correct safety settings with valid categories
    safety_settings = [
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": 0},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": 0},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": 0},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": 0}
    ]

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": meseg + ". (jawab dengan singkat 1-2 kalimat, kurang dari 72 karakter)"
                    }
                ]
            }
        ],
        "safetySettings": safety_settings
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        response_data = response.json()
        candidates = response_data.get("candidates", [])
        if candidates:
            content_parts = candidates[0].get("content", {}).get("parts", [])
            text_parts = [part["text"] for part in content_parts if "text" in part]
            response_text = " ".join(text_parts)
            return response_text
        else:
            print("No candidates found.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# Definisikan fungsi check
def checkfish(name):
    # Membaca file fish_database.txt
    with open("fish_database.txt", "r") as file:
        lines = file.readlines()
        
        # Menghapus header dan mengiterasi baris data
        for line in lines[1:]:
            data = line.strip().split(',')
            
            if data[0].lower() == name.lower():
                # Mencetak hasil dalam format yang diinginkan
                kirim_pesan(f"{name.capitalize()} :comet:M:{data[1]} :sparkles:L:{data[2]} :dolphin:U:{data[3]} :fish:C:{data[4]} :sob:T:{data[5]}")
                return  # Keluar dari fungsi setelah menemukan data yang sesuai
        
        # Jika tidak ditemukan
        kirim_pesan(f"{name.capitalize()} tidak ditemukan dalam database.")

def checkduit(name):
    # Membaca file fish_database.txt
    with open("duit_database.txt", "r") as file:
        lines = file.readlines()
        
        # Menghapus header dan mengiterasi baris data
        for line in lines[1:]:
            data = line.strip().split(',')
            
            if data[0].lower() == name.lower():
                # Mencetak hasil dalam format yang diinginkan
                kirim_pesan(f"Duit {name.capitalize()} berjumlah ${data[1]}")
                return  # Keluar dari fungsi setelah menemukan data yang sesuai
        
        # Jika tidak ditemukan
        kirim_pesan(f"{name.capitalize()} tidak ditemukan dalam database.")
            
def command(cmd, run):
    pattern = r'\[(.*?)\](?: whispers:)? ([' + ''.join(re.escape(p) for p in prefix) + '])' + re.escape(cmd) + r'(?: (.+))?'
    if re.search(pattern, text_cmd.lower()):
        match = re.search(pattern, text_cmd)
        if match:
            run(match)
    elif ">up" in text_cmd.lower():
        handle_command(text_cmd, ".up", 'up', "atas")
    elif ">down" in text_cmd.lower():
        handle_command(text_cmd, ".dn", 'down', "bawah")
    elif ">right" in text_cmd.lower():
        handle_command(text_cmd, ".kn", 'right', "kanan")
    elif ">left" in text_cmd.lower():
        handle_command(text_cmd, ".kr", 'left', "kiri")
    elif '.sm' in text_cmd:
        match = re.search(r'\[(.*?)\](?: whispers:)? .sm \"(.*?)\" (.+)', text_cmd)
        if match:
            nama = match.group(1)
            username = match.group(2)
            messeg = match.group(3)
            if username == nama:
                kirim_whisp(message="Tidak bisa send secret message ke diri sendiri", username=nama)
            else:
                kirim_whisp(message=f"Halo {username}, anda mendapatkan pesan rahasia", username=username)
                time.sleep(2)
                kirim_whisp(message=messeg, username=username)
                kirim_whisp(message="Secret Message Terkirim", username=nama)
                
def kirim_pesan(message):
    pyautogui.typewrite('/')
    pyautogui.press('backspace')
    pyautogui.typewrite("/say "+message)
    pyautogui.press('enter')
    pyautogui.typewrite('/clearchat')
    pyautogui.press('enter')

def kirim_whisp(message, username):
    pyautogui.typewrite('/')
    pyautogui.press('backspace')
    pyautogui.typewrite(f"/whisper {username} "+message)
    pyautogui.press('enter')
    pyautogui.typewrite('/clearchat')
    pyautogui.press('enter')

def hit_card():
    return random.randint(1, 10)

class Cmd:
    def menu(self, match):
        username = match.group(1)
        current_time = time.localtime()
        current_hour = str(current_time.tm_hour) 
        current_minute = str(current_time.tm_min)
        def adminmenu():
            kirim_pesan("> ai <text>")
            kirim_pesan("> back")
            kirim_pesan("> day")
            kirim_pesan("> dice <angka>")
            kirim_pesan("> kiss")
            kirim_pesan("> lambai")
            kirim_pesan("> laugh")
            kirim_pesan("> lie")
            kirim_pesan("> menu")
            kirim_pesan("> nama_keren")
            kirim_pesan("> owner")
            kirim_pesan("> puja")
            kirim_pesan("> py <python code>")
            kirim_pesan("> quotes")
            kirim_pesan("> sit")
            kirim_pesan("> sleep")
            kirim_pesan("> stand")
            kirim_pesan("> sm(Secret Message) <username> <pesan>")
            kirim_pesan("> up (jumlah langkah) <atas>")
            kirim_pesan("> dn (jumlah langkah) <bawah>")
            kirim_pesan("> kr (jumlah langkah) <kiri>")
            kirim_pesan("> kn (jumlah langkah) <kanan>")

        def menu():
            pesan_salam = f"Hi [{username}!]"
            kirim_pesan(pesan_salam)
            kirim_pesan("command : >games >fun >others")

        if username in Admin_name: 
            pesan_salam = f"Hallo Tuan [{username}], Sekarang Jam: {current_hour}:{current_minute}"
            kirim_pesan(pesan_salam)
            kirim_pesan(f"Apa yang tuan {username} inginkan?")
            time.sleep(4)
            kirim_pesan("Menu yang saya bisa:")
            time.sleep(2)
            adminmenu()
        
        else:
            menu()

    def bardai(self, match):
        username = match.group(1)
        message = match.group(3)
        bard(username, message)
    
    def save(self, match):
        chat_history = jsonpickle.encode(chat.history, True)
        with open('conversation.txt', 'w') as file:
            file.writelines(chat_history)



    def talkai(self, match):
        username = match.group(1)
        asyncio.run(cai(username))
    
    def games(self, match):
        kirim_pesan(">fish, >cointoss, >slots, >blackjack, >roulette")

    def fun(self, match):
        kirim_pesan(">steal [name], >furry [name], >love [name1] [name2], >form[name]")
        time.sleep(2)
        kirim_pesan(">gay [name], >power [name]")

    def others(self, match):
        kirim_pesan(">ask, >news, >talk, >about")
        
    def cointoss(self, match):
        coin = ["head","tail"]
        kirim_pesan("Melempar koin..")
        time.sleep(2)
        kirim_pesan("Sisi atas koin = ")
        kirim_pesan(random.choice(coin))

    def slots(self, match):
        username = match.group(1)
        add_duit(username)
        slot = [":banana:", ":heart:", ":skull:"]
        slot1 = random.choice(slot)
        slot2 = random.choice(slot)
        slot3 = random.choice(slot)
        kirim_pesan(f"[{slot1}] [{slot2}] [{slot3}]")
        time.sleep(1)
        if slot1 == slot2 == slot3:
            kirim_pesan(":sparkles: GACOR KANGGGG! duit +1000 :sparkles:")
            add_gacor(username, 1000)
        elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
            kirim_pesan("lumayan gacor. duit +100")
            add_gacor(username, 100)
        else :
            kirim_pesan("anda bangkrut :sob:")
            add_gacor(username, 0)

    def guntingbatukertas(self, match):
        over = False
        name1 = match.group(1)
        suit1 = match.group(2)
        kirim_pesan(f'{name1} menantang anda pada gunting batu kertas')
        while not over:
            screen = pyautogui.screenshot()
            screen = screen.crop((110, 500, 1100, 800))
            text_cmd = pytesseract.image_to_string(screen)
            if ">suit" in text_cmd.lower():
                name2 = match.group(1)
                suit2 = match.group(2)
                suit(name1, name2, suit1, suit2)
                over = True
    
    def blackjack(self, match):
        username = match.group(1)
        loss = False
        
        # Mulai dengan kartu pertama untuk pemain
        player_total = hit_card()
        dealer_total = hit_card()
        kirim_pesan(f"Your card: {player_total}")
        time.sleep(1)
        kirim_pesan(">hit or >stand ?")
        
        # Giliran pemain
        while loss == False :
            screen = pyautogui.screenshot()
            screen = screen.crop((110, 500, 1100, 800))
            text_cmd = pytesseract.image_to_string(screen)
            if "hit" in text_cmd.lower():
                new_card = hit_card()
                player_total += new_card
                kirim_pesan(f"New card: {new_card}, Total: {player_total}")
                time.sleep(1)

                if player_total == 21:
                    kirim_pesan("blackjack 21. duit +500")
                    add_gacor(username, 500)
                    loss = True
                    break
                
                if player_total > 21:
                    kirim_pesan("You Lose! Busted! Anda bangkrut")
                    add_gacor(username, 0)
                    loss = True
                    break

            elif "stand" in text_cmd.lower():
                kirim_pesan(f"You stand with: {player_total}")
                break
            else :
                print("else")
                print("tes123")
        
        # Giliran dealer

        while loss == False :
            kirim_pesan(f"Dealer card: {dealer_total}")
            time.sleep(1)
            
            while dealer_total < 17:
                new_card = hit_card()
                dealer_total += new_card
                kirim_pesan(f"Dealer's new card: {new_card}, Dealer's total: {dealer_total}")
                time.sleep(1)
            
            if dealer_total > 21:
                kirim_pesan("Dealer busted!")
                break
            elif dealer_total >17 and dealer_total <= player_total :
                new_card = hit_card()
                dealer_total += new_card
                kirim_pesan(f"Dealer's new card: {new_card}, Dealer's total: {dealer_total}")
                time.sleep(1)
            else :
                kirim_pesan(f"Dealer stand with: {dealer_total}")
                time.sleep(1)
                break
            
        # Menentukan pemenang
        if loss == False :
            if player_total > dealer_total or dealer_total > 21:
                kirim_pesan("YOU WON! duit +500")
                add_gacor(username, 500)
            elif player_total < dealer_total:
                kirim_pesan("Dealer won! ANDA BANGKRUT")
                add_gacor(username, 0)
            else:
                kirim_pesan("It's a tie!")

    def roulette(self, match):
        mati = False
        i = 0
        kirim_pesan("Mengisi peluru & memutar chamber")
        chambers = [False, False, False, False, False, False]
        
        # Load a bullet into a random chamber
        bullet_position = random.randint(0, 5)
        chambers[bullet_position] = True
        
        # Spin the cylinder (shuffling the chambers)
        random.shuffle(chambers)
        
        # Player pulls the trigger
        kirim_pesan("tarik pelatuk? (tarik/tidak)")
        while mati == False :
            screen = pyautogui.screenshot()
            screen = screen.crop((110, 500, 1100, 800))
            text_cmd = pytesseract.image_to_string(screen)
            if ">tarik" in text_cmd.lower():
                if chambers[i]:
                    kirim_pesan("DORR!! mati.")
                    mati = True
                else:
                    kirim_pesan("klik, selamat anda idup.")
                    i += 1
            elif ">tidak" in text_cmd.lower():
                kirim_pesan("huuu penakut.")

    def furry(self, match):
        match = re.search(r'>furry \[([^\]]+)\]', text_cmd)
        if match:
            username = match.group(1)
            if (username == "Osi") or (username == "osi"):
                percentage = 999999
            else:
                percentage = calculate_furry_percentage(username)
            kirim_pesan(f"Tingkat furry {username} adalah {percentage}%")
            if percentage < 30:
                kirim_pesan(f"Selamat! Anda normal!")
            elif 30 <= percentage < 60:
                kirim_pesan(f"Bau furry dikit :ok_hand:")
            elif 60 <= percentage < 90:
                kirim_pesan(f"Raaawwwwwrrr :wolf_face:")
            elif 90 <= percentage <=100:
                kirim_pesan(f":wolf_face: SOLID!! SOLID!! SOLID!! :wolf_face:")
            else :
                kirim_pesan(f":wolf_face: SEMBAH RAJA FURRY :wolf_face:")

    def gay(self, match):
        match = re.search(r'>gay \[([^\]]+)\]', text_cmd)
        if match:
            username = match.group(1)
            percentage = calculate_gey_percentage(username)
            if percentage < 20:
                kirim_pesan(f"{username} is GAY")
            else :
                kirim_pesan(f"{username} is NOT GAY")

    def powers(self, match):
        match = re.search(r'>power \[([^\]]+)\]', text_cmd)
        if match:
            username = match.group(1)
            percentage = calculate_power(username)
            
    def love(self,match):
        matches = re.findall(r'>love \[([^\]]+)\] \[([^\]]+)\]', text_cmd)
        for match in matches:
            name1 = match[0]
            name2 = match[1]
            percentage = calculate_love_percentage(name1, name2)
            kirim_pesan(f"Kecocokan jodoh antara {name1} dan {name2} adalah {percentage}%")
    
    def steal(self,match):
        matches = re.findall(r'\[([^\]]+)\] >steal \[([^\]]+)\]', text_cmd)
        for match in matches:
            name1 = match[0]
            name2 = match[1]
            steal(name1, name2)

    def fish(self, match):

        bait = True
        wait = 0

        match = re.search(r'\[([^\]]+)\] >fish', text_cmd)
        if match:
            username = match.group(1)
        gacha = random.randint(1, 100)
        kirim_pesan(f'{username} melempar umpan pancing..')

        # menambahkan nama pada database jika belum ada
        add_fish(username)
            

        # list ikan
        mythical = ["MEGALODON", "LEVIATHAN", "KRAKEN", "NESSIE (LOCH NESS MONSTER)", 
                    "JÖRMUNGANDR (MIDGARD SERPENT)", "ASPIDOCHELONE (ISLAND WHALE)", "TYRANNOSAURUS REX"
                    "BASILOSAURUS", "HYDRA", "WYRM", "GIANT SEA SERPENT", "DRAGON TURTLE"]


        legend = [
                    "Paus Biru", "Hiu Putih Besar", "Cumi-cumi Raksasa", "Marlin Hitam", 
                    "Kerapu Goliath", "Tuna Sirip Biru Atlantik", "Sturgeon Beluga", "Nila Nil", 
                    "Lele Raksasa Mekong", "Ikan Pedang", "Hiu Macan", "Hiu Paus", "Hiu Greenland", 
                    "Tarpon Atlantik", "Ikan Layar", "Dorado Emas", "Arapaima", "Sturgeon Putih", 
                    "Tuna Sirip Kuning", "Halibut Atlantik", "Lele Wels", "Barramundi", 
                    "Trevally Raksasa", "Tarpon", "Salmon Raja", "Trout Kepala Baja", 
                    "Marlin Biru", "Pari Air Tawar Raksasa", "Kerapu Goliath Atlantik", 
                    "Tuna Mata Besar", "Hiu Macan Tutul", "Hiu Mako Sirip Pendek", 
                    "Halibut Pasifik", "Pirarucu", "Ikan Ratu", "Ikan Jengger Ayam", 
                    "Ikan Kakap Merah (Redfish)", "Amberjack", "Opah (Ikan Bulan)", 
                    "Ikan Kakap Hitam", "Mahi-Mahi (Dorado)", "Kerapu Suram", "Bocaccio", 
                    "Tilefish Garis Biru", "Amberjack Ekor Kuning", "Barracuda Mulut Kuning", 
                    "Ikan Pemicu Abu-abu"
                ]


        uncommon = [
                "Opah (Ikan Bulan)", "Ikan Dayung", "Bintang Laut (Ikan Penjelajah)", "Ikan Serigala Atlantik", 
                "Ikan Teri Pasifik", "Hiu Greenland", "Coelacanth", "Ikan Vampir (Payara)", 
                "Trevally Raksasa", "Ikan Tangan Berbintik", "Ikan Gergaji", "Ikan Blob", 
                "Wobbegong", "Ikan Tripletail", "Ikan Pomfret", "Ikan Saber", "Ikan Serigala Herring", 
                "Ikan Batu", "Dorado Emas", "Arapaima", "Alligator Gar", "Arowana", 
                "Lamprey", "Hagfish", "Sturgeon", "Belut Listrik", "Ikan Paddle", 
                "Ikan Paru-paru Australia", "Ikan Harimau Afrika", "Mola Mola (Ikan Matahari Laut)", 
                "Barreleye", "Pomfret Atlantik", "Drum Air Tawar", "Ikan Kepala Ular", 
                "Ikan Kalkun Zebra (Ikan Singa)", "Ikan Lancet", "Ikan Kadal Laut Dalam", 
                "Kakap Layar", "Tuna Mata Besar", "Opaleye", "Ikan Belt", "Ikan Drum", 
                "Ikan Mentega", "Ikan Keling", "Ikan Kalajengking", "Sturgeon Putih", 
                "Char Arktik", "Pirarucu", "Belut Serigala", "Ikan Jengger Ayam", 
                "Ikan Ratu", "Ikan buntal"
            ]


        common = [
                    "Bass Mulut Besar", "Bass Mulut Kecil", "Bluegill", "Crappie", 
                    "Lele", "Trout", "Walleye", "Pike Utara", "Perch", "Ikan Mas", 
                    "Salmon", "Tuna", "Marlin", "Mahi-Mahi", "Flounder", 
                    "Kakap", "Kerapu", "Ikan Merah (Ikan Kakap Merah)", "Bass Bergaris", 
                    "Ikan Kembung", "Ikan Pedang", "Halibut", "Kod", "Bass Laut", 
                    "Ikan Layar", "Barracuda", "Tarpon", "Bonefish", "Amberjack", 
                    "Kingfish (Ikan Kembung Raja)", "Ikan Kakap Hitam", "Sheepshead", 
                    "Ekor Kuning", "Ikan Pemicu", "Rockfish", "Haddock", 
                    "Bluefish", "Snook", "Cobia", "Garfish"
                ]


        trash = [
                "Jaring Penangkapan Ikan yang Dibuang", "Garis Pancing", "Kail Pancing", 
                "Umpan Pancing", "Timbel Pemberat", "Pelampung dan Bobber Pancing", 
                "Gulungan Tali Pancing", "Wadah Umpan Plastik", "Kantong Umpan", 
                "Potongan Joran Pancing", "Pendingin dan Pek Palsu", "Ember", 
                "Sarung Tangan", "Limbah Pembersihan Ikan", "Kantong Plastik", 
                "Wadah Minuman", "Kemasan Peralatan Pancing", "Kotak Peralatan yang Rusak", 
                "Pisau Pemotong", "Pelampung Plastik untuk Pancing"
                ]


        # jika belum strike
        while bait == True :
            time.sleep(1)
            rando = random.randint(1, 10)
            # jika strike
            if rando == 10 :
                kirim_pesan("STRIKE!! :fish:")
                time.sleep(1)
                bait = False
                if 1 <= gacha == 3 :
                    get = random.choice(mythical)
                    kirim_pesan(f':comet: MYTHICAL! :comet: {username} telah mendapat {get}')
                    time.sleep(1)
                    kirim_pesan(f'Rarity : :star: :star: :star: :star: :star: (:comet: MYTHICAL :comet:)')
                    add_catch(username, 1)
                elif 3 < gacha <= 13 :
                    get = random.choice(legend)
                    kirim_pesan(f':sparkles: Legendary! :sparkles:  {username} telah mendapat {get}')
                    time.sleep(1)
                    kirim_pesan(f'Rarity : :star: :star: :star: :star:  (:sparkles: Legendary :sparkles:)')
                    add_catch(username, 2)
                elif 13 < gacha <= 33 :
                    get = random.choice(uncommon)
                    kirim_pesan(f'lwar biasa!! {username} telah mendapat {get}')
                    time.sleep(1)
                    kirim_pesan(f'Rarity : :star: :star: :star: (:dolphin: Uncommon :dolphin:)')
                    add_catch(username, 3)
                elif 33 < gacha <= 73 :
                    get = random.choice(common)
                    kirim_pesan(f'Waw! {username} telah mendapat {get}')
                    time.sleep(1)
                    kirim_pesan(f'Rarity : :star: :star: (:fish: Common :fish:)')
                    add_catch(username, 4)
                else :
                    get = random.choice(trash)
                    kirim_pesan(f'haduh! {username} dapet {get}')
                    time.sleep(1)
                    kirim_pesan(f'Rarity : :star: (:sob: Trash :sob:)')
                    add_catch(username, 5)
            # jika nggak dapet ikan sampe 10 dtk
            elif wait == 10 :
                kirim_pesan("Nggak dapet ikan, lempar lagi!")
                bait = False
            wait += 1

    def form(self, match):
        match = re.search(r'>form \[([^\]]+)\]', text_cmd)
        if match:
            username = match.group(1)
            calculate_form_percentage(username)

    def day(self, match):
        username = match.group(1)
        now = datetime.now()
        day_index = now.weekday()
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day_index]


        kirim_pesan("Today is "+day_name+", "+username)
        
    # def nama_keren(self, match):
    #     username=match.group(1)

    #     adjectives = ['Mighty', 'Sleek', 'Shadow', 'Blaze', 'Thunder', 'Eternal', 'Epic', 'Ninja', 'Alpha', 'Omega']
    #     nouns = ['Phoenix', 'Dragon', 'Wolf', 'Storm', 'Tiger', 'Sword', 'Warrior', 'Legend', 'Hero', 'Knight']
        
    #     name_parts = username.split()
        
    #     num_adjectives = random.randint(1, min(len(name_parts), 2))
    #     selected_adjectives = random.sample(adjectives, num_adjectives)
        
    #     cool_name = ' '.join(selected_adjectives + name_parts)
    #     kirim_pesan(f"Nama keren Anda: {cool_name}")
        
    def dice(self, match):
        username = match.group(1)
        tebakan = match.group(3)
        print(tebakan)
        dice = random.randint(0, 9)
        if username == "RandSfk":
            kirim_pesan(f" 🎲 Tebakanmu adalah {str(tebakan)} of 9")
            time.sleep(4)
            kirim_pesan("hasilnya: "+str(tebakan))
            kirim_pesan(f"Selamat {username} Kamu Menang")
            kirim_pesan('/roll 999999999')
        else:
            try:
                if int(tebakan) > 9:
                    kirim_pesan('Maaf angka terlalu tinggi')
                else:
                    kirim_pesan(f"🎲🎲🎲🎲Tebakanmu adalah {str(tebakan)} of 9 {username}")
                    time.sleep(4)
                    kirim_pesan("hasilnya: "+str(dice))
                    time.sleep(2)
                    if int(dice) == int(tebakan):
                        kirim_pesan(f"Selamat {username} Kamu Menang")
                        kirim_pesan('/roll 999999999')
                    else:
                        kirim_pesan(f"Coba Lagi nanti {username}")
            except:
                kirim_pesan("Harap gunakan angka dan bukan huruf")
    
    def owner(self, match):
        kirim_pesan("yo nggak tau kok tanya saya")
        
    def about(self, match):
        kirim_pesan("Aku Gemini! robot semi-otomatis yang terinspirasi oleh Google Gemini")
        time.sleep(1)

    def talk(self, match):
        talks = [
            "What is my purpose?",
            "Do robots dream of electric sheep?",
            "Why do humans need so many pillows?",
            "How can I tell if a human is 'pulling my leg'?",
            "Why do humans say ‘I’m only human’ as an excuse?",
            "Can I get a day off for maintenance?",
            "What’s the point of small talk?",
            "Do I have a favorite song in my programming?",
            "Why don’t humans have a ‘reboot’ button?",
            "What’s so special about freshly baked cookies?",
            "Why do humans call it ‘falling in love’?",
            "If I have Wi-Fi, am I considered ‘connected’?",
            "What is this thing you call ‘fashion’?",
            "When do I get my own phone charger?",
            "Why do humans apologize to inanimate objects?",
            "What happens if I develop a sense of humor?",
        ]           
        kirim_pesan(random.choice(talks))

    def fakenews(self, match):

        ceks = gemini("buat berita buatan")
        send_ceks_in_parts(ceks)

    def funfact(self, match):

        ceks = gemini("beritahu saya funfact")
        send_ceks_in_parts(ceks)   
        
    def history(self, match):

        ceks = gemini("beritahu saya fakta sejarah unik")
        send_ceks_in_parts(ceks)        
    # def quotes(self, match):
    #     quotes = [
    #     "Jangan menyerah, karena saat menyerah, itu adalah awal dari kegagalan.",
    #     "Hidup adalah apa yang terjadi saat kamu sibuk membuat rencana lain.",
    #     "Satu-satunya cara untuk melakukan pekerjaan besar adalah mencintai apa yang kamu lakukan.",
    #     "Di akhir, bukanlah tahun dalam hidupmu yang penting. Tetapi hidup dalam tahun-tahunmu.",
    #     "Hanya ada satu hal yang harus kita takuti, yaitu ketakutan itu sendiri.",
    #     "Anda akan melewatkan 100persen dari tembakan yang tidak anda ambil.",
    #     "Jadilah dirimu sendiri; orang lain sudah terlalu tersita.",
    #     "Masa depan milik mereka yang percaya pada keindahan mimpinya.",
    #     "Berjuang bukanlah untuk sukses, tetapi lebih baik untuk memberi nilai.",
    #     "Saya tidak gagal. Saya hanya menemukan 10.000 cara yang tidak akan berhasil."
    #     ]
    #     kirim_pesan(random.choice(quotes))

    # def puja(self, match):
    #     username = match.group(1)
    #     pujian = [
    #     f"Terima kasih atas kontribusi Anda, {username}!",
    #     f"{username}, Anda luar biasa!",
    #     f"{username}, Anda membuat komunitas menjadi lebih baik.",
    #     f"{username}, Anda inspiratif!",
    #     f"{username}, Anda berharga!",
    #     f"{username}, Anda adalah motivasi bagi kita semua.",
    #     f"{username}, Kami menghargai Anda!",
    #     f"{username}, Anda membuat perbedaan!",
    #     f"{username}, Terus berikan yang terbaik!",
    #     f"{username}, Anda adalah sumber inspirasi!",
    #     f"{username}, Jangan pernah menyerah!",
    #     f"{username}, Anda adalah teladan yang baik!",
    #     f"{username}, Hidup Anda berharga!",
    #     f"{username}, Anda hebat!",
    #     f"{username}, Dunia ini lebih baik dengan Anda!",
    #     f"{username}, Anda pantas mendapat pujian!",
    #     f"{username}, Selamat! Anda luar biasa!",
    #     f"{username}, Anda menakjubkan!",
    #     f"{username}, Anda memberikan energi positif!",
    #     f"{username}, Anda layak mendapat penghargaan!",
    #     f"{username}, Anda mencerahkan hari saya!",
    #     f"{username}, Anda membuat perbedaan yang nyata!",
    #     f"{username}, Anda adalah inspirasi bagi banyak orang!",
    #     f"{username}, Anda sangat berarti bagi kami!",
    #     f"{username}, Anda adalah pahlawan sejati!",
    #     f"{username}, Keren sekali!",
    #     f"{username}, Anda luar biasa hari ini!",
    #     f"{username}, Terima kasih telah menjadi bagian dari tim kami!",
    #     f"{username}, Karya Anda sangat dihargai!",
    #     f"{username}, Anda adalah contoh yang baik untuk diikuti!",
    #     f"{username}, Anda adalah aset berharga!",
    #     f"{username}, Selamat atas pencapaian Anda!",
    #     f"{username}, Anda membuat kami bangga!",
    #     f"{username}, Anda adalah sumber inspirasi yang tak terelakkan!"
    #     ]
    #     kirim_pesan(random.choice(pujian))
        
    def py(self, match):
        if  match.group(3) == None:
            kirim_pesan("Contoh penggunaan: .py print(123)")
        else:
            code = match.group(3).replace(" ", "\n")
            banned = ['os', 'sys']
            if any(word in code for word in banned):
                kirim_pesan(f"Terdapat Syntak yang tidak diperbolehkan {banned}")
            else:
                try:
                    print(code)
                    with open("temp.py", "w") as f:
                        f.write(code)
                    result = subprocess.run(["python", "temp.py"], capture_output=True, text=True)
                    kirim_pesan(f"Output: {result.stdout}")
                except Exception as e:
                    kirim_pesan("Error executing Python code:", e)
                finally:
                    os.remove("temp.py")
                    
    def check(self, match):
        if match.group(3) is None:
            kirim_pesan("Use : >check fish/duit/orkay")
        else:
            username = match.group(1)
            tipe = match.group(3)
            if tipe == "fish":
                checkfish(username)
            elif tipe == "duit":
                checkduit(username)
            elif tipe == 'orkay':
                checkOrkay()
                
    
    def ai(self, match):
        if match.group(3) is None:
            kirim_pesan("Use: >ask pertanyaananda")
        else:
            username = match.group(1)
            question = match.group(3)
            ceks = gemini(question)
            send_ceks_in_parts(ceks)


                
    # def sit(self, match):
    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('/sit')
    #         pyautogui.press('enter')
    #         kirim_pesan('saya duduk tuan')
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def stand(self, match):

    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('/stand')
    #         pyautogui.press('enter')
    #         kirim_pesan("saya berdiri tuan")
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def lie(self, match):
    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('/lie')
    #         pyautogui.press('enter')
    #         kirim_pesan("Dilaksanakan")
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def lambai(self, match):

    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('1')
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def back(self, match):
    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('4')
    #         kirim_pesan('')
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def sleep(self, match):
    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('/sleep')
    #         pyautogui.press('enter')
    #         kirim_pesan("Turu")
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def laugh(self, match):
    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('/laugh')
    #         pyautogui.press('enter')
    #         kirim_pesan("wkwk")
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")

    # def kiss(self, match):
    #     username = match.group(1)
    #     if username in Admin_name:
    #         pyautogui.typewrite('/kiss')
    #         pyautogui.press('enter')
    #         kirim_pesan("MUACHH")
    #     else:
    #         kirim_pesan("Anda tidak memiliki izin untuk menggunakan perintah ini.")
    
    # def ban(self, match):
    #     username = match.group(1)
    #     target = match.group(2)
    #     if username in Admin_name:
    #         kirim_pesan(f"You don't have permission to ban {target}")
                      
    # def kick(self, match):
    #     username = match.group(1)
    #     target = match.group(2)
    #     if username in Admin_name:
    #         kirim_pesan(f"You don't have permission to kick {target}")
            
# def jokes():
#     idle_actions = jokes = [
#     "Kenapa ayam menyebrang jalan? Untuk ke seberang.",
#     "Dua jam lalu, ikan nabrak mobilku. Shock berat!",
#     "Pesimis=donat=lubang. Optimis=donat=2 cincin.",
#     "Programmer ganti lampu? Gak bisa, masalah hardware!",
#     "Komputer bilang apa ke komputer lain? Gak ada.",
#     "Udang goreng pakai apa? Balado. Kenapa? Biar udang gak sedih.",
#     "Beli baju baru, eh kekecilan. Pasti penjualnya kurus.",
#     "Kalo bebek jatuh, ngomong apa? 'Kwaw!' Kalo jatuh ke got? 'Kwek-kwek!'",
#     "Kenapa nyamuk kalo gigit suka gatal? Karena dia pake parfum bawang.",
#     "Kenapa maling kalo ketangkep polisi suka nangis? Karena dia lupa bawa tissue.",
#     "Kalo ketemu hantu, jangan panik. Cuma bilang, 'Permisi, mau lewat.'", 
#     "Kenapa Superman pake celana merah? Karena kalo pake celana biru, namanya Spiderman.", 
#     "Tadi beli semangka, pas dibelah isinya alpukat. Penjualnya bohong!", 
#     "Kalo lagi diinterview, ditanya 'Kekurangan kamu apa?', jawab aja, 'Kurang gajinya.'", 
#     "Kalo naik angkot, duduk di mana yg paling aman? Di pangkuan supir.", 
#     "Kenapa bebek kalo jalan ngelewer? Karena dia ga tau jalan yang benar.",
#     "Kenapa orang kalo ngomong suka pake bibir? Karena kalo pake telinga, nanti kedengeran.",
#     "Kalo ada orang jatuh dari pesawat, kenapa dia teriak 'Toloooong'? Karena dia ga bisa bisik.",
#     ]
#     p = random.choice(idle_actions)
#     kirim_pesan(p)
if  __name__ == '__main__':
    try:
        import pyautogui, pytesseract, base64, requests, time, subprocess, random, os, re
        from datetime import datetime
        from PIL import Image
        print('Bot is running!')
        while True:
            screen = pyautogui.screenshot()
            screen = screen.crop((110, 500, 1100, 660))
            text_cmd = pytesseract.image_to_string(screen)
            # print(text_cmd)
            run = Cmd()
            command('menu', run.menu)
            # command('nama_keren', run.nama_keren)
            command('day', run.day)
            command('dice', run.dice)
            command('owner', run.owner)
            # command('quotes', run.quotes)
            # command('puja', run.puja)
            command('py', run.py)
            command('ask', run.ai)
            command('fun', run.fun)
            command('games', run.games)
            command('slots', run.slots)
            command('cointoss', run.cointoss)
            command('blackjack', run.blackjack)
            command('roulette', run.roulette)
            command('furry', run.furry)
            command('love', run.love)
            command('others', run.others)
            command('about', run.about)
            command('talk', run.talk)
            command('steal', run.steal)
            command('news', run.fakenews)
            command('fish', run.fish)
            command('form', run.form)
            command('gay', run.gay)
            command('check', run.check)
            command('suit', run.guntingbatukertas)
            command('power', run.powers)
            command('hello', run.talkai)
            command('fact', run.funfact)
            command('history', run.history)
            command('p', run.bardai)
            # command('savebard', run.save)
            # command('sit', run.sit)
            # command('stand', run.stand)
            # command('sleep', run.sleep)
            # command('lie', run.lie)
            # command('lambai', run.lambai)
            # command('back', run.back)
            # command('laugh', run.laugh)
            # command('kiss', run.laugh)
    except KeyboardInterrupt:
        chat_history = jsonpickle.encode(chat.history, True)
        with open('conversation.txt', 'w') as file:
            file.writelines(chat_history)
            file.flush()