import streamlit as st
from algoritmo_contagem import contar_inversoes
from scraper_kworb import raspar_top_15
import random

# página inicial
st.set_page_config(
    page_title="Music Ranking Comparison",
    page_icon="🎵",
    layout="centered"
)

# Aqui garante que o scraping só será feito uma vez
@st.cache_data
def carregar_dados():
    """Carrega os dados do ranking uma única vez."""
    return raspar_top_15()

def analisar_similaridade(ranking_usuario, ranking_oficial):
    """Calcula a similaridade e retorna os resultados formatados."""
    total_de_itens = len(ranking_oficial)
    # 1. Mapear cada música para sua posição oficial no ranking
    mapa_posicao_oficial = {musica: i + 1 for i, musica in enumerate(ranking_oficial)}
    
    # 2. Converter o ranking do usuário (lista de strings) para uma lista de números
    ranking_numerico_usuario = [mapa_posicao_oficial[musica] for musica in ranking_usuario]
    
    # 3. Calcular as inversões
    inversoes = contar_inversoes(ranking_numerico_usuario)
    
    # 4. Calcular o índice de similaridade
    max_inversoes = total_de_itens * (total_de_itens - 1) / 2
    similaridade_percentual = 100 * (1 - (inversoes / max_inversoes))
    
    return inversoes, similaridade_percentual

# Feedback da similaridade do gosto musical do usuário.
def get_feedback_similaridade(similaridade):
    """Retorna uma mensagem amigável baseada na porcentagem de similaridade."""
    if similaridade >= 80:
        return "Veredito: Gêmeos musicais! 🎶 Você está super alinhado com as tendências do Brasil.", "success"
    elif similaridade >= 50:
        return "Veredito: Bom gosto! Você curte os hits, mas também tem suas próprias pérolas escondidas.", "info"
    elif similaridade >= 20:
        return "Veredito: Alma alternativa! Seu gosto é único e se destaca da multidão.", "warning"
    else:
        return "Veredito: Totalmente contra a maré! Você é um verdadeiro vanguardista musical.", "error"


# Criação da interface
st.title("🎵 Music Ranking Comparison")
st.markdown("### Compare seu gosto musical com o Top 15 do Brasil!")
st.write("---")

# Carrega os dados usando a função com cache
ranking_oficial = carregar_dados()


if not ranking_oficial:
    st.error("Não foi possível carregar o ranking do kworb.net. Por favor, tente recarregar a página mais tarde.")
else:
    st.info("**Instrução:** Clique na caixa abaixo e selecione as músicas na sua ordem de preferência, da 1ª à 15ª.")

    lista_embaralhada = list(ranking_oficial)
    
    random.shuffle(lista_embaralhada)

    #Estrutura que permite o usuário selecionar as músicas que ele queira.
    ranking_usuario = st.multiselect(
        label="**Monte seu ranking aqui:**",
        options=lista_embaralhada,
        placeholder="Selecione sua música favorita...",
        label_visibility="visible"
    )


    # Apresenta ao usuário a ordem que ele selecionou.
    if ranking_usuario:
        st.markdown("---")
        st.write("**Sua ordem atual:**")
        # O 'enumerate' cria a numeração 1º, 2º, 3º...
        for i, musica in enumerate(ranking_usuario):
            st.markdown(f"&nbsp;&nbsp;&nbsp;`{i+1}º` - {musica}")

    st.write("---")
    
    # botão para iniciar o cálculo
    if st.button("Calcular Similaridade", type="primary"):
        if len(ranking_usuario) != len(ranking_oficial):
            st.warning(f"Por favor, selecione todas as {len(ranking_oficial)} músicas para fazer a comparação.")
        else:
            
            with st.spinner('Analisando as vibes... 🤖'):
                inversoes, similaridade = analisar_similaridade(ranking_usuario, ranking_oficial)
                
                # aqui mostra resultados
                st.subheader("🎉 Seu Resultado!")

                col1, col2 = st.columns(2)
                col1.metric(label="Índice de Similaridade", value=f"{similaridade:.1f}%")
                col2.metric(label="Nº de 'Discordâncias' (inversões)", value=f"{inversoes}")

                feedback_texto, feedback_tipo = get_feedback_similaridade(similaridade)
                
                if feedback_tipo == "success":
                    st.success(feedback_texto)
                elif feedback_tipo == "info":
                    st.info(feedback_texto)
                elif feedback_tipo == "warning":
                    st.warning(feedback_texto)
                else:
                    st.error(feedback_texto)