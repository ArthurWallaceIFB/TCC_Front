import io
import os

import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

import scrapy
import scrapy.crawler as crawler
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from multiprocessing import Process, Queue


class IfbSpider(scrapy.Spider):
    name = "ifb_spider"
    start_urls = []

    custom_settings = {
        "DEPTH_LIMIT": 2,
        "DOWNLOAD_DELAY": 0.5,
    }

    accepted_files = ["pdf"]
    allowed_domains = []
    content_element = "#content"

    @classmethod
    def set_spider_params(cls, start_urls, depth_limit, download_delay, accepted_files, allowed_domains, content_element, result_file_path):
        cls.start_urls = start_urls
        cls.custom_settings = {
            "DEPTH_LIMIT": depth_limit,
            "DOWNLOAD_DELAY": download_delay,
        }
        cls.accepted_files = accepted_files
        cls.allowed_domains = allowed_domains
        cls.content_element = content_element
        cls.result_file_path = result_file_path

    def __init__(self, *args, **kwargs):
        super(IfbSpider, self).__init__(*args, **kwargs)
        self.data = []
        self.json_file = open(f"{self.result_file_path}", "w", encoding="utf-8")
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename="scrapy.log",
            format="%(levelname)s: %(message)s",
            level=logging.DEBUG,
        )
    

    def limpar_texto_html(self, html):
        # Use BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html, "html.parser")

        # Remova todas as tags de script e estilo
        for script in soup(["script", "style"]):
            script.extract()

        # Obtenha o texto limpo
        texto_limpo = soup.get_text()

        # Remova espaços em branco em excesso e quebras de linha
        texto_limpo = " ".join(texto_limpo.split())

        return texto_limpo

    def extrair_texto_pdf(self, pdf_content):
        pdf_text = ""
        pdf = PdfReader(io.BytesIO(pdf_content))

        for page in pdf.pages:
            pdf_text += page.extract_text()

        return pdf_text

    def parse(self, response):
        for link in response.css(f"{self.content_element} a::attr(href)").getall():
            if link.startswith("/"):
                link = response.urljoin(link)
            parsed_url = urlparse(link)
            if parsed_url.netloc in self.allowed_domains:
                yield response.follow(link, self.parse_page)

    def parse_page(self, response):
        url = response.url
        print(url)

        # Verifique se a URL termina com uma extensão de arquivo aceita
        if url.endswith(tuple(f".{ext}" for ext in self.accepted_files)):
            # Se for um arquivo PDF, chame a função para extrair texto
            if url.endswith(".pdf"):
                text = self.extrair_texto_pdf(response.body)
                title = os.path.basename(url)
            else:
                text = None

        else:
            content = response.css(self.content_element).get()
            text = self.limpar_texto_html(str(content))
            title = response.css("title::text").get()

        if text and title and url:
            self.data.append(
                {
                    "Title": title,
                    "URL": url,
                    "Content": text,
                }
            )

        # Verifique o nível de profundidade e siga mais links se estiver dentro do limite
        if response.meta["depth"] < self.custom_settings["DEPTH_LIMIT"]:
            for link in response.css(f"{self.content_element} a::attr(href)").getall():
                if link.startswith("/"):
                    link = response.urljoin(link)
                parsed_url = urlparse(link)
                if parsed_url.netloc in self.allowed_domains:
                    yield response.follow(link, self.parse_page)

    def closed(self, reason):
        # Salve os dados em um arquivo JSON
        json.dump(self.data, self.json_file, ensure_ascii=False, indent=4)
        self.json_file.close()




# Função para iniciar o Spider Scrapy

def run_scrapy_chatbot_version(start_urls, depth_limit, download_delay, accepted_files, allowed_domains, content_element, result_file_path):
    def f(q):
        try:
            IfbSpider.set_spider_params(start_urls, depth_limit, download_delay, accepted_files, allowed_domains, content_element, result_file_path)
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(IfbSpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            print("Error in run_scrapy_chatbot_version: ", e)
            q.put(e)

    print("Start Scraping")
    print("Params: ", start_urls, depth_limit, download_delay, accepted_files, allowed_domains, content_element, result_file_path)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

    

# if __name__ == "__main__":
#     from scrapy.crawler import CrawlerProcess

#     process = CrawlerProcess()
#     process.crawl(IfbSpider)
#     process.start()
