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


if __name__ == "__main__":
    # arquivo = './exemplo1.pbm'
    arquivo = './imagens/lorem_s12_c02_just_noise.pbm'
    imagem_str = leitor_PBM(arquivo)
    largura, altura, vetor_bidimensional = parse_string_array(imagem_str)
    # print(largura,altura, vetor_bidimensional)
    print(largura,altura)
    print(len(vetor_bidimensional))
    print(len(vetor_bidimensional[0]))
    print(len(vetor_bidimensional[len(vetor_bidimensional)-1]))

    matriz = filtro_mediana(largura, altura, vetor_bidimensional)

    formato = 'P1'
    salvar_PBM('./noise_gerada.pbm', formato, largura, altura, matriz)

