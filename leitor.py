import netpbmfile
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
    width, height = map(int, lines[1].split())
    print(width,height)

    bitmap = []
    leftover_chars = []

    i = 2
    while len(bitmap) < height and i < len(lines):
        if not lines[i].startswith('#'):  # Ignora linhas que começam com '#'
            # print('Remaining',leftover_chars)
            row = [int(pixel) for pixel in lines[i].strip()]
            if i == 2:
                print(len(row))
            row = leftover_chars+row
            leftover_chars = []
            # print('Row 1', row)

            # Preenche a linha com caracteres da próxima linha se for mais curta que a largura
            if len(row) < width:
                remaining_chars = width - len(row)
                next_line_chars = [int(pixel) for pixel in lines[i + 1].strip()[: remaining_chars]]
                lines[i+1] = lines[i+1][remaining_chars:]
                row.extend(next_line_chars)
                # print('Row 2',row)

            elif len(row) > width:
                leftover_chars = [int(pixel) for pixel in lines[i].strip()[width:]]
                row = row[:width]
                

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
    # arquivo = './dilatacao_pbm.pbm'
    arquivo = './lorem_s12_c02_espacos_noise.pbm'
    imagem = leitor_PBM(arquivo)
    array = parse_pbm_string(imagem)
    print(len(array))
    # print(imagem[0])
    # print(imagem[1])
    # print(imagem[2])
    # print(imagem[3])
    # elemento_estruturante = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    # elemento_estruturante = [[0, 0, 0], [0, 1, 1], [0, 0, 0]]
    # imagem_dilatada = dilatacao_com_elemento_estruturante(imagem,elemento_estruturante)

    