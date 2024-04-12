import numpy as np
import statistics

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
    """ arquivo = './imagens/lorem_s12_c02_just_noise.pbm'
    imagem_str = leitor_PBM(arquivo)
    largura, altura, vetor_bidimensional = parse_string_array(imagem_str)

    matriz = filtro_mediana(largura, altura, vetor_bidimensional)
    formato = 'P1'
    salvar_PBM('./lorem_s12_c02_just_noise_sem_ruido.pbm', formato, largura, altura, matriz)

    sem_ruido = './lorem_s12_c02_just_noise_sem_ruido.pbm'
    sem_ruido_str = leitor_PBM(sem_ruido)
    largura, altura, vetor_bidimensional = parse_string_array(sem_ruido_str)
    vetor_np = np.array(vetor_bidimensional, dtype=np.uint8) """

    """ elemento_estruturante_dilatacao = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1]], dtype=np.uint8)
    dilatacao0 = dilatacao(vetor_np, elemento_estruturante_dilatacao)
    dilatacao1 = dilatacao(dilatacao0, elemento_estruturante_dilatacao)
    dilatacao2 = dilatacao(dilatacao1, elemento_estruturante_dilatacao)
    dilatacao3 = dilatacao(dilatacao2, elemento_estruturante_dilatacao)
    dilatacao4 = dilatacao(dilatacao3, elemento_estruturante_dilatacao)
    salvar_PBM('./lorem_s12_c02_just_noise_dilatada.pbm', formato, largura, altura, dilatacao4) """

    img = './lorem_s12_c02_just_noise_dilatada10_copy.pbm'
    dilatacao4_str = leitor_PBM(img)
    largura, altura, vetor_bidimensional = parse_string_array(dilatacao4_str)

    print(len(vetor_bidimensional))
    coluna_central = int((largura)/2)
    qtd_linhas_col_1 = 0
    for i in range(altura-1):
        if vetor_bidimensional[i][coluna_central] == 1 and vetor_bidimensional[i+1][coluna_central] == 0:
            qtd_linhas_col_1 += 1

    print(qtd_linhas_col_1)
    
    coluna_central = int((largura+1)/2)
    qtd_linhas_col_2 = 0
    for i in range(altura-1):
        if vetor_bidimensional[i][coluna_central] == 1 and vetor_bidimensional[i+1][coluna_central] == 0:
            qtd_linhas_col_2 += 1

    print(qtd_linhas_col_2)
