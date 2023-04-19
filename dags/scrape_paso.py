import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

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

    media_bodies = soup.find_all("div", class_="media-body")
    
    info_general = media_bodies[0]
    info_general_ps = info_general.find_all("p")
    paso_info['pais'] = info_general_ps[0].get_text("|", strip=True).split("|")[1]
    paso_info['provincia'] = info_general_ps[1].get_text("|", strip=True).split("|")[1]

    info_cruce = media_bodies[2]
    info_cruce_ps = info_cruce.find_all("p")
    
    info_cruce_dict = {}

    for p in info_cruce_ps:
        key = p.get_text("|", strip=True).split("|")[0][:-1]
        key = key.lower().replace(" ","_")
        value = p.get_text("|", strip=True).split("|")[1]
        
        if value[:-2].isdigit():
            value = int(value[:-2])
        
        info_cruce_dict[key] = value

    keys = ['tipo_de_paso', 'temperatura', 'tiempo', 'viento', 'visibilidad', 'altura_del_río', 'alerta', 'evacuación']

    for key in keys:
        paso_info[key] = info_cruce_dict.get(key, None)

    return paso_info