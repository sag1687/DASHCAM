import shapefile
import simplekml
import gpxpy
import gpxpy.gpx
import tkinter as tk
from tkinter import filedialog

def convert_shp_to_kml_gpx(input_shp, output_kml, output_gpx):
    # Carica il file shp
    sf = shapefile.Reader(input_shp)

    # Crea un nuovo file kml
    kml = simplekml.Kml()
    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.points)):
            kml.newpoint(coords=[(shape.shape.points[i][0], shape.shape.points[i][1])])
    kml.save(output_kml)

    # Crea un nuovo file gpx
    gpx = gpxpy.gpx.GPX()
    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.points)):
            waypoint = gpxpy.gpx.GPXWaypoint(shape.shape.points[i][1], shape.shape.points[i][0])
            gpx.waypoints.append(waypoint)
    with open(output_gpx, 'w') as f:
        f.write(gpx.to_xml())

def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Seleziona un file", filetypes = (("shape files","*.shp"),("all files","*.*")))
    return filename

def save_file_dialog():
    filename = filedialog.asksaveasfilename(defaultextension='.kml')
    return filename

def save_file_dialog_gpx():
    filename = filedialog.asksaveasfilename(defaultextension='.gpx')
    return filename

def convert():
    input_shp = browse_files()
    output_kml = save_file_dialog()
    output_gpx = save_file_dialog_gpx()
    convert_shp_to_kml_gpx(input_shp, output_kml, output_gpx)

root = tk.Tk()
button = tk.Button(root, text="Converti", command=convert)
button.pack()
root.mainloop()
