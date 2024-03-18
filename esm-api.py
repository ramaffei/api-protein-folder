import os
import time
import requests
import biotite.structure.io as bsio
from src.AlphaRamachan import plot
from src.fetch_pdb import phi_psi

URL_API = 'https://api.esmatlas.com'

def get_PDB_by_sequence(data, filename = ''):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    header = data.get('header', '>unnamed')
    sequence = data.get('sequence')

    if not sequence:
        raise 'No se proporciono ninguna secuencia'

    endpoint = '/foldSequence/v1/pdb/'
    response = requests.post(f'{URL_API}{endpoint}', headers=headers, data=sequence, verify=False)
    pdb_string = response.content.decode('utf-8')
    
    if not filename:
        name = sequence[:3] + sequence[-3:]
        filename = os.path.join(f'results/{header.replace(">","")}_{name}.pdb')
    
    with open(filename, 'w') as f:
        f.write(pdb_string)
    
    return filename
    """     struct = bsio.load_structure(filename, extra_fields=["b_factor"])
    plddt = set(struct.b_factor)
    # plDDT value is stored in the B-factor field
    #plot_proceed = plot(filename, save=False, show=True) """

def get_PDB_by_targetID(target_id):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    endpoint = f'/fetchPredictedStructure/{target_id}'
    response = requests.get(f'{URL_API}{endpoint}', headers=headers, verify=False)
    pdb_string = response.content.decode('utf-8')
    
    filename = os.path.join(f'results/{target_id}.pdb')
    
    with open(filename, 'w') as f:
        f.write(pdb_string)
    
    return filename

def get_PDB_first_similar_sequence(data):
    
    headers = {
    'authority': 'api.esmatlas.com',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'origin': 'https://esmatlas.com',
    'referer': 'https://esmatlas.com/',
    }

    endpoint = '/searchSequence/ticket'
    header = data.get('header', '>unnamed')
    sequence = data.get('sequence')
    data = {
        'q': f'{header}\n{sequence}',
        'mode':'accept',
        'email':'rodrigoa.maffei@gmail.com',
        'database[]':'highquality_clust30'
    }

    response = requests.post(f'{URL_API}{endpoint}', headers=headers, data=data, verify=False)
    json_reponse = response.json()
    ticket_id = json_reponse.get('id')

    result = get_ticket_result(ticket_id)

    if not result:
        raise 'Ticket result error'
    
    sequences = result[0].get('alignments')
    if not sequences:
        raise 'Not sequences similar'
    
    seq_max_scores = max(sequences, key=lambda x:x['score'])
    target_id = seq_max_scores.get('target')

    return get_PDB_by_targetID(target_id)

def get_ticket_result(ticket_id):
    headers = {
        'authority': 'api.esmatlas.com',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://esmatlas.com',
        'referer': 'https://esmatlas.com/',
    }
        
    if not ticket_id:
        raise 'Error, no ticket id'
    
    endpoint = '/searchSequence/result/'
        
    while True:
        response2 = requests.get(
        f'{URL_API}{endpoint}{ticket_id}/0',
        headers=headers, verify=False
        )
        if response2.status_code == 200:
            response_json2 = response2.json()
            print(response_json2)
            return response_json2.get('results')

if __name__ == '__main__':
    data = {
        'header': '>1E',
        'sequence': 'MDSSEVVKVKQASIPASQPNTEQSPAIVLPFQFEATTFGTAETAAQVSLQTADPITKLTAPYRHAQIVECKAILTPTDLAVSNPLTVYLAWVPANSPATPTQILRVYGGQSFVLGGAISAAKTIEVPLNLDSVNRMLKDSVTYTDTPKLLAYSRAPTNPSKIPTASIQISGRIRLSKPMLIAN'
    }

    pdb_similar = get_PDB_first_similar_sequence(data)
    pdb_sequence = get_PDB_by_sequence(data)

    print(pdb_similar)
    print(pdb_sequence)