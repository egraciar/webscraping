# -*- coding: utf-8 -*-

###############################################################################
# Ejercicios prácticos: Práctica WebScraping fin de curso
# Profesor: Pedro Bonillo
# Autor: Enrique Gracia rosuero@gmail.com
# Fecha elaboración ejercicios: 19/01/2024
# Versión: 1.0
# Ejercicio práctico final de curso.
# Documentar código 90%
# Creación de una función 5%
# Publicar código en GitHub 5%
#
###############################################################################

"""
Script que realiza una tarea de web scraping de la página web de noticias de Telemadrid
www.telemadrid.es. El script:
* Obtiene todas las categorías de noticias que existen en la página web
* Obtiene todas las noticias y las almacena en formato CSV en un archivo denominado "noticias.csv".
../data/noticias.csv

"""


# Importación de los módulos necesario para el funcinaiento del scritp

import requests                 # Permite obtener el código HTML de una página web
from bs4 import BeautifulSoup   # Permite extraer datos e información de textos en HTML y XML
from datetime import datetime   # Librería para el trabajo con datos tipo fecha


def procesa_fecha(url_noticia):
    """
    Fucnión que recibe la cadena url_noticia, extrae la fecha de la url y la devuelve en formato
    AAAA-MM-DD
    :param url_noticia:
    :return: fecha_formateada
    """
    # Comenzamos a procesar la fecha. Separamos la url en dos partes.
    # El separador es "--". La parte de la derecha de la URL es la fecha
    lista_fecha = url_noticia.split('--')

    # Pomenos en una variable al cadena de caracteres que forma la fecha y que
    # está en la posición [1] de "lista_fecha"
    fecha_caracteres = lista_fecha[1].replace('.html', '')

    # Formateamos la cadena de caracteres que representa la fecha tomando cada
    # bloque de caracteres y convirtiéndolo a formato fecha.
    fecha_formateada = datetime(int(fecha_caracteres[0:4]),  # Año
                                int(fecha_caracteres[4:6]),  # Mes
                                int(fecha_caracteres[6:8]))  # Día

    # Aplicamos el formato de fecha deseado: YYYY:MM:DD
    fecha_formateada = fecha_formateada.strftime("%Y/%m/%d")

    return fecha_formateada


