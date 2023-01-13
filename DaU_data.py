import zipfile
import os
from GoogleDrive_API_connections.GDriveFunctions import download_file

path = "D_data/"
file = "Images.zip"

if not os.path.exists(path):
    os.mkdir(path)
    print("Successfully created folder")

if not os.path.exists(path + file):
    download_file(file, path)

with zipfile.ZipFile(path + file, 'r') as zip_ref:
    zip_ref.extractall(path)
    print("Successful unpacking")

os.remove(path + file)
print("Successful deletion of compressed file")


