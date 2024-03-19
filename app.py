import base64
import os
import tempfile

from flask import Flask, request, send_file
from flask_cors import CORS

from src.fetch_pdb import phi_psi
from src.AlphaRamachan import plot
from src.functions import allowed_file, extractFileByExtension, fastaToList
from src.z_scores import calcular_zscore_desde_pdb, plot_z_scores_from_json, graficar_zscores
from src.esm_api import get_PDB_by_sequence, get_PDB_first_similar_sequence 
app = Flask(__name__)

# Obteniendo configuración por default de archivo
settings_module = os.getenv('APP_SETTINGS_MODULE')
app.config.from_object(settings_module)

# Permitiendo CORS para evitar problemas en ambiente de desarrollo (COMENTAR EN PRODUCCIÓN)
cors = CORS(app, supports_credentials=True, resources={r'/*': {'origins': '*'}})

# Formateando carpeta con ruta absoluta
#FOLDER = app.config['BASE_DIR']+app.config['UPLOAD_FOLDER']
FOLDER = os.path.dirname(os.path.abspath(__file__))+'/results'

@app.route('/',methods=["GET"])
def server_up():
    return {'msg':'SERVER UP'}

@app.route("/pdb/esm/fasta/", methods=['POST'])
def getPDBsByFasta():
    file = request.files['fastaFile']
    if not file or not allowed_file(file.filename, ['fasta', 'FASTA']):
        return {'msg': 'No se encontró un archivo valido'}, 403
    
    temp_file = tempfile.TemporaryFile()
    file.save(temp_file)
    temp_file.seek(0)
    sequences = fastaToList(temp_file.read().decode("utf-8"))
    temp_file.close()

    pdbs = {}
    for sequence in sequences:
        try:
            pdb_similar = get_PDB_first_similar_sequence(sequence, FOLDER)
            pdb_sequence = get_PDB_by_sequence(sequence, FOLDER)
        except ValueError as e:
            return {'msg': 'No se pudo procesar la solicitud'}, 400
        pdbs[sequence.get('header', 'no_name')] = {
                'pdb': pdb_sequence,
                'pdb_comparacion': pdb_similar
            }
        
    return {'msg': 'Archivos descargados con éxito', 'data': pdbs}

@app.route("/pdb/plot/zscores/", methods=['POST'])
def get_plot_zscores_compare():
    # Leyendo datos del cuerpo de la solicitud
    datos = request.get_json()
    filenames = datos.get('filenames')
    if not filenames or len(filenames) != 2:
        return {'msg': 'Error, se necesitan 2 archivos para graficar z_scores'}
    
    # Formateando nombre del archivo con la ubicación del mismo
    filename_pdb = [os.path.join(FOLDER, filename) for filename in filenames]

    z_scores = calcular_zscore_desde_pdb(filename_pdb[0], filename_pdb[1])
    plot_proceed = graficar_zscores(z_scores)
    encoded_image = base64.b64encode(plot_proceed.read()).decode('utf-8')

    #return send_file(plot_proceed, mimetype='image/png')
    return {'msg': 'Éxito', 'data': encoded_image}

@app.route("/upload/", methods=['POST'])
def uploadAndExtract():
    
    # Leyendo archivo de la respuesta y comprobando extension
    file = request.files['zipFile']
    if not file or not allowed_file(file.filename, ['zip']):
        return {'msg': 'No se encontró un archivo valido'}, 403
    
    extracted_archives = {}

    # Extrayendo Archivos JSONs y formateando su ruta relativa
    JSONs = extractFileByExtension(file, FOLDER, 'json')
    JSONs = [os.path.relpath(a, FOLDER) for a in JSONs]
    extracted_archives['JSON'] = JSONs

    # Extrayendo Archivos PDBs y formateando su ruta relativa
    PDBs = extractFileByExtension(file, FOLDER, 'pdb')
    PDBs = [os.path.relpath(a, FOLDER) for a in PDBs]
    extracted_archives['PDB'] = PDBs

    return {'msg': 'Archivos cargados con éxito', 'data': extracted_archives}

@app.route("/pdb/", methods=["POST"])
def get_pdb_proceed():

    # Leyendo datos del cuerpo de la solicitud
    datos = request.get_json()
    filenames = datos.get('filenames')
    if not filenames or len(filenames)<1:
        return {'msg': 'Error, no se encontraron archivos'}
    ignored_residues = datos.get('ignored_residues', False)
    
    # Formateando nombre del archivo con la ubicación del mismo
    filename_pdb = [os.path.join(FOLDER, filename) for filename in filenames]

    # Ejecutando procedimiento
    proceed = phi_psi(filename_pdb, ignored_residues)

    return {'msg': 'Éxito', 'data': proceed}

@app.route("/json/plot/zscores/", methods=["POST"])
def get_plot_z_scores():
    # Leyendo datos del cuerpo de la solicitud
    datos = request.get_json()
    filename = datos.get('filename')
    if not filename:
        return {'msg': 'Error, no se encontró ningún archivo'}
    
    # Formateando nombre del archivo con la ubicación del mismo
    filename_json = os.path.join(FOLDER, filename)

    # Ejecutando procedimiento
    plot_proceed = plot_z_scores_from_json(filename_json, show=True)
    encoded_image = base64.b64encode(plot_proceed.read()).decode('utf-8')

    #return send_file(plot_proceed, mimetype='image/png')
    return {'msg': 'Éxito', 'data': encoded_image}

@app.route("/pdb/plot/ramachandran/", methods=["POST"])
def get_plot_ramachan():
    
    # Leyendo datos del cuerpo de la solicitud
    datos = request.get_json()
    filename = datos.get('filename')
    if not filename:
        return {'msg': 'Error, no se encontró ningún archivo'}
    
    # Formateando nombre del archivo con la ubicación del mismo
    filename_pdb = os.path.join(FOLDER, filename)

    # Ejecutando procedimiento
    plot_proceed = plot(filename_pdb)
    encoded_image = base64.b64encode(plot_proceed.read()).decode('utf-8')

    #return send_file(plot_proceed, mimetype='image/png')
    return {'msg': 'Éxito', 'data': encoded_image}

@app.route("/pdb/plots/", methods=["POST"])
def get_plots():
    
    # Leyendo datos del cuerpo de la solicitud
    datos = request.get_json()
    filenames = datos.get('filenames')
    if not filenames or len(filenames)<1:
        return {'msg': 'Error, no se encontraron archivos'}
    
    # Formateando nombre del archivo con la ubicación del mismo
    filename_pdb = [os.path.join(FOLDER, filename) for filename in filenames]
    
    # Ejecutando procedimiento
    plot_proceed = plot(filename_pdb)

    encoded_image = base64.b64encode(plot_proceed.read()).decode('utf-8')

    #return send_file(plot_proceed, mimetype='image/png')
    return {'msg': 'Éxito', 'data': encoded_image}

if __name__ == '__main__':
   app.run()