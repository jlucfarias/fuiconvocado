from datetime import datetime
from bs4 import BeautifulSoup
import requests
import scrapy

class Trt21Spider(scrapy.Spider):
  name = "trt21"
  allowed_domains = ["www.trt21.jus.br"]
  start_urls = ["https://www.trt21.jus.br/legislacao/expedientes?field_expediente_tipo_value=ATO&pesquisa_textual=&ano=2024&mes=all&page=0"]

  def parse(self, response):
    print(response.request.headers)

    if response.status != 200:
      print("Status: {}", response.status)
      print("User agent: {}", response.request.headers['User-Agent'])

      return {
        'success': False,
        'reason': 'Status incorrect'
      }

    soup = BeautifulSoup(response.text, 'html.parser')
    main = soup.find('div', class_='view-ano-mes')

    if main is None:
      print('Main is None')

      return {
        'success': False,
        'reason': 'Main is None'
      }

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

      act_headers = {'User-Agent': response.request.headers['User-Agent']}
      act_response = requests.get(f"https://www.trt21.jus.br{link}", headers=act_headers)
      act_soup = BeautifulSoup(act_response.text, 'html.parser')
      act_main = act_soup.find('article')
      act_text = act_main.find('div', class_="field--text-with-summary")
      nomination = act_text.find('p', string="Nomeado: JOAO LUCAS FARIAS DE ALMEIDA")

      if nomination is None:
        continue

      return {
        'success': True
      }

    print('No nomination')

    return {
      'success': False,
      'reason': 'No nomination'
    }
