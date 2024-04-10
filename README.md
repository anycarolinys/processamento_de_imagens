Projeto de Pré OCR (Optical Character Recognition)

Dilatação e erosão
Abertura e fechamento
Transformada hit-or-miss


Opening - is the composite function of dilation and erosion. That means that it is erosion followed by dilation. What erosion means is that if we have a structuring element that is a 3 X 3 matrix, the central pixel will be replaced by the darkest pixel in the 3 X 3 neighborhood. Opening is erosion followed by dilation which makes it perfect for removing salt noise (white dots) and ensuring that the key features are relatively sharp.

Closing is dilation followed by erosion. Dilation means that the central pixel will be replaced by the brightest pixel in the vicinity (filter structural element). Perfect for removing pepper noise and ensuring that the key features are relatively sharp.

Dado que a imagem contém ruído sal e pimenta do tamanho de um pixel, é necessário primeiro remover esse ruído antes de aplicar os métodos de detecção de linhas, colunas e palavras. Aqui estão alguns conceitos de morfologia que poderiam ser úteis:

Erosão e Dilatação: Essas operações morfológicas são comumente usadas para remover ruído e refinar bordas. A erosão pode ser usada para eliminar ruído sal e a dilatação para eliminar ruído de pimenta.

Abertura e Fechamento: A abertura é uma operação que consiste em aplicar uma erosão seguida por uma dilatação. É útil para remover pequenos objetos indesejados, enquanto o fechamento (dilatação seguida de erosão) pode ajudar a fechar pequenos buracos na imagem.

Transformação de Hit-or-Miss: Esta técnica é útil para detecção de padrões específicos na imagem. Pode ser útil para detectar características de texto, como linhas horizontais e verticais.

Esqueletização: A esqueletização é uma técnica que reduz a largura dos objetos na imagem para uma linha central. Pode ser útil para detectar a estrutura básica das letras e palavras.

Detecção de Bordas: A detecção de bordas pode ajudar a identificar áreas onde o texto está localizado, fornecendo pontos de partida para a detecção de linhas e colunas.

Componentes Conectados: Identificar e rotular componentes conectados na imagem pode ajudar a separar diferentes palavras ou partes do texto.

Filtragem por Tamanho: Após a detecção de componentes conectados, é possível aplicar filtros para remover componentes muito pequenos ou muito grandes, que provavelmente não correspondem a palavras.

Transformada de Hough: A transformada de Hough pode ser útil para detectar linhas retas na imagem, o que pode ser útil para identificar bordas de linhas e colunas.

Ao combinar esses conceitos de morfologia com técnicas de processamento de imagens, você pode criar um algoritmo robusto de pré-processamento de OCR para contar linhas e colunas, além de detectar palavras em uma imagem PBM com ruído sal e pimenta. É importante experimentar e ajustar os parâmetros dessas técnicas para obter os melhores resultados para o seu conjunto de dados específico.






