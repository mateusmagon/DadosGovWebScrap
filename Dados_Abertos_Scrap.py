# rodar no prompt de comando com local_do_arquivo py>scrapy runspider nome_do_arquivo.py  -o testeScrap.csv
# Desenvolvido por Mateus Magon em 15/11/2019
# Scrapy 1.8.0
# Python 3.7.4
# Extrai informações dos dados abertos do Ministério da Saúde catalogados no site dados.gov.br

# importa o framework Scrapy
import scrapy

#lista vazia que será utilizada para limpeza do campo de títulos mais à frente
lista_titulos=[]

#chama a classe de funções e nomeia o crawler
class DadosGovSpider(scrapy.Spider):
    name = 'main-spider'
    
    # função que  faz a conexão com a primeira página do MS e cria um objeto response que contém todos os seus dados
    def start_requests(self):
        urls = ['http://dados.gov.br/organization/ministerio-da-saude-ms']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
    #função que busca os links e as páginas que contém os metadados sobre as bases de dados publicadas 
    def parse(self, response):
        self.log("Eu estou aqui {}".format(response.url))
        
        #cria uma lista com todos os links nos títulos das bases de dados
        links = response.xpath('//*[@id="content"]/div/div/article/div/ul/li/div/h3/a/@href').extract()

        #segue os links encontrados
        for link in links:
            yield response.follow(url = link, callback = self.parse2)

        #faz a mesma coisa, só que com as páginas
        pages = response.xpath('//*[@id="content"]/div[3]/div/article/div/div/ul/li/a/@href').extract()
        for page in pages:
            yield response.follow(url = page, callback = self.parse)
    #cria listas a partir da extração dos dados do objeto response
    def parse2(self, response):

        
        self.log("Eu estou aqui {}".format(response.url))
        titulos = response.xpath('//*[@id="content"]/div[3]/div/article/div/h1/text()').extract()
        last_atual = response.xpath('//*[@id="content"]/div[3]/div/article/div/section[3]/table/tbody/tr[4]/td/span/text()').extract()
        criado = response.xpath('//*[@id="content"]/div[3]/div/article/div/section[3]/table/tbody/tr[5]/td/span/text()').extract()
        fonte =  response.xpath('//*[@id="content"]/div[3]/div/article/div/section[3]/table/tbody/tr[1]/td/a/text()').extract()
        autor =  response.xpath('//*[@id="content"]/div[3]/div/article/div/section[3]/table/tbody/tr[2]/td[@property="dc:creator"]//text()').extract()
        mantenedor = response.xpath('//*[@id="content"]/div[3]/div/article/div/section[3]/table/tbody/tr[3]/td[@property ="dc:contributor"]//text()').extract()
        licenca = response.xpath('//*[@* = "dc:rights"]/text()').extract()

        #faz a limpeza no campo 'titulos', que apresentava espaços e quebras de parágrafo
        for titulo in titulos:
            titulo_limpo = str(titulo).replace('\n','').strip()
            lista_titulos.append(titulo_limpo)


        #retorna a criação de um dicionário que será utilizado pelo próprio Scrapy para gerar um arquivo csv (executar no prompt de comando 'local_do_arquivo>scrapy runspider nomedoarquivo.py  -o nomedoarquivo.csv'(Scrapy e Python devem estar          instalados no ambiente)
        
        yield{
            'Base de dado': titulo_limpo,
            'Última Atualização' : last_atual,
            'Criado em': criado,
            'Fonte': fonte,
            'Autor':autor,
            'Mantenedor': mantenedor,
            'Licença': licenca

        }
