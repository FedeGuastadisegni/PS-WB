# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy_crawler.items import AutorItem, PublicacionItem
from scrapy.linkextractors import LinkExtractor

class crawler(scrapy.Spider):
	name = "crawler"
	

	start_urls = [#"http://www.sac.org.ar/argentine-cardiology-journal-archive",
					#"http://rinfi.fi.mdp.edu.ar/xmlui/recent-submissions?offset=",
					#"http://road.issn.org/issn_search?afs:query=&show-adv=0&afs:replies=100#.VqaLtl4oDtR",
					#"http://www.intechopen.com/books/latest/1/list",
					#"http://eprints.internano.org",
					"http://nparc.cisti-icist.nrc-cnrc.gc.ca/npsi/ctrl"]
					#"http://eprints.bbk.ac.uk/view/subjects/csis.html",
					#"http://canterbury33.eprints-hosting.org/view/subjects/QA75.html",
					#"http://www.repository.heartofengland.nhs.uk/view/subjects/WK.html"]
					#"http://bdh.bne.es/bnesearch/Search.do"]
					#"http://binpar.caicyt.gov.ar/cgi-bin/koha/opac-detail.pl?biblionumber=98723&query_desc="]

	

	def parse(self, response):
		url3 = "http://road.issn.org/issn_search?afs:query=&show-adv=0&afs:replies=100#.VqaLtl4oDtR"
		yield scrapy.Request(url3,callback=self.parse_web2)

		


	

	def parse_web0(self, response): #http://www.sac.org.ar/argentine-cardiology-journal/
	# Observaciones: Funciona, pero el ISBN se repite porque es el unico que hay en la pagina. Por lo tanto, es el unico que concuerda con el Regex.
		i=0
		for sel in response.xpath("//ul[@class='d3s-revista']"):
			publicaciones = sel.xpath("//li[contains(p, 'Scientific Letters')]/p[@class='d3s-titulo-post']/text()").extract()
			autores = sel.xpath("//li[contains(p, 'Scientific Letters')]/p[@class='d3s-titulo-autores']/text()").extract()
			links = sel.xpath("////li[contains(p, 'Scientific Letters')]/a[contains(@href,'.pdf')]/@href").extract()
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = response.xpath("//p[@class='d3s-titulo-numero']/text()").re(r'\d\d\d\d')[0].strip()
					publicacion['isbn'] = response.xpath("//div[@id='d3s-page-content']/div/div/div/text()").re(r'\d\d\d\d-\d\d\d\d')[0].strip()
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = links[o]
					yield publicacion
					o+=1
				i+=1 
		
	def parse_web1(self, response): #http://rinfi.fi.mdp.edu.ar/xmlui/recent-submissions?offset=0/20/40
	# Observaciones: Funciona, y trae de las tres paginas. Problema: Las publicaciones estan en dos tipos distintos de Xpath (hay 20 por pagina, esta sacando 10 por pagina)
	# Puede parecer que repite el año, pero son todas de 2014. El isbn esta dentro del PDF, decidi poner un Null.
		i=0
		for sel in response.xpath("//div[@id='ds-main']/div[@id='ds-content-wrapper']/div[@id='ds-content']/div[@id='ds-body']"):
			publicaciones = sel.xpath("//div[@id='ds-body']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_main-recent-submissions']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_recent-submissions']/ul[@class='ds-artifact-list']/li[@class='ds-artifact-item odd' or @class='ds-artifact-item even']/div[@class='artifact-description']/div[@class='artifact-title']/a/text()").extract()
			#publicaciones = sel.xpath("//div[@id='ds-body']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_main-recent-submissions']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_recent-submissions']/ul[@class='ds-artifact-list']/li[@class='ds-artifact-item even']/div[@class='artifact-description']/div[@class='artifact-title']/a/text()").extract()
			autores = sel.xpath("//div[@id='ds-main']/div[@id='ds-content-wrapper']/div[@id='ds-content']/div[@id='ds-body']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_main-recent-submissions']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_recent-submissions']/ul[@class='ds-artifact-list']/li[@class='ds-artifact-item odd']/div[@class='artifact-description']/div[@class='artifact-info']/span[@class='author']/span/text()").extract()
			links = sel.xpath("//div[@id='ds-main']/div[@id='ds-content-wrapper']/div[@id='ds-content']/div[@id='ds-body']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_main-recent-submissions']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_recent-submissions']/ul[@class='ds-artifact-list']/li[@class='ds-artifact-item odd']/div[@class='artifact-description']/div[@class='artifact-title']/a/@href").extract()
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = (response.xpath("//div[@id='ds-main']/div[@id='ds-content-wrapper']/div[@id='ds-content']/div[@id='ds-body']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_main-recent-submissions']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_recent-submissions']/ul[@class='ds-artifact-list']/li[@class='ds-artifact-item odd']/div[@class='artifact-description']/div[@class='artifact-info']/span[@class='publisher-date']/span[@class='date']/text()").re(r'\d\d\d\d')[0].strip())
					publicacion['isbn'] = "Null"
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = "http://rinfi.fi.mdp.edu.ar"+ links[o]
					yield publicacion
					o+=1
				i+=1
		

	def parse_web2(self, response): #http://road.issn.org/issn_search?afs:query=&show-adv=0&afs:replies=100#.VrO8GF4oDtT
	# Observaciones: Trae todo. Por cuestiones de similitud, en esta pagina, el año va a tener que quedar con formato aaaa/mm/dd
		i=0
		for sel in response.xpath("//div[@class='page-container']/div[@class='page']/div[@id='main-content']/div[@class='main-content-inside']/div[@class='region-content']/div[@class='issn-search']/div[@class='search-results']/div[@class='search-result type-journals']"):
			publicaciones = sel.xpath("//div[@class='page-container']/div[@class='page']/div[@id='main-content']/div[@class='main-content-inside']/div[@class='region-content']/div[@class='issn-search']/div[@class='search-results']/div[@class='search-result type-journals']/div[@class='search-result-title']/a/text()").extract()
			#publicaciones = sel.xpath("//div[@id='ds-body']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_main-recent-submissions']/div[@id='aspect_discovery_recentSubmissions_RecentSubmissionTransformer_div_recent-submissions']/ul[@class='ds-artifact-list']/li[@class='ds-artifact-item even']/div[@class='artifact-description']/div[@class='artifact-title']/a/text()").extract()
			autores = sel.xpath("//div[@class='page-container']/div[@class='page']/div[@id='main-content']/div[@class='main-content-inside']/div[@class='region-content']/div[@class='issn-search']/div[@class='search-results']/div[@class='search-result type-journals']/div[@class='search-result-publisher']/text()").extract()
			links = sel.xpath("//div[@class='page-container']/div[@class='page']/div[@id='main-content']/div[@class='main-content-inside']/div[@class='region-content']/div[@class='issn-search']/div[@class='search-results']/div[@class='search-result type-journals']/div[@class='search-result-title']/a/@href").extract()
			anios = response.xpath("//div[@class='page-container']/div[@class='page']/div[@id='main-content']/div[@class='main-content-inside']/div[@class='region-content']/div[@class='issn-search']/div[@class='search-results']/div[@class='search-result type-journals']/div[@class='search-result-registration_year']").re(r'\d\d\d\d-\d\d-\d\d')
			isbns = response.xpath("//div[@class='page-container']/div[@class='page']/div[@id='main-content']/div[@class='main-content-inside']/div[@class='region-content']/div[@class='issn-search']/div[@class='search-results']/div[@class='search-result type-journals']/div[@class='search-result-issn']").re(r'\d+-\d+')
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = anios[o]
					publicacion['isbn'] = isbns[o]
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = links[o]
					yield publicacion
					o+=1
				i+=1
	
	
	def parse_web3(self, response): #http://www.intechopen.com/books/latest/1/list itera sobre todas las paginas.
	# Observaciones: cambios en el while: cambie la forma en la que el año y el ISBN se obtienen. Ahora, son arrays como los demas elementos. Esto evita que se guarden duplicados
		i=0
		for sel in response.xpath("//div[@id='sizer']/div[@id='content']/div[@class='grid']/div[@class='main-content']/div[@id='tc']/div/ul[@class='book-listing entity-listing']/li"):
			publicaciones = sel.xpath("//div[@id='sizer']/div[@id='content']/div[@class='grid']/div[@class='main-content']/div[@id='tc']/div/ul[@class='book-listing entity-listing']/li/dl/dt/a/text()").extract() #publicacion
			autores = response.xpath("//div[@id='sizer']/div[@id='content']/div[@class='grid']/div[@class='main-content']/div[@id='tc']/div/ul[@class='book-listing entity-listing']/li/dl/dd[@class='meta']/text()[count(preceding-sibling::br) = 0]").re(r'Editor\s*(.*)') #FUNCIONA!
			links = sel.xpath("//div[@id='sizer']/div[@id='content']/div[@class='grid']/div[@class='main-content']/div[@id='tc']/div/ul[@class='book-listing entity-listing']/li/dl/dt/a/@href").extract() #links
			anios = response.xpath("//div[@id='sizer']/div[@id='content']/div[@class='grid']/div[@class='main-content']/div[@id='tc']/div/ul[@class='book-listing entity-listing']/li/dl/dd[@class='meta']/text()").re(r' \d\d\d\d')
			isbns = response.xpath("//div[@id='sizer']/div[@id='content']/div[@class='grid']/div[@class='main-content']/div[@id='tc']/div/ul[@class='book-listing entity-listing']/li/dl/dd[@class='meta']/text()").re(r'\d\d\d-\d\d\d-\d\d-\d\d\d\d-\d')
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = anios[o]
					publicacion['isbn'] = isbns[o]
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = "http://www.intechopen.com"+links[o]
					yield publicacion
					o+=1
				i+=1	


	def parse_web4(self, response): #http://eprints.internano.org/
	# Observaciones: todo funciona bien.
		i=0
		for sel in response.xpath("//div[@id='wrapper']/div[@id='shadow']/div[@id='box']/div"):
			publicaciones = sel.xpath("//div[@id='wrapper']/div[@id='shadow']/div[@id='box']/div/div[@class='ep_tm_page_content']/div[@class='ep_latest_additions']/div[@class='ep_latest_list']/div[@class='ep_latest_result']/a/em/text()").extract() #publicacion
			autores = response.xpath("//div[@id='wrapper']/div[@id='shadow']/div[@id='box']/div/div[@class='ep_tm_page_content']/div[@class='ep_latest_additions']/div[@class='ep_latest_list']/div[@class='ep_latest_result']/span[@class='person_name']/text()").extract() #Autor
			links = sel.xpath("//div[@id='wrapper']/div[@id='shadow']/div[@id='box']/div/div[@class='ep_tm_page_content']/div[@class='ep_latest_additions']/div[@class='ep_latest_list']/div[@class='ep_latest_result']/a/@href").extract()
			anios = response.xpath("//div[@id='wrapper']/div[@id='shadow']/div[@id='box']/div/div[@class='ep_tm_page_content']/div[@class='ep_latest_additions']/div[@class='ep_latest_list']/div[@class='ep_latest_result']/text()").re(r'\((\d\d\d\d)\)')
			isbns = response.xpath("//div[@id='wrapper']/div[@id='shadow']/div[@id='box']/div/div[@class='ep_tm_page_content']/div[@class='ep_latest_additions']/div[@class='ep_latest_list']/div[@class='ep_latest_result']/text()").re(r'\d+-\d+|\w+-\w+')
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = anios[o]
					publicacion['isbn'] = isbns[o]
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = links[o]
					yield publicacion
					o+=1
				i+=1
	
	def parse_web5(self, response): #Cisti
		i=0
		for sel in response.xpath("//div[@class='page']/div[@class='core']/div[@class='colLayout']/div[@class='center']/div[@id='content-container-3col']"):
			publicaciones = sel.xpath("//div[@class='page']/div[@class='core']/div[@class='colLayout']/div[@class='center']/div[@id='content-container-3col']/div[@class='paddRecent']/div[@class='table-row widthFull']/span[@class='boldFont']/a/text()").extract() #publicacion
			autores = response.xpath("//div[@class='page']/div[@class='core']/div[@class='colLayout']/div[@class='center']/div[@id='content-container-3col']/div[@class='paddRecent']/div[@class='table-row widthFull forceWordWrap']/a/text()").extract() #Autor
			links = sel.xpath("//div[@class='page']/div[@class='core']/div[@class='colLayout']/div[@class='center']/div[@id='content-container-3col']/div[@class='paddRecent']/div[@class='table-row widthFull']/span[@class='boldFont']/a/@href").extract()
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = 2016
					publicacion['isbn'] = "1059-9630"
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = "http://nparc.cisti-icist.nrc-cnrc.gc.ca"+links[o]
					yield publicacion
					o+=1
				i+=1


	def parse_web6(self, response): #http://eprints.bbk.ac.uk/view/subjects/csis.html
	#Observaciones: Funciona bien, pero la publicacion en la base va a tener solo un autor. Cuestiones de diseño.
		
		# Cada publicacion esta en un <p>. Hago el for sobre ellos.
		for publication in response.css('div > div.ep_tm_page_content > div.ep_view_page.ep_view_page_view_subjects > p'):

			# Cada publicacion tiene un <a> donde se encuentra el titulo y el Link.
			for title in publication.xpath('./a'):
				pubtitle = title.xpath('normalize-space(.)').extract_first()
				publink = title.xpath('@href').extract_first()
				break
			# Aplico Regex para sacar el Año entre los parentesis
			pubyear = publication.xpath('./text()').re_first(r'\((\d+)\)')

			# Obtengo los autores. Me devuelve un array, pero no lo puedo guardar asi en la base, y como no encontre solucion, decidi guardar uno solo.
			author = publication.xpath('./span[@class="person_name"][./following-sibling::a]/text()').extract()

			# Obtengo el numero luego de ISBN o ISSN. Si no hay nada, devuelve NULL
			isxn = publication.xpath('./a/following-sibling::text()').re_first(r'(ISBN\s+\d+|ISSN\s+\d+-\d+)')
			
			publicacion = PublicacionItem()
			publicacion['titulo_publicacion'] = pubtitle
			publicacion['anio_publicacion'] = pubyear 
			publicacion['isbn'] = isxn
			publicacion['nombre_autor'] = author[0]
			publicacion['url_link'] = publink
			yield publicacion
			
	
	def parse_web7(self, response): #christ church
		i=0	
		for sel in response.xpath("//div[@id='ExtContainer']/div[@id='ExtWrapper']/div[@id='ExtBody']/div[@id='ExtMainContent']"):
			publicaciones = sel.xpath("//div[@id='ExtContainer']/div[@id='ExtWrapper']/div[@id='ExtBody']/div[@id='ExtMainContent']/div[@class='ep_view_page ep_view_page_view_subjects']/p/a/em/text()").extract() #publicacion
			autores = response.xpath("//div[@id='ExtContainer']/div[@id='ExtWrapper']/div[@id='ExtBody']/div[@id='ExtMainContent']/div[@class='ep_view_page ep_view_page_view_subjects']/p/span[@class='person_name']/text()").extract() #Autor
			links = sel.xpath("//div[@id='ExtContainer']/div[@id='ExtWrapper']/div[@id='ExtBody']/div[@id='ExtMainContent']/div[@class='ep_view_page ep_view_page_view_subjects']/p/a/@href").extract()
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = response.xpath("//div[@id='ExtContainer']/div[@id='ExtWrapper']/div[@id='ExtBody']/div[@id='ExtMainContent']/div[@class='ep_view_page ep_view_page_view_subjects']/p").re(r'\d\d\d\d')[0].strip() #Fecha, ultimos cuatro digitos.
					publicacion['isbn'] = response.xpath("//div[@id='ExtContainer']/div[@id='ExtWrapper']/div[@id='ExtBody']/div[@id='ExtMainContent']/div[@class='ep_view_page ep_view_page_view_subjects']/p").re(r'\d\d\d\d-\d\d\d\d')[0].strip()
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = links[o]
					yield publicacion
					o+=1
				i+=1	
			
	def parse_web8(self, response): #Repository UK
		i=0
		for sel in response.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']"):
			publicaciones = sel.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']/p/a/em/text()").extract() #publicacion
			autores = response.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']/p/span[@class='person_name']/text()").extract() #Autor
			links = sel.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']/p/a/@href").extract()
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = response.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']/p").re(r'\d\d\d\d')[0].strip() #Fecha, ultimos cuatro digitos.
					publicacion['isbn'] = response.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']/p").re(r'\d\d\d\d-\d\d\d\d')[0].strip()
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = links[o]
					yield publicacion
					o+=1
				i+=1
	
