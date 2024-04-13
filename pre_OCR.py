import os
import statistics
import time
import numpy as np

""" leitor_PBM
recebe o caminho de um arquivo .pbm como entrada e lê todo o seu conteúdo, 
retornando uma  string contendo as linhas do arquivo. """
def leitor_PBM(arquivo):
    # Abre o arquivo em modo de leitura 
    with open(arquivo,'r') as arquivo:
        linhas = arquivo.read()
    
    # Retorna o conteúdo do arquivo em formato string
    return linhas

""" parse_string_vetor
recebe uma string contendo o conteúdo de um arquivo .pbm e o analisa para extrair 
largura, altura e os pixels da imagem """
def parse_string_vetor(pbm_string):
    # Divide a string em uma lista de linhas, separadas pelo caractere de quebra de linha
    linhas = pbm_string.split('\n')
    
    # Remove linhas de comentário que começam com '#' da lista
    linhas = [linha for linha in linhas if not linha.startswith('#')]
    
    # Obtem a largura e altura da imagem a partir da segunda linha e converte para inteiros
    largura, altura = map(int, linhas[1].split())
    
    # Obtem os pixels da imagem a partir da terceira linha
    pixels = linhas[2:] 
    
    vetor_inteiros = []
    for linha in pixels:
        # Converte cada caractere da linha para inteiro e adiciona a lista de pixels
        vetor_inteiros.extend([int(char) for char in linha])

    # Converte a lista de pixels em uma matriz bidimensional
    vetor_convertido = [vetor_inteiros[i:i+largura] for i in range(0, len(vetor_inteiros), largura)]

    return largura, altura, vetor_convertido

""" obter_vizinhanca
recebe uma posição (linha, coluna) na matriz m e retorna uma
lista contendo os valores dos pixels vizinhos, incluindo o próprio pixel. """
def obter_vizinhanca(linha, coluna, m):
    
    # Verifica se a linha está dentro dos limites da matriz
    if (linha+1 < len(m) and linha-1 >= 0):
        # Obtem a 8 vizinhança
        vizinhos = [ m[linha-1][coluna][0], m[linha+1][coluna][0],
                m[linha][coluna-1][0], m[linha][coluna+1][0],
                m[linha-1][coluna+1][0], m[linha+1][coluna+1][0],
                m[linha-1][coluna-1][0], m[linha+1][coluna-1][0]]
        
        # Adiciona o valor do próprio pixel a lista de vizinhos
        vizinhos.append(m[linha][coluna][0])
        
        # Ordena a lista de vizinhos
        vizinhos.sort()
        return vizinhos
    return None

""" mediana
    calcula a mediana de uma lista de inteiros """
def mediana(lista):
    return int(statistics.median(lista))

""" filtro_mediana
aplica o filtro da mediana a matriz de pixels """
def filtro_mediana(largura, altura, matriz):
    matriz_vizinhos = matriz_auxiliar(matriz)

    # Percorre as linhas da matriz (exceto as bordas)
    for i in range(1,altura-1):
        # Percorre as colunas da matriz (exceto as bordas)
        for j in range(1,largura-1):
            # Obtem os valores dos vizinhos do pixel atual
            vizinhanca = obter_vizinhanca(i,j, matriz_vizinhos)
            novo_pixel = mediana(vizinhanca)
             # Substitui o valor do pixel atual pelo valor da mediana
            matriz[i][j] = novo_pixel
    
    return matriz

""" matriz_auxiliar
cria uma nova matriz a partir da matriz de pixels, 
onde cada pixel é representado como uma lista contendo o valor do pixel e um marcador (inicialmente 0) """
def matriz_auxiliar(matriz):
    nova_matriz = []

    # Percorre as linhas da matriz original
    for linhas in matriz:
        linha = []
        # Percorre os pixels da linha
        for pixel in linhas:
             # Adiciona o valor do pixel e um marcador a nova linha
            linha.append([pixel,0])
        # Adiciona a nova linha a nova matriz
        nova_matriz.append(linha)
    return nova_matriz


""" salvar_PBM
salva uma imagem PBM na pasta raiz
 """
def salvar_PBM(nome_arquivo, formato, largura, altura, pixels):
    with open(nome_arquivo, 'w') as arquivo:
         # Escreve o formato na primeira linha
        arquivo.write(f"{formato}\n")
         # Escreve a largura e altura na segunda linha
        arquivo.write(f"{largura} {altura}\n")
        
        for i in range(altura):
            for j in range(largura):
                # Escreve o valor do pixel
                arquivo.write(f'{pixels[i][j]}')
            arquivo.write('\n')


"""   dilatar_imagem
aplica a operação de dilatação a uma imagem binária 
usando um elemento estruturante especificado
"""
def dilatar_imagem(image, elemento):
    # Obtem as dimensões da imagem
    altura, largura = len(image), len(image[0])
    # Obtem as dimensões do elemento estruturante
    elemento_altura, elemento_largura = len(elemento), len(elemento[0])
    # Cria uma matriz para a imagem dilatada
    imagem_dilatada = [[0 for _ in range(largura)] for _ in range(altura)]
    
    # Percorre cada pixel da imagem
    for y in range(altura):
        for x in range(largura):
            # Se o pixel atual for preto (1)
            if image[y][x] == 1:
                # Percorre o elemento estruturante
                for i in range(elemento_altura):
                    for j in range(elemento_largura):
                        # Verifica se a posição do elemento estruturante está dentro dos limites da imagem
                        if 0 <= y + i < altura and 0 <= x + j < largura:
                            # Se tiver uma sobreposição entre o pixel atual e o elemento estruturante
                            # define o pixel correspondente na imagem dilatada como preto (1)
                            if elemento[i][j] == 1:
                                imagem_dilatada[y + i][x + j] = 1
    return imagem_dilatada

