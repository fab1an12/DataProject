from pymongo import MongoClient

# Conexión a MongoDB local
local_client = MongoClient("mongodb://localhost:27017")  # Cambia el URI
local_db_name = input("Introduce el nombre de tu base de datos local: ")
local_db = local_client[local_db_name]

# Conexión a MongoDB en la nube
cloud_client = MongoClient("mongodb+srv://fabianmiulescu:DataProject2024@cluster0.dzrgu.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
cloud_db_name = input("Introduce el nombre de tu base de datos en la nube: ")
cloud_db = cloud_client[cloud_db_name]

while True:
    local_collection_name = input("\nIntroduce el nombre de la colección local (o escribe 'salir' para terminar): ")
    if local_collection_name.lower() == 'salir':
        print("Transferencia completada.")
        break

    if local_collection_name not in local_db.list_collection_names():
        print(f"La colección '{local_collection_name}' no existe en la base de datos local. Intenta de nuevo.")
        continue

    cloud_collection_name = input(f"Introduce el nombre de la colección en la nube para '{local_collection_name}': ")
    
    # Obtener colecciones
    local_collection = local_db[local_collection_name]
    cloud_collection = cloud_db[cloud_collection_name]