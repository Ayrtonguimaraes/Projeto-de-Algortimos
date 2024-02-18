#Importa as bibliotecas necessárias para rodar o projeto
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import *


# Classe ConjuntoDisjunto para gerenciar conjuntos disjuntos, utilizando a otimização de compressão de caminho e união por rank.
class ConjuntoDisjunto:
    # Método inicializador da classe ConjuntoDisjunto. Este método é chamado quando uma nova instância da classe é criada.
    def __init__(self, vertices):
        self.pai = {vertice: vertice for vertice in vertices}
        self.rank = {vertice: 0 for vertice in vertices}

    # Método para encontrar o representante (ou pai) do conjunto ao qual um vértice pertence. Utiliza a técnica de compressão de caminho para otimizar futuras operações.
    def encontrar(self, vertice):
        if self.pai[vertice] != vertice:
            self.pai[vertice] = self.encontrar(self.pai[vertice])
        return self.pai[vertice]

    # Método para unir os conjuntos de dois vértices, garantindo que, após a união, ambos os vértices pertençam ao mesmo conjunto.
    def unir(self, vertice1, vertice2):
        raiz1 = self.encontrar(vertice1)
        raiz2 = self.encontrar(vertice2)
        if raiz1 != raiz2:
            if self.rank[raiz1] < self.rank[raiz2]:
                self.pai[raiz1] = raiz2
            elif self.rank[raiz1] > self.rank[raiz2]:
                self.pai[raiz2] = raiz1
            else:
                self.pai[raiz2] = raiz1
                self.rank[raiz1] += 1
# Função para implementar o algoritmo de Kruskal a fim de encontrar a Árvore Geradora Mínima (AGM) de um grafo.
def kruskal(df):
    arestas_ordenadas = df.sort_values(by='weight').itertuples(index=False)
    floresta = ConjuntoDisjunto(vertices=pd.unique(df[['source', 'target']].values.ravel('K')))
    arestas_agm = []
    for aresta in arestas_ordenadas:
        origem, destino, peso, _ = aresta
        if floresta.encontrar(origem) != floresta.encontrar(destino):
            floresta.unir(origem, destino)
            arestas_agm.append(aresta)
    agm_df = pd.DataFrame(arestas_agm, columns=df.columns)
    return agm_df

# Função para criar um grafo a partir de um DataFrame utilizando a biblioteca NetworkX.
def criar_grafo(df):
    G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr=True, create_using=nx.Graph())
    return G

# Função para encontrar a Árvore Geradora Mínima (AGM) de um grafo representado por um DataFrame.
def encontrar_agm(df):
    agm_df = kruskal(df)
    return criar_grafo(agm_df)

# Função para visualizar a Árvore Geradora Mínima (AGM) de um grafo utilizando a biblioteca Matplotlib e NetworkX.
def exibir_agm(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', alpha=0.6)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.title("Árvore Geradora Mínima do Córtex Visual de Rato", size=15)
    plt.axis('off')
    plt.show()

# Função para iniciar a interface gráfica do usuário utilizando Tkinter, para visualização da Árvore Geradora Mínima (AGM).
def iniciar_interface(G):
    janela = Tk()
    janela.title("Árvore Geradora Mínima")

    # Carrega a imagem como ícone
    icone = PhotoImage(file='C:\\Users\\ayrto\\AppData\\Roaming\\JetBrains\\PyCharmCE2023.3\\scratches\\img.png')
    janela.iconphoto(False, icone)

    janela.geometry('1000x720')
    janela.configure(bg='#f0f0f0')

    texto_descricao = "Este é um visualizador de grafo, utilizando o algoritmo de kruskal para fazer a árvore geradora mínima."
    label_intro = Label(janela, text=texto_descricao, font=("Arial", 12, "bold"), bg='#f0f0f0', justify='left')
    label_intro.pack(side='top', fill='x', padx=10, pady=10)

    botao = Button(janela, text="Ver Árvore Geradora Mínima", command=lambda: exibir_agm(G), bg='#add8e6', fg='black', padx=10, pady=5)
    botao.pack(side='top', pady=10)

    imagem_rato = PhotoImage(file='C:\\Users\\ayrto\\AppData\\Roaming\\JetBrains\\PyCharmCE2023.3\\scratches\\img_2.png')
    label_imagem_rato = Label(janela, image=imagem_rato, bg='#f0f0f0')
    label_imagem_rato.image = imagem_rato
    label_imagem_rato.pack(side='bottom', anchor='sw', padx=10, pady=10)

    janela.mainloop()

# Chama a função 'criar_grafo' para converter os dados do DataFrame em um objeto de grafo 'G' usando NetworkX, baseando-se nas arestas e pesos definidos nos dados.
if __name__ == "__main__":
    caminho_dados = "C:\\Users\\ayrto\\Downloads\\bn-mouse_visual-cortex_2_updated.csv"
    df = pd.read_csv(caminho_dados)

    G = criar_grafo(df)
    AGM = encontrar_agm(df)

    # Iniciar a interface gráfica
    iniciar_interface(AGM)
