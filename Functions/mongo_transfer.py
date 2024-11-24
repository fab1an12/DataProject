from pymongo import MongoClient

# Conexión a MongoDB local
local_client = MongoClient("mongodb://root:example@localhost:27017/")  # Cambia el URI
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

    cloud_collection_name = input(f"Introduce el nombre de la colección en la nube para '{local_collection_name}': ")
    
    # Obtener colecciones
    local_collection = local_db[local_collection_name]
    cloud_collection = cloud_db[cloud_collection_name]

    # Transferir documentos
    print(f"Transfiriendo documentos de '{local_collection_name}' a '{cloud_collection_name}'...")
    documents = local_collection.find()
    inserted_count = 0

    for document in documents:
        # Remover el campo '_id' para evitar conflictos si ya existe en la colección destino
        document.pop('_id', None)
        cloud_collection.insert_one(document)
        inserted_count += 1

    print(f"Transferencia de '{local_collection_name}' completada. {inserted_count} documentos transferidos.")

