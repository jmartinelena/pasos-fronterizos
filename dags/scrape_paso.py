import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_paso(url, timestamp):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    paso_info = {}

    estado_y_actualizacion = soup.find("div", class_="text-muted m-t-3 lead")
    actualizacion = estado_y_actualizacion.get_text("|", strip=True).split("|")[1]
    
    dias, horas, minutos, segundos = re.search(r"(?:(\d+)\s*(?:dia)s?)?\s(?:(\d+)\s*(?:hora)s?)?\s(?:(\d+)\s*(?:minuto)s?)?\s(?:(\d+)\s*(?:segundos)s?)", actualizacion).groups()
    
    dias = int(dias) if dias is not None else 0
    horas = int(horas) if horas is not None else 0
    minutos = int(minutos) if minutos is not None else 0
    segundos = int(segundos) if segundos is not None else 0

    paso_info['estado'] = estado_y_actualizacion.find("span").text
    paso_info['ultima_actualizacion'] = (timestamp - timedelta(days=dias, hours=horas, minutes=minutos, seconds=segundos)).strftime("%Y-%m-%d %H:%M:%S")

    return paso_info