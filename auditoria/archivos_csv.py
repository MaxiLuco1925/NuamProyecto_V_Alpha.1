import csv

datos = [
    ["Nombre", "Edad", "Ciudad"],
    ["Ignacio", 27, "Calama"],
    ["Maxi", 19, "Calama" ]
]

with open("datos.csv", mode="w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerows(datos)
