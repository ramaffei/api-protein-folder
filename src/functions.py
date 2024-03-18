from io import StringIO
import os
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from Bio import SeqIO

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

def fastaToList(file_fasta):
    fasta_sequences = SeqIO.parse(StringIO(file_fasta),'fasta')
    list_sequences = []
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        list_sequences.append({
            'header': name,
            'sequence': sequence
        })
    return list_sequences

if __name__ == '__main__':
    print(fastaToList('1E57.FASTA'))