import tkinter as tk
from tkinter import messagebox
import pandas as pd
import serial
import time

# Ustawienia portu szeregowego
ser = serial.Serial('COM5', 9600, timeout=1)  # Zmień 'COM5' na odpowiedni port
time.sleep(2)  # Czekaj na nawiązanie połączenia

# Globalna lista do przechowywania danych pomiarowych
data = []

# Funkcja do rozpoczęcia pomiaru
def start_measurement():
    global measuring
    measuring = True
    measure_distance()

def measure_distance():
    if measuring:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                distance = float(line)
                timestamp = time.time()
                data.append([timestamp, distance])
                distance_label.config(text=f"Odległość: {distance} cm")
            except ValueError:
                print(f"Nieprawidłowe dane: {line}")
        root.after(1000, measure_distance)  # Opóźnienie 1000 ms

# Funkcja do zatrzymania pomiaru
def stop_measurement():
    global measuring
    measuring = False

# Funkcja do zapisu danych do pliku CSV
def save_to_csv():
    if data:
        df = pd.DataFrame(data, columns=["Czas", "Odległość"])
        df.to_csv('measurements.csv', index=False)
        messagebox.showinfo("Sukces", "Dane zostały zapisane do measurements.csv")
    else:
        messagebox.showwarning("Brak danych", "Brak danych do zapisania")

# Ustawienia GUI
root = tk.Tk()
root.title("Miernik Odległości")

distance_label = tk.Label(root, text="Odległość: -- cm", font=("Helvetica", 16))
distance_label.pack(pady=20)

start_button = tk.Button(root, text="Rozpocznij pomiar", command=start_measurement, font=("Helvetica", 14))
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Zatrzymaj pomiar", command=stop_measurement, font=("Helvetica", 14))
stop_button.pack(pady=10)

save_button = tk.Button(root, text="Zapisz do CSV", command=save_to_csv, font=("Helvetica", 14))
save_button.pack(pady=10)

# Zmienna globalna do kontroli pomiaru
measuring = False

root.mainloop()

# Zamknięcie połączenia szeregowego przy zamknięciu programu
ser.close()
