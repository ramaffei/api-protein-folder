import io
import json
from matplotlib import pyplot as plt

import numpy as np

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

if __name__ == '__main__':
# Uso de la función
    file_path = 'upload/JSONs/rank_1_model_1_ptm_seed_1_1E57_1_PHYSALIS MOTTLE VIRUS_PHYSALIS MOTTLE VIRUS_pae.json'
    plot_z_scores_from_json(file_path)