- ## API-PROTEIN-FOLDER

Este proyecto es una API REST Flask que proporciona funcionalidades para la gestión de archivos relacionados con proteínas.
### Ejecución del Proyecto en Local

Para ejecutar este proyecto en tu máquina local, sigue estos pasos: 
1. **Clonar el Repositorio:** 

```bash
git clone https://github.com/ramaffei/api_protein_folder.git
``` 
2. **Crear un Entorno Virtual (opcional pero recomendado):** 

```Copy code
python -m venv venv
``` 
3. **Activar el Entorno Virtual:**  
- En Windows:

```Copy code
venv\Scripts\activate
``` 
- En macOS y Linux:

```bash
source venv/bin/activate
``` 
4. **Instalar los Requerimientos:** 

```Copy code
pip install -r requirements.txt
``` 
5. **Ejecutar la Aplicación Flask en Modo Debug:** 

```Copy code
flask --app app run --debug
```
### Endpoints
#### 1. /upload 
- **Descripción:**  Este endpoint recibe un archivo zip y retorna un JSON con las rutas relativas de los archivos descomprimidos, organizados por extensiones. 
- **Ejemplo de Uso en JavaScript con Fetch:** 

```javascript
fetch('http://localhost:5000/upload', {
  method: 'POST',
  body: formData // FormData object with 'zipFile' key containing the zip file
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```
#### 2. /pdb/ 
- **Descripción:**  Este endpoint recibe un JSON con un parámetro obligatorio "filenames", que es un array con las rutas relativas de ciertos archivos, y un parámetro opcional "ignored_residues" que es booleano. 
- **Ejemplo de Uso en JavaScript con Fetch:** 

```javascript
const requestData = {
  filenames: ['file1.pdb', 'file2.pdb'],
  ignored_residues: true
};

fetch('http://localhost:5000/pdb/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(requestData)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```
#### 3. /pdb/plots 
- **Descripción:**  Este endpoint recibe un JSON con un parámetro obligatorio "filenames" y retorna una imagen en base64. 
- **Ejemplo de Uso en JavaScript con Fetch:** 

```javascript
const requestData = {
  filenames: ['file1.pdb', 'file2.pdb']
};

fetch('http://localhost:5000/pdb/plots', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(requestData)
})
.then(response => response.blob())
.then(blob => {
  const imageURL = URL.createObjectURL(blob);
  // Use imageURL to display the image
})
.catch(error => console.error('Error:', error));
```

¡Listo! Ahora puedes utilizar esta API en tu entorno local para gestionar archivos relacionados con proteínas. Si tienes alguna pregunta, no dudes en contactarme.# api-protein-folder