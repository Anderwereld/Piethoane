import random
import csv
import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    print("Sensor Data")
    print("1. nieuwe sensor metingen")
    print("2. Laad metingen uit CSV")
    
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Kies").strip()
        if choice not in ["1", "2"]:
            print("Dat mag niet.")
            
    if choice == "1":
        sensor_type = input("Voer sensortype in").strip()
        if not sensor_type:
            sensor_type = "sensor"
            
        while True:
            try:
                count = int(input("Aantal metingen:"))
                if count <= 0:
                    print("Aantal moet meer zijn dan 0")
                    continue
                break
            except ValueError:
                print("Voer een getal in.")
                
        while True:
            try:
                min_val = float(input("Minimale waarde: "))
                max_val = float(input("Maximale waarde: "))
                if min_val >= max_val:
                    print("Minimale waarde moet kleiner zijn dan de maximale waarde.")
                    continue
                break
            except ValueError:
                print("Voer een geldig getal in voor min en max.")
                
        while True:
            try:
                threshold = float(input("drempelwaarde: "))
                break
            except ValueError:
                print("Voer een geldig getal in voor de drempelwaarde.")
                
        return {
            "mode": "generate",
            "sensor_type": sensor_type,
            "count": count,
            "min_val": min_val,
            "max_val": max_val,
            "threshold": threshold
        }
    else:
        filename = input("geef csv bestandsnaam: ").strip()
        if not filename:
            filename = "readings.csv"
            
        while True:
            try:
                threshold = float(input("drempelwaarde voor analyse: "))
                break
            except ValueError:
                print("Voer een geldig getal in.")
                
        return {
            "mode": "load",
            "filename": filename,
            "threshold": threshold
        }

def generate_readings(count, minimum, maximum):
    random.seed(42)  
    readings = [round(random.uniform(minimum, maximum), 2) for _ in range(count)]
    return readings

def calculate_statistics(readings):
    arr = np.array(readings)
    stats = {
        "count": len(arr),
        "mean": np.mean(arr),
        "min": np.min(arr),
        "max": np.max(arr),
        "std": np.std(arr)
    }
    return stats

def find_outliers(readings, threshold):
    arr = np.array(readings)
    above_threshold = arr[arr > threshold]
    return above_threshold

def save_readings(filename, readings):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["sample", "reading"])
            for sample_num, reading in enumerate(readings, start=1):
                writer.writerow([sample_num, reading])
        print(f"opgeslagen in '{filename}'.")
    except OSError as e:
        print(f"Fout bij opslaan: {e}")

def load_readings(filename):
    readings = []
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                readings.append(float(row["reading"]))
        print(f"succesvol '{filename}' geopend.")
    except FileNotFoundError:
        print(f"Kan'{filename}' Niet openen.")
    return readings

def plot_readings(readings, threshold, sensor_type):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(readings) + 1), readings, marker='o', linestyle='-', color='blue', label='Metingen')
    plt.axhline(y=threshold, color='red', linestyle='--', label=f'Threshold ({threshold})')
    plt.title(f'Sensor Metingen - {sensor_type}')
    plt.xlabel('Sample Nummer')
    plt.ylabel('Waarde')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_histogram(readings, sensor_type):
    plt.figure(figsize=(8, 5))
    plt.hist(readings, bins=10, color='green', edgecolor='black', alpha=0.7)
    plt.title(f'Sensor Metingen - {sensor_type}')
    plt.xlabel('Waarde')
    plt.ylabel('Frequentie')
    plt.grid(True)
    plt.show()

def main():
    user_data = get_user_input()
    if user_data["mode"] == "generate":
        readings = generate_readings(user_data["count"], user_data["min_val"], user_data["max_val"])
        save_readings("readings.csv", readings)
        sensor_type = user_data["sensor_type"]
        threshold = user_data["threshold"]
    else:
        filename = user_data["filename"]
        threshold = user_data["threshold"]
        readings = load_readings(filename)
        sensor_type = "Geladen Sensor"
        
        if not readings:
            print("Geen data beschikbaar.")
            return
    stats = calculate_statistics(readings)
    print("\nAnalyse Resultaten")
    print(f"Aantal metingen: {stats['count']}")
    print(f"Gemiddelde: {stats['mean']:.2f}")
    print(f"Minimum: {stats['min']}")
    print(f"Maximum: {stats['max']}")
    print(f"Standaardafwijking: {stats['std']:.2f}")

    outliers = find_outliers(readings, threshold)
    print(f"Aantal uitstekende waardes ({threshold}): {len(outliers)}")
    if len(outliers) > 0:
        print(f"Uitstekende waardes: {list(outliers)}")
    else:
        print("Geen uitstekende waardes.")

    plot_readings(readings, threshold, sensor_type)
    plot_histogram(readings, sensor_type)

if __name__ == "__main__":
    main()