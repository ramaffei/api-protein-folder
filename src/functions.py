from werkzeug.utils import secure_filename
from zipfile import ZipFile

ALLOWED_EXTENSIONS = ['zip',]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extractFileByArchive(file, folder, condicion):
    with ZipFile(file) as zipfile:
        list_name_archive = zipfile.namelist()
        for name_archive in list_name_archive:
            if name_archive.endswith(condicion):
                zipfile.extract(secure_filename(name_archive), folder)

