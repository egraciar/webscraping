import requests
from bs4 import BeautifulSoup

# URL de ejemplo
url = 'https://www.telemadrid.es/'

try:
    # Realizar la petición
    respuesta = requests.get(url)
    # print(respuesta)
    # print(respuesta.text)

    # Verificar si la petición fue exitosa (código 200)
    if respuesta.status_code == 200:
        # Analizar el contenido con BeautifulSoup
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        # print(soup)
        # Aquí puedes realizar operaciones de Web Scraping
        noticias = soup.find_all('article', class_='card-news')
        if noticias:
            # print(noticias)
            for articulo in noticias:
                try:
                    titulo = articulo.find('a', class_='oop-link').text.strip()
                    url_noticia = articulo.find('a', class_='oop-link')['href']
                    # print(articulo)
                    print(f"Título: {titulo} y la URL: {url_noticia}")
                    # input()
                except:
                    try:
                        titulo = articulo.find('a', class_='lnk').text.strip()
                        url_noticia = articulo.find('a', class_='lnk')['href']
                        print(f"Título: {titulo} y la URL: {url_noticia}")
                    except:
                       pass
        else:
            print(f"ERROR: La página {url} no tiene noticias")

    else:
        print(f"Error al obtener la página. Código de estado: {respuesta.status_code}")
except:
    print(f"Error: no se puede conectar a la página: {url} o existe un error al procesarla")

