import random

from algoritmo_contagem import contar_inversoes
from dados import RANKING_BRASIL_TOP_15

def apresentar_e_obter_ranking_usuario(lista_de_musicas):

    print("--- Analisador de Gosto Musical: Meu Spotify Vibe ---")
    print("Abaixo estão as 15 músicas mais tocadas no Brasil.")
    print("Ordene-as de acordo com a sua preferência!\n")

    # Mapeia cada música ao seu número (posição)
    mapa_musica_para_posicao = {musica: i + 1 for i, musica in enumerate(lista_de_musicas)}
    
    musicas_para_exibir = list(lista_de_musicas)
    random.shuffle(musicas_para_exibir) # Embaralha para não enviesar a resposta do usuário

    for musica in musicas_para_exibir:
        posicao_oficial = mapa_musica_para_posicao[musica]
        print(f"{posicao_oficial}: {musica}")

    print("\nDigite os números de 1 a 15 na sua ordem de preferência, separados por espaço.")
    ranking_usuario_str = input("Sua ordem: ")

    try:
        ranking_numerico = [int(num) for num in ranking_usuario_str.split()]
        
        # Validacaoo simples 
        if len(ranking_numerico) != len(lista_de_musicas) or len(set(ranking_numerico)) != len(lista_de_musicas):
            print("\nErro: Entrada inválida. Por favor, insira todos os 15 números de 1 a 15, sem repetição.")
            return None
            
        return ranking_numerico
    except ValueError:
        print("\nErro: Entrada inválida. Use apenas números separados por espaço.")
        return None

def analisar_e_mostrar_resultado(inversoes, total_de_itens):
    """
    Calcula a similaridade e exibe o feedback final para o usuário.
    """
    # O pior caso (ranking totalmente invertido) tem n*(n-1)/2 inversões.
    maximo_de_inversoes = total_de_itens * (total_de_itens - 1) / 2
    
    # Converte o número de inversões em uma porcentagem de similaridade.
    similaridade = 100 * (1 - (inversoes / maximo_de_inversoes))

    print("\n--- Resultado da Análise ---")
    print(f"Número de 'discordâncias' (inversões) com o ranking Brasil: {inversoes}")
    print(f"Seu gosto musical é {similaridade:.2f}% similar ao Top 15 do Brasil!")

    if similaridade >= 80:
        print("Veredito: Você está super em alta! Seu gosto é totalmente mainstream.")
    elif similaridade >= 50:
        print("Veredito: Você tem um gosto equilibrado, curte os hits mas tem suas próprias preferências.")
    else:
        print("Veredito: Você definitivamente tem um gosto alternativo e único!")

def iniciar_programa():
    """
    Função principal que orquestra a execução da aplicação.
    """
    # obter o ranking do usuário.
    ranking_do_usuario = apresentar_e_obter_ranking_usuario(RANKING_BRASIL_TOP_15)
    
    if ranking_do_usuario:
        
        num_inversoes = contar_inversoes(ranking_do_usuario)
        
        # result
        analisar_e_mostrar_resultado(num_inversoes, len(RANKING_BRASIL_TOP_15))


if __name__ == "__main__":
    iniciar_programa()