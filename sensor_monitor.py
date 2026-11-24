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
                
