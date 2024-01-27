Guida al Codice
Importazione delle Librerie
Il codice inizia importando una serie di librerie necessarie per il suo funzionamento:

pandas e geopandas: Utilizzate per gestire e analizzare dati tabellari e geospaziali.
shapely.geometry: Fornisce strumenti per manipolare e analizzare forme geometriche, in questo caso per creare punti.
datetime: Per lavorare con date e orari.
tkinter: Per creare un'interfaccia grafica utente (GUI).
threading: Per eseguire processi in parallelo.
time e os: Utilizzati per funzionalità di base del sistema operativo.
cv2: Libreria di OpenCV per l'elaborazione di video e immagini.
Funzioni di Conversione e Analisi
Conversione del Tempo NMEA:

nmea_time_to_readable: Converte l'orario in formato NMEA in un formato leggibile e comprensibile. Ad esempio, converte l'ora da una stringa come "123456" in un formato orario standard.
Conversione delle Coordinate NMEA:

nmea_to_decimal: Trasforma le coordinate NMEA, che sono in gradi e minuti, in gradi decimali, un formato più comune per la rappresentazione delle coordinate geografiche.
Conversione della Velocità da Nodi a km/h:

knots_to_kmh: Converte la velocità da nodi, comunemente usata in ambito nautico, in chilometri orari.
Analisi delle Linee NMEA:

parse_nmea_lines: Estrae informazioni utili dalle linee di dati NMEA, come tempo, velocità, latitudine, longitudine e altitudine.
Elaborazione Video
Estrazione dei Frame dal Video:
extract_frames: Estrae i frame da un file video a intervalli regolari, basandosi sui dati temporali forniti e li salva in una cartella specificata.
Processo di Estrazione Dati
Estrazione e Analisi dei Dati NMEA:

extract_nmea_to_files: Legge i dati NMEA da un file, li analizza utilizzando le funzioni sopra descritte, estrae i frame corrispondenti dal video e poi salva i dati in un DataFrame (pandas) e un GeoDataFrame (geopandas).
Creazione di un Thread per l'Estrazione:

start_extraction: Avvia il processo di estrazione dei dati in un thread separato per non bloccare l'interfaccia grafica.
Interfaccia Grafica con Tkinter
Selezione di File e Cartelle:

select_file e select_folder: Permettono all'utente di selezionare file e cartelle attraverso la GUI.
Setup dell'Interfaccia Grafica:

Questa sezione crea l'interfaccia grafica utilizzando Tkinter, con etichette, campi di testo e pulsanti per permettere all'utente di inserire i percorsi dei file e avviare l'elaborazione.
Esecuzione del Programma
Infine, il codice avvia l'interfaccia grafica e attende che l'utente interagisca con essa per iniziare il processo di estrazione e analisi dei dati.
