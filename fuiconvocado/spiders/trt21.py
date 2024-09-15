from datetime import datetime
from bs4 import BeautifulSoup
import requests
import scrapy


class Trt21Spider(scrapy.Spider):
  name = "trt21"
  allowed_domains = ["www.trt21.jus.br"]
  start_urls = ["https://www.trt21.jus.br/legislacao/expedientes?field_expediente_tipo_value=ATO&pesquisa_textual=&ano=2024&mes=all&page=0"]

  def parse(self, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    main = soup.find('div', class_='view-ano-mes')
    table = main.find('table')
    body = table.find('tbody')
    acts = body.findAll('tr')
    now = datetime.now()
    today = now.date()

    for act in acts:
      date = act.find('td', headers="view-field-expediente-data-table-column").text.strip()
      link = act.find('td', headers="view-title-table-column").find('a')['href']

      if datetime.strptime(date, "%d/%m/%Y").date() != today:
        continue

      act_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
      act_response = requests.get(f"https://www.trt21.jus.br{link}", headers=act_headers)
      act_soup = BeautifulSoup(act_response.text, 'html.parser')
      act_main = act_soup.find('article')
      act_text = act_main.find('div', class_="field--text-with-summary")
      nomination = act_text.find('p', string="Nomeado: JOAO LUCAS FARIAS DE ALMEIDA")

      if nomination is None:
        continue

    pass
