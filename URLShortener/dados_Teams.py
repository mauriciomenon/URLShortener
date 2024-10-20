from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configuração do driver do Chrome para reutilizar o perfil do usuário
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Path/To/Your/Chrome/Profile")  # Substituir com o caminho do perfil do Chrome
chrome_options.add_argument("--profile-directory=Default")  # Substituir se você tiver perfis diferentes

# Configurar o driver do Chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL da reunião do Teams
meeting_url = "https://teams.microsoft.com/l/meetup-join/19%3a663835a62f3f4662bf6577467faeb993%40thread.tacv2/1610834377647?context=%7b%22Tid%22%3a%2230b1e5ea-e05e-4a77-99d3-a3c62c328784%22%2c%22Oid%22%3a%227355f150-d4d3-4e4c-9800-bdcedf2ff88c%22%7d"

try:
    # Abrir o navegador e acessar a página da reunião
    driver.get(meeting_url)

    # Usar espera explícita para garantir que a página está carregada
    wait = WebDriverWait(driver, 20)
    
    # Esperar que o título da página seja carregado
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "title")))
    
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
