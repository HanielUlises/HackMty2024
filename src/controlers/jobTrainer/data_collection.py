import requests
import data_base_handler as dh

#Debe ser recibida de un input
GITHUB_API_TOKEN = ""

# Función para ignorar directorios irrelevantes
def should_ignore_directory(dir_name):
    IGNORED_DIRECTORIES = [
        ".git", ".github", ".idea", ".vscode", "node_modules", "dist", "build", "bin", "venv", ".venv",
        "lib", "vendor", "third_party", "logs", "coverage", ".cache", "out"
    ]
    return dir_name in IGNORED_DIRECTORIES or dir_name.startswith(".")

# Función para ignorar archivos con extensiones no relevantes
def should_ignore_file(file_name):
    IGNORED_EXTENSIONS = [
        ".bin", ".exe", ".dll", ".so", ".o", ".a", ".out", ".dylib", ".img", ".pyc", ".class", ".jar", ".apk",
        ".deb", ".rpm", ".msi", ".pkg", ".sln", ".vcxproj", ".vcpkg", ".csproj", ".xcodeproj", ".idea", ".iml", 
        ".gradle", ".git", ".DS_Store", ".lock", ".ttf", ".otf", ".woff", ".woff2", ".stl", ".obj", ".fbx", ".dwg", 
        ".dxf", ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".db", ".mdb", ".accdb", ".gitignore"
    ]
    return any(file_name.endswith(ext) for ext in IGNORED_EXTENSIONS)

# Función que obtiene los archivos del repositorio y el contenido
def get_documents_github(owner, repo, path="", api_token=None):
    directory_dict = {}
    
    GITHUB_API_URL = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    # Establecer los headers para la solicitud, utilizando el token si está disponible
    headers = {"Authorization": f"token {api_token}"} if api_token else {}

    # Realizar la solicitud GET a la API de GitHub
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    if response.status_code == 200:
        files = response.json()
        
        # Usar la ruta completa (path) para organizar los archivos y subdirectorios
        full_path = path if path else "root"  # Si es la raíz, lo llamamos "root"
        
        # Agregar el directorio al diccionario si no está ya
        if full_path not in directory_dict:
            directory_dict[full_path] = []
        
        for file_info in files:
            file_name = file_info['name']
            
            # Saltar directorios que deben ser ignorados
            if file_info["type"] == "dir" and should_ignore_directory(file_name):
                print(f"Ignored directory: {file_name}")
                continue

            if file_info["type"] == "file":
                # Ignorar archivos con extensiones no relevantes
                if should_ignore_file(file_name):
                    print(f"Ignored file: {file_name}")
                    continue
                
                # Obtener el contenido del archivo
                file_content = get_file_content(file_info["download_url"], headers)
                
                # Agregar el contenido del archivo al diccionario bajo el directorio actual
                directory_dict[full_path].append({"file_name": file_name, "content": file_content})
                
            elif file_info["type"] == "dir":
                # Recursivamente obtener los archivos del subdirectorio, usando la ruta completa
                subdirectory_dict = get_documents_github(owner, repo, file_info["path"], api_token)
                
                # Actualizar el diccionario con los archivos del subdirectorio
                directory_dict.update(subdirectory_dict)
    else:
        print(f"Error obteniendo archivos: {response.status_code}")
        
    return directory_dict

# Función para obtener el contenido de un archivo dado su URL de descarga
def get_file_content(download_url, headers):
    response = requests.get(download_url, headers=headers)
    if response.status_code == 200:
        return response.text  # Devolver el contenido del archivo como texto
    else:
        print(f"Error obteniendo el contenido del archivo: {response.status_code}")
        return None

# Función para imprimir de forma gráfica los archivos y directorios
def print_graphic_structure(directory_dict, level=0):
    indent = "  " * level  # Indentación basada en el nivel de profundidad
    
    for directory, files in directory_dict.items():
        # Imprimir el directorio con un símbolo de carpeta
        print(f"{indent}📁 {directory}")
        
        for file_info in files:
            # Imprimir el archivo con un símbolo de documento y su nombre
            print(f"{indent}  ├─📄 {file_info['file_name']}")
            # Imprimir una porción del contenido del archivo
            print(f"{indent}    Contenido:\n{file_info['content'][:100]}...")  # Solo imprime los primeros 100 caracteres






