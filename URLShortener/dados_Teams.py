from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Configuração do driver do Chrome para reutilizar o perfil do usuário
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Path/To/Your/Chrome/Profile")  # Substituir com o caminho do perfil do Chrome
chrome_options.add_argument("--profile-directory=Default")  # Substituir se você tiver perfis diferentes

# Configurar o driver do Chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL da reunião do Teams
meeting_url = "https://teams.microsoft.com/l/meetup-join/19%3Ameeting_NWQ5MmUyZWQtMjIwYy00YzU1LWE4YmUtZDA3NjM4OTU2MDg1%40thread.v2/0?context=%7B%22Tid%22%3A%223590422d-8e59-4036-9245-d6edd8cc0f7a%22%2C%22Oid%22%3A%22fe62638f-2f4f-41cc-b20f-dc91c9c4250d%22%7D"

try:
    # Abrir o navegador e acessar a página da reunião
    driver.get(meeting_url)
    
    # Aguardar alguns segundos para a página carregar completamente
    time.sleep(10)  # Ajustar conforme necessário ou substituir por esperas explícitas

    # Extrair o conteúdo da página
    page_source = driver.page_source

    # Usar BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extrair o título da reunião
    title = soup.find('title').text.strip() if soup.find('title') else 'Título não encontrado'
    
    # Exemplo para buscar o horário da reunião - ajustar conforme a estrutura real da página
    # Aqui estamos assumindo que a hora pode estar em um elemento específico
    time_info = soup.find('div', class_='some-time-class')  # Ajuste a classe ou tag correta
    time_str = time_info.text.strip() if time_info else 'Horário não encontrado'

    # Exibir as informações extraídas
    print(f"Título da Reunião: {title}")
    print(f"Horário da Reunião: {time_str}")

finally:
    # Fechar o navegador
    driver.quit()