'''	def parse_web9(self, response): #search.Do
		i=0
		for sel in response.xpath("//div/div[@class='ep_tm_page_content']/div[@class='ep_view_page ep_view_page_view_subjects']"):
			publicaciones = sel.xpath("//div[@id='wrapper']/div[@id='content']/div[@id='div1']/div[@id='results']/div[@id='lista']/div[@class='entrada']/div[@class='details']/h2/a[@class='LabelBlueBold']/text()").extract() #publicacion
			autores = response.xpath("//div[@id='wrapper']/div[@id='content']/div[@id='div1']/div[@id='results']/div[@id='lista']/div[@class='entrada']/div[@class='details']/span[@class='dato'][1]/b/text()").extract() #Autor
			links = sel.xpath("//div[@id='wrapper']/div[@id='content']/div[@id='div1']/div[@id='results']/div[@id='lista']/div[@class='entrada']/div[@class='details']/h2/a[@class='LabelBlueBold']/@href").extract()
			if i == 0:
				o=0
				while o != len(publicaciones):
					publicacion = PublicacionItem()
					publicacion['titulo_publicacion'] = publicaciones[o]
					publicacion['anio_publicacion'] = response.xpath("//div[@id='wrapper']/div[@id='content']/div[@id='div1']/div[@id='results']/div[@id='lista']/div[@class='entrada']/div[@class='details']/span[@class='dato'][3]/b/text()").re(r'\d\d\d\d')[0].strip() #Fecha, ultimos cuatro digitos.
					publicacion['isbn'] = "NULL"
					gsub('\t|\n', '', autores[o])
					print(autores[o])
					raw_input()
					publicacion['nombre_autor'] = autores[o]
					publicacion['url_link'] = "http://bdh.bne.es"+links[o]
					yield publicacion
					o+=1
				i+=1'''#tarda demasiado tiempo.


				