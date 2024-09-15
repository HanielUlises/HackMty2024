from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pinecone import Pinecone

from openai import OpenAI

DATA_BASE_URI = "mongodb+srv://losCaris:k3sqwhuHtS8q1rKI@datacompany.hhzul.mongodb.net/?retryWrites=true&w=majority&appName=DataCompany"

def init_pinecone():
  # Inicializar Pinecone con tu API Key
  pc = Pinecone(
    api_key="4b0a21a6-406b-4f35-a7c8-ab0a52a9f73e"
  )
  conection = pc.Index(name="company", host="https://company-rk4tcos.svc.aped-4627-b74a.pinecone.io")
  return conection 


def get_vector_metadata(index, vector_id):
    response = index.fetch(ids=[vector_id])
    
    # Check if the vector exists in the index
    if vector_id in response['vectors']:
        vector_data = response['vectors'][vector_id]
        metadata = vector_data.get('metadata', {})
        return metadata
    else:
        return None


# Función para cargar los documentos de MongoDB y almacenarlos en Pinecone
def load_documents_pinecone(index, model):
    # Obtener los documentos desde MongoDB
    response = get_all_documents()
    
    # Cargar el modelo de Hugging Face para generar embeddings
    
    # Generar embeddings y almacenar en Pinecone
    for i, r in enumerate(response['documents']):
        text = r['text']  # Contenido del documento
        metadata = {"directory": r['directory'], "file_name": r['file_name']}  # Metadatos
        
        # Generar el embedding para el contenido del documento
        embedding = model.encode([text])[0]  # Obtener el embedding
        
        # Almacenar el embedding en Pinecone con los metadatos
        index.upsert(vectors=[(f"doc_{i+1}", embedding.tolist(), metadata)])
        print(f"Document {i+1} stored in Pinecone with metadata: {metadata}")

# Función para obtener todos los documentos de MongoDB
def get_all_documents(conection):
    response_dict = {"documents": []}   
    for document in conection.find():
        directory_name = document.get("directory")
        file_name = document.get("file_name")        
        content = document.get("content")
        response_dict["documents"].append({
            "directory": directory_name, 
            "file_name": file_name, 
            "text": content
        }) 
    return response_dict

def get_text_from_metadata(metadata, mongo):
    directory = metadata['directory']
    file_name = metadata['file_name']
    
    document = mongo.find_one({"directory": directory, "file_name": file_name})
    if document:
        return document['content']
    else:
        return None


# Función para conectarse a la base de datos 'Company' y la colección 'Information'
def connect_to_company_information(uri):
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


def retrieve_document(query, index, mongo,model):
    embed = model.encode([query])[0]
    embed_list = embed.tolist()
    response = index.query(
        namespace="",
        vector=embed_list,
        top_k=5,
        include_values=True
    )
    
    ids = []
    if response['matches']:
        for match in response['matches']:
            score = match['score']  # Extraer el valor del score de similitud
        #print(match)
        if score < 0.1:  # Comparar el score de similitud con el umbral
            return None
        else:
            match_id = match['id']
            ids.append(match_id)
    else:
        return None
    if ids is not None:
        for id in ids:
            text = get_text_from_metadata(get_vector_metadata(index, id),mongo )
            #print(text)
    return ids

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



