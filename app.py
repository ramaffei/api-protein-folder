import os
from flask import Flask, request
from src.functions import allowed_file, extractFileByArchive

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'

@app.route('/',methods=["GET", "POST"])
def server_up():
    return {'msg':'SERVER_UP'}

@app.route("/upload", methods=['POST'])
def uploadAndApply():
    file = request.files['zipFile']

    if not file or not allowed_file(file.filename):
        return {'msg': 'No se encontró el archivo valido'}, 403
    
    folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    
    try:
        # Archivos JSONs
        folder_json = os.path.join(folder, 'JSONs')
        extractFileByArchive(file, folder_json, '.json')

        # Archivos PDBs
        folder_pdb = os.path.join(folder, 'PDBs')
        extractFileByArchive(file, folder_pdb, '.pdb')
    except:
        {'msg': 'Ocurrió un error al cargar los archivos'}

    return {'msg': 'Archivos cargados con éxito'}

