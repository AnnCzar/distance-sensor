import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


class Sensor:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Distance Measurement")

        # inicjalziacja portu szeregowego
        self.serial_port = 'COM5'  
        self.baud_rate = 9600
        self.ser = None

        self.unit = tk.StringVar(value="cm")

        self.create_widgets() # stworzenie okna

        self.data = []

    def create_widgets(self):

        serial_frame = ttk.LabelFrame(self.root, text="Serial Connection")
        serial_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(serial_frame, text="Serial Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_entry = ttk.Entry(serial_frame)
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port_entry.insert(0, self.serial_port)

        ttk.Label(serial_frame, text="Baud Rate:").grid(row=1, column=0, padx=5, pady=5)
        self.baud_entry = ttk.Entry(serial_frame)
        self.baud_entry.grid(row=1, column=1, padx=5, pady=5)
        self.baud_entry.insert(0, self.baud_rate)

        self.connect_button = ttk.Button(serial_frame, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Measurement mode frame
        mode_frame = ttk.LabelFrame(self.root, text="Measurement Mode")
        mode_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.mode = tk.StringVar(value="continuous")
        self.froms = tk.StringVar(value="10")
        self.to = tk.StringVar(value="20")

        ttk.Radiobutton(mode_frame, text="Continuous", variable=self.mode, value="continuous",
                        command=self.clear_plot).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(mode_frame, text="Single", variable=self.mode, value="single", command=self.clear_plot).grid(
            row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(mode_frame, text="Range", variable=self.mode, value="range",
                        command=self.clear_plot).grid(row=2, column=0, padx=5, pady=5, sticky="w")

        ttk.Label(mode_frame, text="From (cm):").grid(row=2, column=1, padx=5, pady=5, sticky="e")
        self.interval_entry = ttk.Entry(mode_frame, textvariable=self.froms)
        self.interval_entry.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Label(mode_frame, text="To (cm):").grid(row=3, column=1, padx=5, pady=5, sticky="e")
        self.interval_entry1 = ttk.Entry(mode_frame, textvariable=self.to)
        self.interval_entry1.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        self.start_button = ttk.Button(mode_frame, text="Start Measurement", command=self.start_measurement)
        self.start_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.stop_button = ttk.Button(mode_frame, text="Stop Measurement", command=self.stop_measurement)
        self.stop_button.grid(row=4, column=1, columnspan=3, padx=10, pady=5)

        # Unit selection frame
        unit_frame = ttk.LabelFrame(self.root, text="Distance Unit")
        unit_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Radiobutton(unit_frame, text="Millimeters (mm)", variable=self.unit, value="mm",
                        command=self.clear_plot).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(unit_frame, text="Centimeters (cm)", variable=self.unit, value="cm",
                        command=self.clear_plot).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(unit_frame, text="Decimeters (dm)", variable=self.unit, value="dm",
                        command=self.clear_plot).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(unit_frame, text="Meters (m)", variable=self.unit, value="m", command=self.clear_plot).grid(
            row=3, column=0, padx=5, pady=5, sticky="w")

        # wykres
        plot_frame = ttk.LabelFrame(self.root, text="Distance Plot")
        plot_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-')  # wykres dla trybu ciągłego
        self.scatter, = self.ax.plot([], [], 'ro')  # scatter plot dla trybu range
        self.ax.set_ylim(0, 200)  
        self.ax.set_xlim(0, 100)  
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Distance (cm)')

        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.ani = FuncAnimation(self.figure, self.update_plot, interval=200)

        save_frame = ttk.LabelFrame(self.root, text="Save Measurements")
        save_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(save_frame, text="Filename:").grid(row=0, column=0, padx=5, pady=5)
        self.filename_entry = ttk.Entry(save_frame)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(save_frame, text="Save to File", command=self.save_to_file)
        self.save_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        display_frame = ttk.LabelFrame(self.root, text="Measured Distance")
        display_frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(display_frame, text="Distance:", font = ("Arial", 15 )).grid(row=0, column=0, padx=5, pady=5)
        self.distance_label = ttk.Label(display_frame, text="N/A", font = ("Arial", 15 ))
        self.distance_label.grid(row=0, column=1, padx=5, pady=5)

        display_message_frame = ttk.LabelFrame(self.root, text="Warning message")
        display_message_frame.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(display_message_frame, text="Message:", font = ("Arial", 15 )).grid(row=0, column=0, padx=5, pady=5)
        self.warning_label = ttk.Label(display_message_frame, text="No warnings", font = ("Arial", 15 ))
        self.warning_label.grid(row=0, column=1, padx=5, pady=5)




    def connect_serial(self):  # funkcja do otwarcia portu szeregowego
        port = self.port_entry.get()
        baud = int(self.baud_entry.get())

        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            messagebox.showinfo("Success", f"Connected to {port} at {baud} baud.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def start_measurement(self):
        self.data = []
        mode = self.mode.get()
        self.start_time = time.time()

        if mode == "single":
            self.measure_single()
        elif mode == "continuous":
            self.measure_continuous()
        elif mode == "range":
            froms = int(self.froms.get())
            to = int(self.to.get())
            self.measure_range(froms, to)

    def stop_measurement(self):
        self.running = False

    def measure_single(self):
        distance = self.read_distance()
        if distance is not None:
            self.update_distance_display(distance)

    def measure_continuous(self):
        self.running = True
        threading.Thread(target=self._continuous_measurement).start()

    def _continuous_measurement(self):
        while self.running:
            distance = self.read_distance()
            if distance is not None:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.data.append((time.time(), distance, timestamp))
                self.update_distance_display(distance)
            time.sleep(0.2)

    def measure_range(self, froms, to):
        self.running = True
        threading.Thread(target=self._range_measurement, args=(froms, to,)).start()

    def _range_measurement(self, froms, to):
        next_measurement_time = time.time()
        while self.running:
            current_time = time.time()
            if current_time >= next_measurement_time:
                distance = self.read_distance()
                if distance is not None and distance<= to and distance >= froms :
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.data.append((time.time(), distance, timestamp))
                    self.update_distance_display(distance)
                    self.warning_label.config(text=f"No warnings")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.data.append((time.time(), 0, timestamp))
                    self.update_distance_display(0)
                    self.warning_label.config(text=f"Measurment out of range")

    def read_distance(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'R')
            line = self.ser.readline().decode().strip()
            try:
                distance = int(line)
                unit = self.unit.get()
                if unit == "mm":
                    distance *= 10  
                elif unit == "dm":
                    distance /= 10  
                elif unit == "m":
                    distance /= 100  
                return distance
            except ValueError:
                return None
        return None

    def clear_plot(self):
        self.data = []
        self.scatter.set_data([], [])
        self.line.set_data([], [])
        self.ax.figure.canvas.draw()

    def update_plot(self, frame=None):
        if not self.data:
            return

        times, distances, _ = zip(*self.data)
        adjusted_times = [t - self.start_time for t in times]

        if self.mode.get() == "continuous":
            self.line.set_data(adjusted_times, distances)
        else:
            self.scatter.set_data(adjusted_times, distances)

        self.ax.set_xlim(min(adjusted_times), max(adjusted_times) + 1)
        self.ax.set_ylim(min(distances) - 10, max(distances) + 10)
        self.ax.set_ylabel(f'Distance ({self.unit.get()})')
        self.ax.figure.canvas.draw()

    def update_distance_display(self, distance):
        self.distance_label.config(text=f"{distance} {self.unit.get()}")

    def save_to_file(self):
        filename = self.filename_entry.get()
        if not filename:
            messagebox.showwarning("Filename Required", "Please enter a filename.")
            return

        with open(f"{filename}.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time", f"Distance ({self.unit.get()})", "Timestamp"])
            for times, distance, timestamp in self.data:
                writer.writerow([times - self.start_time, distance, timestamp])

        messagebox.showinfo("Success", f"Data saved to {filename}.csv")


root = tk.Tk()
app = Sensor(root)
root.mainloop()

