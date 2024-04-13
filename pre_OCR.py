import numpy as np
import statistics
import time

def leitor_PBM(arquivo):
    with open(arquivo,'r') as arquivo:
        linhas = arquivo.read()
    
    return linhas

def parse_string_array(pbm_string):
    linhas = pbm_string.split('\n')
    linhas = [linha for linha in linhas if not linha.startswith('#')]
    largura, altura = map(int, linhas[1].split())
    pixels = linhas[2:]
    
    vetor_inteiros = []
    for linha in pixels:
        vetor_inteiros.extend([int(char) for char in linha])

    vetor_convertido = [vetor_inteiros[i:i+largura] for i in range(0, len(vetor_inteiros), largura)]
    # vetor_convertido = [vetor_inteiros[i:i+largura] for i in range(0, len(vetor_inteiros), largura) if len(vetor_inteiros[i:i+largura]) == largura]

    return largura, altura, vetor_convertido

def obter_vizinhanca(linha, coluna, m):
    
    if (linha+1 < len(m) and linha-1 >= 0):
        """ vizinhos = [ m[linha-1][coluna], m[linha+1][coluna],
                m[linha][coluna-1], m[linha][coluna+1],
                m[linha-1][coluna+1], m[linha+1][coluna+1],
                m[linha-1][coluna-1], m[linha+1][coluna-1]]
        vizinhos.append(m[linha][coluna]) """
        vizinhos = [ m[linha-1][coluna][0], m[linha+1][coluna][0],
                m[linha][coluna-1][0], m[linha][coluna+1][0],
                m[linha-1][coluna+1][0], m[linha+1][coluna+1][0],
                m[linha-1][coluna-1][0], m[linha+1][coluna-1][0]]
        vizinhos.append(m[linha][coluna][0])
        vizinhos.sort()
        # print(f'[{linha}{coluna}] ', vizinhos)
        return vizinhos
    return None


def mediana(lista):
    return int(statistics.median(lista))

def filtro_mediana(largura, altura, matriz):
    # matriz_vizinhos = matriz_valores(largura,altura,matriz)
    matriz_vizinhos = matriz_valores(matriz)
    # matriz = [[1 if (i == 0 and i == altura-1 and j == 0 and j == largura-1) else 0 for j in range(largura)] for i in range(altura)]

    for i in range(1,altura-1):
        for j in range(1,largura-1):
            vizinhanca = obter_vizinhanca(i,j, matriz_vizinhos)
            novo_pixel = mediana(vizinhanca)
            matriz[i][j] = novo_pixel
    
    return matriz

# def matriz_valores(largura, altura,matriz):
def matriz_valores(matriz):
    nova_matriz = []
    for linhas in matriz:
        linha = []
        for pixel in linhas:
            linha.append([pixel,0])
        nova_matriz.append(linha)
    return nova_matriz

def salvar_PBM(nome_arquivo, formato, largura, altura, pixels):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(f"{formato}\n")
        arquivo.write(f"{largura} {altura}\n")
        
        for i in range(altura):
            for j in range(largura):
                arquivo.write(f'{pixels[i][j]}')
            arquivo.write('\n')

def dilatacao(imagem, kernel):
    altura, largura = imagem.shape
    altura_kernel, largura_kernel = kernel.shape
    imagem_dilatada = np.zeros((altura, largura), dtype=np.uint8)
    pad_h = altura_kernel // 2
    pad_w = largura_kernel // 2

    for i in range(pad_h, altura - pad_h):
        for j in range(pad_w, largura - pad_w):
            if np.sum(imagem[i-pad_h:i+pad_h+1, j-pad_w:j+pad_w+1] * kernel) > 0:
                # imagem_dilatada[i, j] = 255
                imagem_dilatada[i, j] = 1

    return imagem_dilatada

def erosao(imagem, kernel):
    altura, largura = imagem.shape
    altura_kernel, largura_kernel = kernel.shape
    imagem_erodida = np.zeros((altura, largura), dtype=np.uint8)
    pad_h = altura_kernel // 2
    pad_w = largura_kernel // 2

    for i in range(pad_h, altura - pad_h):
        for j in range(pad_w, largura - pad_w):
            # if np.min(imagem[i-pad_h:i+pad_h+1, j-pad_w:j+pad_w+1] * kernel) == 255:
            if np.min(imagem[i-pad_h:i+pad_h+1, j-pad_w:j+pad_w+1] * kernel) == 1:
                # imagem_erodida[i, j] = 255
                imagem_erodida[i, j] = 1

    return imagem_erodida

def contar_caractere(string, caractere):
    return string.count(caractere)

if __name__ == "__main__":
    inicio = time.time()
    formato = 'P1'
    img_original = './imagens_grupo/img1_ruido.pbm'
    
    imagem_str = leitor_PBM(img_original)
    largura, altura, vetor_bidimensional = parse_string_array(imagem_str)

    matriz_mediana = filtro_mediana(largura, altura, vetor_bidimensional)
    salvar_PBM('./imagens_grupo/img1_sem_ruido.pbm', formato, largura, altura, matriz_mediana)

    fim = time.time()
    tempo_total = fim - inicio

    img_sem_ruido = './imagens_grupo/img1_sem_ruido.pbm'
    sem_ruido_str = leitor_PBM(img_sem_ruido)
    largura, altura, vetor_bidimensional = parse_string_array(sem_ruido_str)
    

    print(f'Tempo de execucao {tempo_total/60} minutos')