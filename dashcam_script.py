import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import time
import os
import cv2

# Funzione per convertire il tempo NMEA in un formato leggibile
def nmea_time_to_readable(nmea_time, date_str):
    if nmea_time and len(nmea_time) >= 6:
        try:
            # Estrae l'ora dal tempo NMEA
            time_only = datetime.strptime(nmea_time.split('.')[0], '%H%M%S').time()
            # Converte la data NMEA in un formato leggibile
            full_datetime = datetime.strptime(date_str, '%d%m%y')
            # Combina data e ora
            return datetime.combine(full_datetime, time_only).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    return None

# Funzione per convertire una coordinata NMEA in gradi decimali
def nmea_to_decimal(nmea_coord):
    if not nmea_coord:
        return None
    try:
        # Estrae i gradi dalla coordinata NMEA
        degrees = float(nmea_coord) // 100
        # Estrae i minuti dalla coordinata NMEA e li converte in gradi decimali
        minutes = float(nmea_coord) % 100 / 60
        # Combina gradi e minuti
        return degrees + minutes
    except ValueError:
        return None

# Funzione per convertire la velocità da nodi a km/h
def knots_to_kmh(speed_in_knots):
    if not speed_in_knots:
        return None
    try:
        # Converte la velocità da nodi a km/h
        return float(speed_in_knots) * 1.852
    except ValueError:
        return None
# Funzione per analizzare le linee NMEA
def parse_nmea_lines(nmea_lines):
    data_dict = {}
    for nmea_line in nmea_lines:
        parts = nmea_line.split(',')
        if parts[0] == "$GPRMC":
            # Estrae il tempo e la velocità dalla linea "$GPRMC"
            data_dict['Time'] = nmea_time_to_readable(parts[1], parts[9])
            data_dict['Speed'] = knots_to_kmh(parts[7])
        elif parts[0] == "$GPGGA":
            # Estrae la latitudine, la longitudine e l'altitudine dalla linea "$GPGGA"
            data_dict['Latitude'] = nmea_to_decimal(parts[2])
            data_dict['Longitude'] = nmea_to_decimal(parts[4])
            data_dict['Altitude'] = parts[9]
    return data_dict

# Funzione per estrarre i frame da un video
def extract_frames(video_file, output_folder, data_list):
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    for i, data in enumerate(data_list):
        cap.set(cv2.CAP_PROP_POS_MSEC, i * 1000 / fps)
        ret, frame = cap.read()
        if ret:
            frame_file = os.path.join(output_folder, f'frame_{i}.jpg')
            cv2.imwrite(frame_file, frame)
            data['Frame'] = frame_file
    cap.release()

# Funzione per estrarre i dati NMEA da un file di input
def extract_nmea_to_files(input_file, video_file, output_folder, timer_label):
    start_time = time.time()
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data_list = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("$GPRMC") and i + 1 < len(lines) and lines[i + 1].startswith("$GPGGA"):
            # Analizza una coppia di linee NMEA
            parsed_data = parse_nmea_lines([lines[i], lines[i + 1]])
            if parsed_data:
                # Aggiunge i dati analizzati alla lista
                data_list.append(parsed_data)
            i += 2
        else:
            i += 1

    # Estrae i frame dal video
    extract_frames(video_file, output_folder, data_list)
    # Crea un DataFrame dai dati
    df = pd.DataFrame(data_list)
    # Crea un GeoDataFrame dai dati
    gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df.Longitude, df.Latitude) if 'Longitude' in df and 'Latitude' in df])
    # Imposta il sistema di riferimento delle coordinate
    gdf.set_crs(epsg=4326, inplace=True)

    # Percorsi dei file di output
    shapefile_output = os.path.join(output_folder, 'output.shp')
    csv_output = os.path.join(output_folder, 'output.csv')

    # Salva i dati in un file Shapefile e CSV
    gdf.to_file(shapefile_output, driver='ESRI Shapefile')
    df.to_csv(csv_output, index=False)

    end_time = time.time()
    elapsed_time = end_time - start_time
    timer_label.config(text=f"Tempo impiegato: {elapsed_time} secondi")
# Funzione per avviare l'estrazione dei dati in un nuovo thread
def start_extraction(input_file, video_file, output_folder, timer_label):
    extraction_thread = Thread(target=extract_nmea_to_files, args=(input_file, video_file, output_folder, timer_label))
    extraction_thread.start()

# Funzione per selezionare un file
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Funzione per selezionare una cartella
def select_folder(entry):
    folder_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)

# Crea l'interfaccia grafica
root = tk.Tk()

input_label = tk.Label(root, text="File di input NMEA:")
input_label.pack()
input_entry = tk.Entry(root)
input_entry.pack()
input_button = tk.Button(root, text="Sfoglia", command=lambda: select_file(input_entry))
input_button.pack()

video_label = tk.Label(root, text="File video MP4:")
video_label.pack()
video_entry = tk.Entry(root)
video_entry.pack()
video_button = tk.Button(root, text="Sfoglia", command=lambda: select_file(video_entry))
video_button.pack()

output_label = tk.Label(root, text="Cartella di output:")
output_label.pack()
output_entry = tk.Entry(root)
output_entry.pack()
output_button = tk.Button(root, text="Sfoglia", command=lambda: select_folder(output_entry))
output_button.pack()

timer_label = tk.Label(root, text="")
timer_label.pack()

start_button = tk.Button(root, text="Avvia", command=lambda: start_extraction(input_entry.get(), video_entry.get(), output_entry.get(), timer_label))
start_button.pack()

root.mainloop()