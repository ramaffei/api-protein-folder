import io
import json
from matplotlib import pyplot as plt
from Bio.PDB import Superimposer, PDBParser
import numpy as np
from scipy.stats import zscore

def plot_z_scores_from_json(file_path, save=True, show=False):
    # Cargar los datos desde el archivo JSON
    with open(file_path, 'r') as file:
        predicciones = json.load(file)

    # Extraer la lista de distancias
    distancias = [entry.get('distance', [[]])[0] for entry in predicciones]  # Suponiendo que 'distance' es una lista

    # Aplanar la lista de listas de distancias
    distancias = [d for sublist in distancias for d in sublist]

    # Calcular la media y la desviación estándar
    media_distancia = np.mean(distancias)
    std_dev_distancia = np.std(distancias)

    # Calcular Z-scores
    z_scores = [(distancia - media_distancia) / std_dev_distancia for distancia in distancias]

    # Calcula los colores basados en los Z-scores
    colors = plt.cm.RdYlBu_r(np.abs(z_scores) / np.max(np.abs(z_scores)))

    # Ajusta el tamaño del gráfico
    plt.figure(figsize=(10, 6))

    # Crea el gráfico de barras
    bars = plt.bar(range(len(z_scores)), z_scores, color=colors)

    # Agrega una barra horizontal en cero para indicar la media
    plt.axhline(0, color='black', linewidth=0.8, linestyle='dashed')

    # Calcula el promedio de los Z-scores
    average_z_score = np.mean(z_scores)

    # Dibuja la línea de promedio
    plt.axhline(average_z_score, color='red', linewidth=1, linestyle='dashed', label=f'Promedio: {average_z_score:.3e}')

    # Personaliza el gráfico
    plt.ylabel('Z-score')
    plt.title('Z-scores para cada aminoácido')

    # Muestra la leyenda
    #plt.legend()

    # Muestra el gráfico
    if save:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer
    if show:
        plt.show()

def calcular_zscore_desde_pdb(archivo_pdb1, archivo_pdb2):
    # Parsear las estructuras desde los archivos .pdb
    parser = PDBParser(QUIET=True)
    estructura1 = parser.get_structure("estructura1", archivo_pdb1)
    estructura2 = parser.get_structure("estructura2", archivo_pdb2)

    # Obtener los átomos CA alineados de ambas estructuras
    atoms1 = []
    atoms2 = []
    for model1, model2 in zip(estructura1, estructura2):
        for chain1, chain2 in zip(model1, model2):
            for residue1, residue2 in zip(chain1, chain2):
                atom1 = residue1['CA']
                atom2 = residue2['CA']
                atoms1.append(atom1)
                atoms2.append(atom2)

    # Realizar el alineamiento estructural
    superimposer = Superimposer()
    superimposer.set_atoms(atoms1, atoms2)
    superimposer.apply(atoms1)

    # Calcular las distancias euclidianas entre los átomos alineados
    distancias = []
    for atom1, atom2 in zip(atoms1, atoms2):
        distancia = np.linalg.norm(atom1.get_coord() - atom2.get_coord())
        distancias.append(distancia)

    # Calcular el Z-score
    z_scores = zscore(distancias)

    return z_scores

def graficar_zscores(z_scores, save=True, show=False):
    # Calcular el promedio de Z-score por residuo
    promedio_por_residuo = np.mean(z_scores)

    # Graficar los Z-scores y el promedio
    plt.figure(figsize=(10, 6))
    plt.plot(z_scores, label='Z-score por residuo')
    plt.axhline(y=promedio_por_residuo, color='r', linestyle='--', label='Promedio de Z-score')
    plt.xlabel('Residuo')
    plt.ylabel('Z-score')
    plt.title('Z-scores por Residuo')
    plt.legend()
    plt.grid(True)

    # Agregar el valor promedio al gráfico
    plt.text(0.05, 0.9, f'Promedio: {promedio_por_residuo:.2e}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        # Muestra el gráfico
    if save:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer
    if show:
        plt.show()

if __name__ == '__main__':
    """     # Uso de la función
    file_path = 'upload/JSONs/rank_1_model_1_ptm_seed_1_1E57_1_PHYSALIS MOTTLE VIRUS_PHYSALIS MOTTLE VIRUS_pae.json'
    plot_z_scores_from_json(file_path) """
    from os.path import abspath, dirname

    BASE_DIR = dirname(dirname(abspath(__file__)))
    # Archivos .pdb de ejemplo
    archivo_pdb1 = BASE_DIR+"/results/1E57_1_PHYSALIS_MDSIAN.pdb"
    archivo_pdb2 = BASE_DIR+"/results/MGYP000470333580.pdb"

    # Calcular Z-score
    z_scores = calcular_zscore_desde_pdb(archivo_pdb1, archivo_pdb2)

    # Graficar Z-scores
    graficar_zscores(z_scores)