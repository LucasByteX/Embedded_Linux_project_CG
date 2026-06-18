import csv, os
from datetime import datetime

CAMINHO_CSV = '/home/arthur/datalogger/dados/temperaturas.csv'

def salvar_leitura(temperatura, alarme=False):
    novo = not os.path.exists(CAMINHO_CSV)
    with open(CAMINHO_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        if novo:
            writer.writerow(['data_hora', 'temperatura_c', 'alarme'])
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([agora, round(temperatura, 2), 'SIM' if alarme else 'NAO'])
        f.flush()
        os.fsync(f.fileno())