def erodir_imagem(imagem, elemento):
    altura, largura = imagem.shape
    altura_elem, largura_elem = elemento.shape
    imagem_erodida = np.zeros((altura, largura), dtype=np.uint8)
    pad_altura = altura_elem // 2
    pad_largura = largura_elem // 2

    for i in range(pad_altura, altura - pad_altura):
        for j in range(pad_largura, largura - pad_largura):
            if np.min(imagem[i-pad_altura:i+pad_altura+1, j-pad_largura:j+pad_largura+1] * elemento) == 1:
                imagem_erodida[i, j] = 1

    return imagem_erodida

""" contador_linhas
conta o número de linhas 
em colunas específicas de uma imagem """
def contador_linhas(vetor_imagem, qtd_colunas):
     # Verifica se o número de colunas é igual a 2
    if qtd_colunas == 2:
        # Cria uma lista para armazenar o número de linhas na primeira coluna
        array_2_col1 = []
        #  Percorre as colunas nos limites que definem a primeira coluna
        for c in range(400, 1100):
            qtd_linhas = 0
            # Percorre as linhas da primeira coluna
            # Desconsidera as 300 primeiras linhas
            # oois são espaços em branco
            for i in range(300, altura-1):
                if vetor_imagem[i][c] == 1 and vetor_imagem[i+1][c] == 0:
                    qtd_linhas += 1

            array_2_col1.append(qtd_linhas)

        array_2_col2 = []
        #  Percorre as colunas nos limites que definem a segunda coluna
        for c in range(1500, 2000):
            qtd_linhas = 0
            # Percorre as linhas da segunda coluna
            # Desconsidera as 300 primeiras linhas
            # oois são espaços em branco
            for i in range(300, altura-1):
                if vetor_imagem[i][c] == 1 and vetor_imagem[i+1][c] == 0:
                    qtd_linhas += 1

            array_2_col2.append(qtd_linhas)
        #  Retorna o número dentre o numero de linhas obtidos nas duas colunas
        return (max(array_2_col1),max(array_2_col2))
    
    # O número de colunas nao sendo 2, realiza o mesmo processo para três colunas
    elif qtd_colunas == 3:
        array_3_col1 = []
        for c in range(300, 800):
            qtd_linhas = 0
            for i in range(300, altura-1):
                if vetor_imagem[i][c] == 1 and vetor_imagem[i+1][c] == 0:
                    qtd_linhas += 1

            array_3_col1.append(qtd_linhas)

        array_3_col2 = []
        for c in range(990, 1500):
            qtd_linhas = 0
            for i in range(300, altura-1):
                if vetor_imagem[i][c] == 1 and vetor_imagem[i+1][c] == 0:
                    qtd_linhas += 1

            array_3_col2.append(qtd_linhas)

        array_3_col3 = []
        for c in range(1660, 2160):
            qtd_linhas = 0
            for i in range(300, altura-1):
                if vetor_imagem[i][c] == 1 and vetor_imagem[i+1][c] == 0:
                    qtd_linhas += 1

            array_3_col3.append(qtd_linhas)
        return (max(array_3_col1),max(array_3_col2),max(array_3_col3))

if __name__ == "__main__":
    inicio = time.time()
    formato = 'P1'

    arquivo = open('./arquivo_colunas.txt')
    conteudo = arquivo.read()
    nome_arquivo, colunas = conteudo.split('\n')
    colunas = int(colunas)
    nome_arquivo_sem_extensao = os.path.splitext(nome_arquivo)[0]

    imagem_str = leitor_PBM(nome_arquivo)
    largura, altura, vetor_imagem = parse_string_vetor(imagem_str)

    print('Removendo ruidos...')
    matriz_mediana = filtro_mediana(largura, altura, vetor_imagem)
    sem_ruido = nome_arquivo_sem_extensao + '_sem_ruido.pbm' 
    salvar_PBM(sem_ruido, formato, largura, altura, matriz_mediana)
    print('Ruidos removidos!')

    sem_ruido_str = leitor_PBM(sem_ruido)
    largura, altura, vetor_imagem = parse_string_vetor(sem_ruido_str)
    # Criando um vetor de 1s com dimensao 19x19 para economizar tempo de processamento
    dimensao = 19
    elemento = [[1 for _ in range(dimensao)] for _ in range(dimensao)]

    print('Aplicando dilatação...')
    img_dilatada = dilatar_imagem(vetor_imagem, elemento)
    dilatada = nome_arquivo_sem_extensao + f'_dilatada{dimensao}.pbm'
    salvar_PBM(dilatada, formato, largura, altura, img_dilatada)
    print('Dilatação aplicada!')
    
    """ elemento = np.array([[0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0]], dtype=np.uint8)
    largura, altura, vetor_imagem = parse_string_vetor(dilatada)
    vetor_np = np.array(vetor_imagem, dtype=np.uint8)
    imagem_erodida = erodir_imagem(vetor_np, elemento) """

    dimensao = 19
    dilatada = nome_arquivo_sem_extensao + f'_dilatada{dimensao}.pbm'
    print('Lendo imagem dilatada...')
    dilatada_str = leitor_PBM(dilatada)
    largura, altura, vetor_imagem = parse_string_vetor(dilatada_str)
    print('Imagem dilatada lida!')

    print('Contando linhas...')
    linhas_em_colunas = contador_linhas(vetor_imagem, colunas)
    print('Linhas contadas!')
    print(f'Quantidade de linhas por coluna {linhas_em_colunas}')

    fim = time.time()
    tempo_total = fim - inicio
    print(f'Tempo de execucao {tempo_total} segundos')
    print(f'Tempo de execucao {tempo_total/60} minutos')