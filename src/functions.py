import os
from werkzeug.utils import secure_filename
from zipfile import ZipFile

def allowed_file(filename: str, extensions: list):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def extractFileByExtension(file, folder: str, extension: str):
    extracted = []
    with ZipFile(file) as zipfile:
        for zip_info in zipfile.infolist():
            if zip_info.is_dir():
                continue

            if allowed_file(zip_info.filename, extension):
                zip_info.filename = os.path.basename(zip_info.filename)
                folder_ext = os.path.join(folder, f'{extension.upper()}s')
                extracted.append(zipfile.extract(zip_info, folder_ext))
    
    return extracted

