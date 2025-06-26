def contar_inversoes(lista):
    """
    inicia a contagem de inversões em uma lista

    Args:
        lista (list): Uma lista de números a ser analisada

    Returns:
        int: O número total de inversões na lista.
    """
    # Cria uma cópia da lista original
    _, total_de_inversoes = _ordenar_e_contar_recursivo(list(lista))
    return total_de_inversoes


def _ordenar_e_contar_recursivo(sub_lista):
    """
    divide a lista recursivamente e soma as inversões de cada parte

    Args:
        sub_lista (list): A lista a ser ordenada e analisada.

    Returns:
        tuple: Uma tupla contendo (lista_ordenada, numero_de_inversoes).
    """
    # Caso base: uma lista já está ordenada e tem 0 inversões
    if len(sub_lista) <= 1:
        return sub_lista, 0

    # DIVIDIR
    meio = len(sub_lista) // 2
    metade_esquerda = sub_lista[:meio]
    metade_direita = sub_lista[meio:]

    # Chamada recursiva para cada metade.
    esquerda_ordenada, inversoes_na_esquerda = _ordenar_e_contar_recursivo(metade_esquerda)
    direita_ordenada, inversoes_na_direita = _ordenar_e_contar_recursivo(metade_direita)

    # Intercala as duas metades já ordenadas e conta as inversões de quebra
    lista_final_ordenada, inversoes_de_quebra = _intercalar_e_contar(esquerda_ordenada, direita_ordenada)

    # Soma as inversões de todas as fontes
    total_inversoes = inversoes_na_esquerda + inversoes_na_direita + inversoes_de_quebra
    
    return lista_final_ordenada, total_inversoes


def _intercalar_e_contar(metade_esquerda, metade_direita):
    """
    Intercala duas sub-listas já ordenadas, criando uma lista maior e ordenada.
    É aqui que as inversões "de quebra" (split inversions) são contadas.

    Args:
        metade_esquerda (list): Sub-lista da esquerda, já ordenada
        metade_direita (list): Sub-lista da direita, já ordenada

    Returns:
        tuple: Uma tupla contendo (lista_intercalada, inversoes_de_quebra).
    """
    lista_intercalada = []
    inversoes_de_quebra = 0
    
    ponteiro_esquerda, ponteiro_direita = 0, 0

    # Percorre as duas metades enquanto houver elementos nelas
    while ponteiro_esquerda < len(metade_esquerda) and ponteiro_direita < len(metade_direita):
        # Se o elemento da esquerda é menor, apenas o adicionamos ao resultado.
        if metade_esquerda[ponteiro_esquerda] <= metade_direita[ponteiro_direita]:
            lista_intercalada.append(metade_esquerda[ponteiro_esquerda])
            ponteiro_esquerda += 1
        else:
            # Se o elemento da direita é menor, o adicionamos -> INVERSÃO!
            lista_intercalada.append(metade_direita[ponteiro_direita])
            ponteiro_direita += 1
            
            # O elemento da direita é menor que TODOS os elem restantes na lista da esquerda. Contamos todos
            elementos_restantes_na_esquerda = len(metade_esquerda) - ponteiro_esquerda
            inversoes_de_quebra += elementos_restantes_na_esquerda

    # Adiciona os elementos que sobraram 
    lista_intercalada.extend(metade_esquerda[ponteiro_esquerda:])
    lista_intercalada.extend(metade_direita[ponteiro_direita:])
    
    return lista_intercalada, inversoes_de_quebra