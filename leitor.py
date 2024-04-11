
import statistics
import math


""" def dilatacao_com_elemento_estruturante(imagem, elemento_estruturante):
    altura, largura = len(imagem), len(imagem[0])
    nova_imagem = [[0] * largura for _ in range(altura)]

    # Percorre todos os pixels da imagem
    for i in range(altura):
        for j in range(largura):
            # Se o pixel atual for 1, verifique se o elemento estruturante se encaixa completamente na vizinhança
            print(imagem[i][j])
            if imagem[i][j] == 1:
                for k in range(len(elemento_estruturante)):
                    for l in range(len(elemento_estruturante[0])):
                        # Verifica se o elemento estruturante se encaixa na vizinhança do pixel atual
                        if (0 <= i + k - 1 < altura and 0 <= j + l - 1 < largura
                                and elemento_estruturante[k][l] == 1):
                            # Define o pixel correspondente na nova imagem como 1
                            nova_imagem[i + k - 1][j + l - 1] = 1

    return nova_imagem """

def leitor_PBM(arquivo):
    with open(arquivo,'r') as arquivo:
        # linhas = arquivo.readlines()
        linhas = arquivo.read()

    # Removendo comentários
    """ linhas = [linha.strip() for linha in linhas if not linha.startswith('#')]

    formato = linhas[0]
    largura, altura = map(int, linhas[1].split())

    pixels = [[int(pixel) for pixel in linha.split()] for linha in linhas[2:]] """

    return linhas
    # return formato, largura, altura, pixels

def parse_pbm_string(pbm_string):
    lines = pbm_string.split('\n')
    lines = [line for line in lines if not line.startswith('#')]
    width, height = map(int, lines[1].split())
    # print(width,height)

    bitmap = []
    leftover_chars = []

    i = 2
    # i = 3
    while len(bitmap) < height and i < len(lines):
        # Ignora linhas que começam com '#'
        if not lines[i].startswith('#'):  
            row = [int(pixel) for pixel in lines[i].strip()]
            # row = [int(pixel) for pixel in lines[i].split()]
            row = leftover_chars+row
            leftover_chars = []

            # Preenche a linha com caracteres da próxima linha se for mais curta que a largura
            # Enquanto o tamanho da linha for menor do que a largura
            while len(row) < width:
                next_line_chars = [int(pixel) for pixel in lines[i + 1].strip()]
                # next_line_chars = [int(pixel) for pixel in lines[i + 1].split()]
                remaining_next = width-len(row)
                # print('remaining',{remaining_next})
                row.extend(next_line_chars)
                if len(row) > width:
                    lines[i+1] = lines[i+1][remaining_next:]
                    row = row[:width]
                # print('While row', row)
                # print('While row[i+1]', lines[i+1])
            if len(row) > width:
                leftover_chars = [int(pixel) for pixel in lines[i].strip()[width:]]
                # leftover_chars = [int(pixel) for pixel in lines[i].split()[width:]]
                row = row[:width]
                # print('if', row)
                

            bitmap.append(row)
        i += 1

    return width, height, bitmap

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
    # soma = sum(lista)
    # if soma > 4:
    #     return 1
    # return 0

    # return int(math.ceil(statistics.median(lista)))
    return int(statistics.median(lista))

def filtro_mediana(largura, altura, matriz):
    matriz_vizinhos = matriz_valores(largura,altura,matriz)
    matriz = [[1 if (i == 0 and i == altura-1 and j == 0 and j == largura-1) else 0 for j in range(largura)] for i in range(altura)]

    for i in range(1,altura-1):
        for j in range(1,largura-1):
            # print(f'Posicao {i} {j}: {matriz[i][j]}')
            vizinhanca = obter_vizinhanca(i,j, matriz_vizinhos)
            # novo_pixel = mediana(obter_vizinhanca(i,j, matriz))
            # print(f'Vizinhanca {vizinhanca}')
            novo_pixel = mediana(vizinhanca)
            # print(f'Novo pixel:', novo_pixel)
            matriz[i][j] = novo_pixel
    # for i, linha in enumerate(matriz):
        # for j, pixel in enumerate(linha):

    return matriz

def matriz_valores(largura, altura,matriz):
    nova_matriz = []
    for linhas in matriz:
        linha = []
        for pixel in linhas:
            # linha.append({pixel:0})
            linha.append([pixel,0])
        nova_matriz.append(linha)
    return nova_matriz

def salvar_PBM(nome_arquivo, formato, largura, altura, pixels):
    with open(nome_arquivo, 'w') as arquivo:
        # Escrever o tipo e dimensões
        arquivo.write(f"{formato}\n")
        arquivo.write(f"{largura} {altura}\n")
        
        # Escrever os dados da imagem
        """ for linha in dados_imagem:
            linha_formatada = " ".join(str(pixel) for pixel in linha)
            arquivo.write(linha_formatada + "\n") """
        for i in range(altura):
            for j in range(largura):
                arquivo.write(f'{pixels[i][j]}')
                # arquivo.write(f'{pixels[i][j]} ')
            arquivo.write('\n')

if __name__ == "__main__":
    # arquivo = './imagens/lorem_s12_c02_espacos_noise.pbm'
    # arquivo = './imagens/lorem_s12_c02_espacos.pbm'
    # arquivo = './imagens/lorem_s12_c02_just.pbm'
    # arquivo = './pgm/cameraman.pgm'
    arquivo = './exemplo1.pbm'
    # arquivo = './imagens/lorem_s12_c02_just_noise.pbm'
    imagem = leitor_PBM(arquivo)
    largura, altura, matriz = parse_pbm_string(imagem)
    
    print(f'Matriz original', matriz)
    valores = matriz_valores(largura, altura, matriz)


    # formato = 'P1'
    # matriz = filtro_mediana(largura, altura, matriz)
    
    # print(f'Matriz com filtro', len(matriz[0]))
    # salvar_PBM('./noise_mediana.pbm', formato, largura, altura, matriz)