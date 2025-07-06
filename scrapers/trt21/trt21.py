import datetime
from io import StringIO
from lxml import etree
from urllib.parse import urlencode
from requests import get as fetch

class Trt21Scrapper():
  full_name = "Tribunal Regional do Trabalho da 21ª Região"
  name = "TRT 21"
  slug = "trt-21"
  base_url = "https://www.trt21.jus.br"
  list_path = "legislacao/expedientes"
  params = {
    "tipo": 1,
    "numero": "",
    "situacao": "vigente_preto",
    "origem": "TRT21-GP",
    "pesquisa_textual": "Concurso Público de Servidores",
    "ano": "2025",
    "mes": "all",
  }
  headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Brave\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
  }

  def __call__(self) -> bool:
    params = urlencode(self.params)
    url = f"{self.base_url}/{self.list_path}?{params}"
    response = fetch(url, headers=self.headers)

    if not response.ok:
      return False

    content = response.content.decode("utf-8")
    parser = etree.HTMLParser()
    document = etree.parse(StringIO(content), parser=parser)
    items = document.xpath("/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div/div/table/tbody/tr/td[@headers=\"view-field-expediente-data-table-column\"]")
    list_items = []

    for index, item in enumerate(items):
      date = datetime.datetime.strptime(item.text.strip(), "%d/%m/%Y").date()
      anchor = item.getparent().xpath(f"//tr[{index + 1}]/td[1]/a")[0]
      path = anchor.get("href")
      item = Trt21Entry(path, date)
      list_items.append(item)

    # TODO: filter based on last update
    for entry in list_items:
      entry_url = f"{self.base_url}/{entry.path}"
      entry_response = fetch(entry_url, headers=self.headers)

      if not entry_response.ok:
        continue

      entry_content = entry_response.content.decode("utf-8")
      entry_document = etree.parse(StringIO(entry_content), parser=parser)
      wrapper = entry_document.xpath("/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div/div/div/div/span/div/ul/li[9]")[0]
      nominees = wrapper.xpath("//*[contains(text(), \"Nomeado\")]")
      has_user_nomination = False

      for nominee in nominees:
        name = nominee.text.lstrip("Nomeado: ").lstrip("Nomeada: ").strip()

        if name.lower().replace("ã", "a") != "joao lucas farias de almeida":
          continue

        has_user_nomination = True

    return has_user_nomination

class Trt21Entry():
  def __init__(self, path: str, date: datetime.date):
    self.path = path
    self.date = date

  def __str__(self):
    return f"<scrapers.trt21.trt21.Trt21Entry link:{self.path} date:{self.date}>"
