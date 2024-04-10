
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
    while len(bitmap) < height and i < len(lines):
        # Ignora linhas que começam com '#'
        if not lines[i].startswith('#'):  
            row = [int(pixel) for pixel in lines[i].strip()]
            row = leftover_chars+row
            leftover_chars = []

            # Preenche a linha com caracteres da próxima linha se for mais curta que a largura
            # Enquanto o tamanho da linha for menor do que a largura
            while len(row) < width:
                next_line_chars = [int(pixel) for pixel in lines[i + 1].strip()]
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
                row = row[:width]
                # print('if', row)
                

            bitmap.append(row)
        i += 1

    return bitmap


def salvar_PBM(nome_arquivo, formato, largura, altura, pixels):
    """ with open(nome_arquivo, 'w') as arquivo:
        # Escrever o tipo e dimensões
        arquivo.write(f"{tipo}\n")
        arquivo.write(f"{largura} {altura}\n")

        # Escrever os dados da imagem
        for linha in dados_imagem:
            linha_formatada = " ".join(str(pixel) for pixel in linha)
            arquivo.write(linha_formatada + "\n") """

def dilatacao_com_elemento_estruturante(imagem, elemento_estruturante):
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

    return nova_imagem

if __name__ == "__main__":
    # arquivo = './imagens/lorem_s12_c02_espacos_noise.pbm'
    # arquivo = './imagens/lorem_s12_c02_espacos.pbm'
    # arquivo = './imagens/lorem_s12_c02_just_noise.pbm'
    # arquivo = './imagens/lorem_s12_c02_just.pbm'
    arquivo = './dilatacao_pbm.pbm'
    imagem = leitor_PBM(arquivo)
    array = parse_pbm_string(imagem)
    print(len(array))
    print(len(array[0]))
    print(array)
    print(len(array[7]))