from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

directorio_credenciales = 'credentials_module.json'

# sign in
def loggin():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()
    
    return GoogleDrive(gauth)

# Create simple text file
def create_text_file(file_name, content, id_folder):
    credentials = loggin()
    file = credentials.CreateFile({
        'title': file_name,
        'parents': [{'kind': 'drive#fileLink',
                    'id': id_folder}]})
    file.SetContentString(content)
    file.Upload()

# Upload a file
def upload_file(file_path, id_folder):
    credentials = loggin()
    file = credentials.CreateFile({
        'parents': [{'kind': 'drive#fileLink',
                    'id': id_folder}]})
    file['title'] = file_path.split('/')[-1]
    file.SetContentFile(file_path)
    file.Upload()

# Download a file
def download_file(id_file, file_path):
    credenciales = loggin()
    archivo = credenciales.CreateFile({'id': id_file})
    nombre_archivo = archivo['title']
    archivo.GetContentFile(file_path + nombre_archivo)

def download_file_by_title(title, file_path):
    credentials = loggin()
    file_item = credentials.ListFile({'q': "title = '"+title+"'"}).GetList()
    id_file = ""
    for file in file_item:
        id_file = file['id']
    archivo = credentials.CreateFile({'id': id_file})
    try:
        archivo.GetContentFile(file_path + title)
        print("Successful Download")
    except Exception as e:
        if title in os.listdir(file_path):
            os.remove(file_path + title)
        print(e)
        print("Download Failed")

# Search for files
def search_for_file(query):
    result = []
    credentials = loggin()
    file_list = credentials.ListFile({'q': query}).GetList()
    for file in file_list:
        # ID Drive
        print('ID Drive:', file['id'])
        # Link de descarga
        print('link de descarga:', file['downloadUrl'])
        # Nombre del archivo
        print('Nombre del archivo:', file['title'])
        # Tipo de archivo
        print('tipo de archivo:', file['mimeType'])
        # Tamaño
        print('Tamaño:', file['fileSize'])
        print(''.center(50, '-'))
        result.append(file)
    
    return result

# Get all folders
def get_folders(query):
    result = []
    credentials = loggin()
    file_list = credentials.ListFile({'q': query}).GetList()
    for file in file_list:
        result.append(file)

    return result

# ID by title
def get_id_of_title(title):
    credentials = loggin()
    file_item = credentials.ListFile({'q': "title = '"+title+"'"}).GetList()
    for file in file_item:
        return file['id']


if __name__ == '__main__':
    id = get_id_of_title("100_registros_csv.csv")
    path = "/home/marshal/python_exercises/MLops_Project/"
    download_file_by_title("100_registros_csv.csv", "../")