def webscraping(url_scraping, categoria_scraping='todas'):
    """
    Función que realiza el proceso principal de WebScraping.
    Parámetros de entrada:
        url_scraping: Cadena con la URL de la que se desea hacer el scraping
        param categoria_scraping: Categoría de noticias de la que se desea hacer el scraping
        return: No devuelve nada.
    """
    # URL de de telemadrid
    url = url_scraping

    # Realizar la petición
    try:
        respuesta = requests.get(url)  # Se solicita la URL y el resulatado se almacena en "respuesta"
        # Verificar si la petición fue exitosa (código 200)
        if respuesta.status_code == 200:
            try:
                # Inicialización del archivo CSV.
                with open('../data/noticias.csv', 'w') as f:
                    f.write('titulo,url,categoria,fecha'+'\n')
            except:
                print("ERROR: no se pudo crear el archivo noticias.csv")
            try:
                # Se parsea "respuesta" en modo HTML y se deja el contenido en "soup"
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                try:
                    # Se extraen de "soup" todos las ocurrencias cuyo name sea 'article' y class_ 'card-news'
                    noticias = soup.find_all('article', class_='card-news')
                    if noticias:  # Si noticias no está vacío
                        lista_categorias = []  # Inicializamos la lista de categorías (vacía)

                        # Recorremos todos los artículos de de la lista "noticias"
                        for articulo in noticias:
                            # Procesamos los articulos cuya class_ es "oop-link"
                            try:
                                # Extraemos el título del artículo y se lo asignamos a la variable "titulo"
                                titulo = articulo.find('a', class_='oop-link').text.strip()

                                # Obtenemos a continuacíón la URL de la noticia y se almacena en "url_noticia"
                                url_noticia = articulo.find('a', class_='opp-link')['href']

                                # Procesamos url_noticia separando los componentes de la URL y poniendolos
                                # en una lista (lista_url_noticia)
                                lista_url_noticia = url_noticia.split('/')

                                # Analizamos la lista para extraer la categoría
                                if lista_url_noticia[1] != '':          # Si [1] no está vacío...
                                    categoria = lista_url_noticia[1]    # ... la categoría esta en [1]
                                else:                                   # Si no...
                                    categoria = lista_url_noticia[3]    # ... la categoría está en [3]

                                lista_categorias.append(categoria)      # Añadimos la categoría a la lista

                                # Procesamos la fecha a partir de url_noticia
                                fecha = procesa_fecha(url_noticia)

                                # "Limpiamos" la cadena que contiene el título quitando caracteres no
                                # válidos para el título.
                                titulo = titulo.replace('\'', '').replace('"', '').replace(',', '')

                                # Proceso por el que se graban el el fichero las noticias de la categoría
                                # deseada
                                if categoria_scraping == 'todas':   # Si la categoría elegida es "todas"
                                    try:
                                        # Abrimos el archivo para añadir los datos que hemos obtenido
                                        # previamente: titulo, url_noticia, categoria y fecha
                                        with open('../data/noticias.csv', 'a') as f:
                                            f.write(titulo+','+url_noticia+','+categoria+','+str(fecha)+'\n')
                                    except:
                                        print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                else:                               # Se se ha elegido alguna catetoría
                                    if categoria == categoria_scraping:
                                        # Si la categoría de los datos que tenemos coincdide con la seleccionada
                                        try:
                                            # Abrimos el archivo para añadir los datos que hemos obtenido
                                            # previamente: titulo, url_noticia, categoria y fecha
                                            with open('../data/noticias_'+categoria_scraping+'.csv', 'a') as f:
                                                f.write(titulo + ',' +
                                                        url_noticia + ',' +
                                                        categoria + ',' +
                                                        str(fecha) + '\n')
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                            except:
                                # Procesamos los articulos cuya class_ es "lnk"
                                try:
                                    # Extraemos el título del artículo y se lo asignamos a la variable "titulo"
                                    titulo = articulo.find('a', class_='lnk').text.strip()

                                    # Obtenemos a continuacíón la URL de la noticia y se almacena en "url_noticia"
                                    url_noticia = articulo.find('a', class_='lnk')['href']

                                    # Procesamos url_noticia separando los componentes de la URL y poniendolos
                                    # en una lista (lista_url_noticia)
                                    lista_url_noticia = url_noticia.split('/')

                                    # Analizamos la lista para extraer la categoría
                                    if lista_url_noticia[1] != '':          # Si [1] no está vacío...
                                        categoria = lista_url_noticia[1]    # ... la categoría esta en [1]
                                    else:                                   # Si no...
                                        categoria = lista_url_noticia[3]    # ... la categoría está en [3]

                                    lista_categorias.append(categoria)      # Añadimos la categoría a la lista

                                    # Procesamos la fecha a partir de url_noticia
                                    fecha = procesa_fecha(url_noticia)

                                    # "Limpiamos" la cadena que contiene el título quitando caracteres no
                                    # válidos para el título.
                                    titulo = titulo.replace('\'', '').replace('"', '').replace(',', '')

                                    # Proceso por el que se graban el el fichero las noticias de la categoría
                                    # deseada
                                    if categoria_scraping == 'todas':
                                        try:
                                            # Abrimos el archivo para añadir los datos que hemos obtenido
                                            # previamente: titulo, url_noticia, categoria y fecha
                                            with open('../data/noticias.csv', 'a') as f:
                                                f.write(titulo + ',' +
                                                        url_noticia + ',' +
                                                        categoria + ',' +
                                                        str(fecha) + '\n')
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                    else:
                                        if categoria == categoria_scraping:
                                            try:
                                                # Abrimos el archivo para añadir los datos que hemos obtenido
                                                # previamente: titulo, url_noticia, categoria y fecha
                                                with open('../data/noticias_' + categoria_scraping + '.csv', 'a') as f:
                                                    f.write(titulo + ',' +
                                                            url_noticia + ',' +
                                                            categoria + ',' +
                                                            str(fecha) + '\n')
                                            except:
                                                print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                except:
                                    pass
                        # Eliminamos categorías duplicadas convirtiendo la lista en un conjunto
                        conjunto_categorias = set(lista_categorias)
                    else:
                        print(f"Error La pagina {url} no contiene noticias")
                except:
                    print(f"ERROR: No se pudo encontrar articulos en el codigo html")
            except:
                print(f"ERROR: no se pudo convertir la pagina a codigo html")
        else:
            print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")
    except:
        print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")
    return conjunto_categorias


listado_categorias = webscraping('https://www.telemadrid.es/', 'todas')
seleccion = 'x'
while seleccion != '0':
    print("Lista de categorias: ")
    i = 1
    for opcion in listado_categorias:
        print(f"{i}.- {opcion}")
        i = i + 1
    print("0.- Salir")
    seleccion = input("Por favor seleccione una opcion indicando un numero:")
    categorias_listas = list(listado_categorias)
    categoria_seleccionada = categorias_listas[int(seleccion)-1]
    webscraping('https://www.telemadrid.es/', categoria_seleccionada)
