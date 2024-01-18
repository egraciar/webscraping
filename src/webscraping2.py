import requests
from bs4 import BeautifulSoup

# URL de de telemadrid
url = 'https://www.telemadrid.es/'

# Realizar la petición
try:
    respuesta = requests.get(url)
    #print(respuesta)
    #print(respuesta.text)
    # Verificar si la petición fue exitosa (código 200)
    if respuesta.status_code == 200:
        # Analizar el contenido con BeautifulSoup
        try:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            # print(soup)
            # Aquí puedes realizar operaciones de Web Scraping
            # ...
            try:
                noticias = soup.find_all('article', class_='card-news')
                if noticias:
                    #print(noticias)
                    lista_categorias = []
                    for articulo in noticias:
                        try:
                            titulo = articulo.find('a', class_='oop-link').text.strip()
                            url_noticia = articulo.find('a', class_='opp-link')['href']
                            lista_urlnoticia = url_noticia.split('/')
                            if lista_urlnoticia[1] != '':
                                categoria = lista_urlnoticia[1]
                            else:
                                categoria = lista_urlnoticia[3]
                            lista_categorias.append(categoria)
                        except:
                            try:
                                titulo = articulo.find('a', class_='lnk').text.strip()
                                url_noticia = articulo.find('a', class_='lnk')['href']
                                lista_urlnoticia = url_noticia.split('/')
                                if lista_urlnoticia[1] != '':
                                    categoria = lista_urlnoticia[1]
                                else:
                                    categoria = lista_urlnoticia[3]
                                lista_categorias.append(categoria)
                            except:
                                pass
                    conjunto_categorias = set(lista_categorias)
                    print(conjunto_categorias)
                else:
                    print(f"Error La pagina {url} no contiene noticias")
            except:
                print(f"ERROR: No se pudo encontrar articulos en el codigo html")
        except:
            print(f"ERROR: no se pudo convertir la pagina a codigo html")
    else:
        print(f"Error al obtener la página. Código de estado: {respuesta.status_code}")
except:
    print(f"ERROR: No se puede abrir la pagina {url} o existe un error al procesarla")