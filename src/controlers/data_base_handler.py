from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


DATA_BASE_URI = "mongodb+srv://losCaris:k3sqwhuHtS8q1rKI@datacompany.hhzul.mongodb.net/?retryWrites=true&w=majority&appName=DataCompany"
# Función para conectarse a la base de datos 'Company' y la colección 'Information'
def connect_to_company_information(uri):
    # Crear un nuevo cliente y conectarse al servidor MongoDB
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        # Confirmar la conexión con un ping
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # Conectarse a la base de datos 'Company'
        db = client['Company']
        
        # Conectarse a la colección 'Information'
        collection = db['Information']
        
        return collection  # Devolver la colección para operaciones adicionales
    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    
    
    
# Función para almacenar los archivos en MongoDB manteniendo la estructura
def store_files_in_mongodb(directory_dict, collection):
    for directory, files in directory_dict.items():
        for file_info in files:
            # Insertar en MongoDB respetando la jerarquía de directorios
            document = {
                "directory": directory,
                "file_name": file_info['file_name'],
                "content": file_info['content']
            }
            collection.insert_one(document)
            print(f"Stored {file_info['file_name']} in MongoDB under {directory}")


# Función para eliminar todos los registros de la colección
def delete_all_records(collection):
    try:
        # Eliminar todos los documentos de la colección
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from the collection.")
    except Exception as e:
        print(f"Error deleting documents: {e}")



