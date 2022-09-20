import scrapy

# Primer de tot he instalat el scrapy amb el pip
# Her creat el projecte StatCovid
# Despres he inspeccionat la url amb el developer tools per identifcar la taula de covid de la que estava interessat
# He creat el arxiu python amb la spider amb el parse 
# Una vegada tinc les dades genero un DICT per exportar-lo amb format CSV

# Tot se m'ha complicat , pero el nom de les files i les columnes també les podria haver tret de la web pero m'ha faltata temps, le he fet manualment


class StatCovidSpider(scrapy.Spider):
    name = "StatCovid"
    custom_settings = {
        'FEED_URI': 'stadisticasCovid.csv',
        'FEED_FORMAT': 'csv'
    }   
    	
    start_urls = [
        "https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176780&menu=ultiDatos&idp=1254735573175"
    ]


    def parse(self, response):
        posind=0
        fil=[1,2,3,4,5,6] # Files de la taula de la web
        col=[2,4,6,8,10,12] # Posició de les columnes del array scrapy
        
        # Defineixo nom de les columnes
        columna = ['','','Total','',"Hombres",'','Mujeres','','Variacion Anual Tot.','','Variacion anual Hombres','','Variacion anual Mujeres']
       
        # Defineixo nom de les files
        fila = ['Total Defunciones','Covid-19 Virus Identificado','Enfermedades Isquemicas y Corazon','Identificado','Enfermedades Cerebrovasculares','Enfermedades Bronquio y Pulmon','Demencia']
       
        # Obtencio dels valors de la taula a la que fem scrap
        valorsStat= response.xpath('//section[contains(@class,"flexwrap")]//table//tbody//tr//td/text()').getall()
        
        # En disposo a generar un dicionari que exportaré a csv amb el yield, tindra nom fila nom columna i valor
        posicion=2
        for i in fil:
            for j in col:
                # paso el valor a float amb control errors
                valorString=valorsStat[posicion]
                valorString=valorString.replace(".","")
                valorString=valorString.replace(",",".")
                try:
                    valorFloat=float(valorString)
                except ValueError:
                    posicion=posicion-1 # quan no tenim valors poso 0 i anem una posició enrera
                    valorFloat=0       
                info= {
                    'Fila': fila[i-1],
                    'Columna' : columna[j],
                    'valor': valorFloat
                }
                yield info
                posicion=posicion+2 #les dades van de 2 en 2 ments quan el valor es nul
            posicion=posicion+1 #al final de cada file hi ha una posició mes
