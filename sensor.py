import glob

def ler_temperatura():
    try:
        arquivo = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')[0]
        with open(arquivo, 'r') as f:
            linhas = f.readlines()
        if 'YES' in linhas[0]:
            return float(linhas[1].split('t=')[1]) / 1000.0
        return None
    except:
        return None

if __name__ == '__main__':
    temp = ler_temperatura()
    if temp:
        print(f'Temperatura: {temp:.1f} °C')
    else:
        print('ERRO: Sensor não encontrado!')
