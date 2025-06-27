import requests
from bs4 import BeautifulSoup

def raspar_top_15():
    """
    Usa requests e BeautifulSoup para extrair o Top 15 do site kworb.net.
    Esta versão inclui a correção para o encoding de caracteres (UTF-8).
    """
    URL = "https://kworb.net/spotify/country/br_daily.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print("Buscando o ranking mais recente...")
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        response.encoding = 'utf-8'

        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tabela = soup.find('table', id='spotifydaily')
        corpo_tabela = tabela.find('tbody')
        
        linhas = corpo_tabela.find_all('tr')
        
        ranking_raspado = []
        for linha in linhas[:15]:
            celula_musica = linha.find('td', class_='text')
            texto_completo = celula_musica.text.strip()
            ranking_raspado.append(texto_completo)
            
        print("Ranking obtido com sucesso!")
        return ranking_raspado

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao acessar a página: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o scraping: {e}")
        return None

# aq so para caso rodar direto esse arquivo
if __name__ == "__main__":
    top_15 = raspar_top_15()
    if top_15:
        print("\n--- TOP 15 MÚSICAS DO BRASIL (KWROB.NET) ---")
        for i, musica in enumerate(top_15):
            print(f"{i+1}. {musica}")