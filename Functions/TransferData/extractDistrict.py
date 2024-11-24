from pymongo import MongoClient

MONGO_URI = "mongodb+srv://fabianmiulescu:DataProject2024@cluster0.dzrgu.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
DB_NAME = "distritos_barrios"
COLLECTION_NAME = "distritos"

def extraer_barrios():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Extraer los nombres de barrios y coordenadas
    barrios = collection.find({}, {"nombre": 1, "geo_shape.geometry.coordinates": 1, "_id": 0})
    barrios_lista = []
    for barrio in barrios:
        nombre = barrio["nombre"]
        coordenadas = barrio["geo_shape"]["geometry"]["coordinates"]
        barrios_lista.append({"nombre": nombre, "coordenadas": coordenadas})
    return barrios_lista