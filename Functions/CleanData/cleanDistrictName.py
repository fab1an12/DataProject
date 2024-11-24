import re

def limpiar_nombre_barrio(nombre):
    nombre = nombre.lower()
    nombre = nombre.replace("ï", "i")
    nombre = re.sub(r"[^a-z0-9\s-]", "", nombre)
    return nombre.replace(" ", "-")
