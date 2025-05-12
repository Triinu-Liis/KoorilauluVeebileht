import os

# Set the folder path you want to clean
kaust = '/home/triinuliist/mysite/static/salvestatud'

# Loop through all files in the folder
for f in os.listdir(kaust):
    failitee = os.path.join(kaust, f)
    try:
        if os.path.isfile(failitee):
            os.remove(failitee)
            print(f"Kustutasin: {failitee}")
    except Exception as e:
        print(f"Faili {failitee} ei saanud kustutada: {e}")