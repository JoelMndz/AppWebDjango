import re
import xml.etree.ElementTree as ET
from datetime import date

import os


def convertirDate(fecha:str):
    """
    Funcion para convetir una fecha en un date
    """
    datos = fecha.split('/')
    if len(datos) == 3:
        return date(year=int(datos[2]),month=int(datos[1]),day=int(datos[0]))

    return None

def ordenarMensajes(mensajes):
    """
    Funcion para ordenar mensajes por la fecha
    """
    #Aplicamos metodo de ordenamiento por seleccion
    for i in range(len(mensajes)-1):
        indice = i
        minimo = convertirDate(mensajes[i]['fecha'])
        for j in range(i+1,len(mensajes)):
            actual = convertirDate(mensajes[j]['fecha'])
            if minimo > actual:
                minimo = actual
                indice = j
        if indice != i:
            aux = mensajes[i]
            mensajes[i] = mensajes[indice]
            mensajes[indice] = aux

def calcularMensajes(data:dict, fecha:str)-> dict:
    """
    Funcion que cuenta los mensajes positivos, negativos, neutros en una fecha determinada
    """
    conteo = {'total':0,'positivos':0, 'negativos':0, 'neutros':0}

    for i in data['mensajes']:
        if i['fecha'] == fecha:
            #Contamos la cantidad de palabras positivas
            positivas = 0
            for j in data['palabras positivas']:
                if j.lower() in i['texto'].lower():
                    positivas += 1
            #Contamos la cantidad de palabras negativas
            negativas = 0
            for j in data['palabras negativas']:
                if j.lower() in i['texto'].lower():
                    negativas += 1

            #Si el mensaje es positivo
            if positivas > negativas:
                conteo['positivos'] += 1
            elif negativas > positivas:
                conteo['negativos'] += 1
            else:
                conteo['neutros'] += 1

    conteo['total'] = conteo['neutros'] + conteo['negativos'] + conteo['positivos']

    return conteo

def analisisEmpresa(data:dict,fecha):
    """
    Funcion que retorna un analisis con las iteracion de las empresas en la fecha x
    """
    analisis = {}
    for e in data['empresas']:
        conteo = {'total':0,'positivos': 0, 'negativos': 0, 'neutros': 0}
        for i in data['mensajes']:
            # Si la fecha y nombre de la empresa coinciden
            if i['fecha'] == fecha and e['nombre'].lower() in i['texto'].lower():
                # Contamos la cantidad de palabras positivas
                positivas = 0
                for j in data['palabras positivas']:
                    if j.lower() in i['texto'].lower():
                        positivas += 1
                # Contamos la cantidad de palabras negativas
                negativas = 0
                for j in data['palabras negativas']:
                    if j.lower() in i['texto'].lower():
                        negativas += 1

                # Si el mensaje es positivo
                if positivas > negativas:
                    conteo['positivos'] += 1
                elif negativas > positivas:
                    conteo['negativos'] += 1
                else:
                    conteo['neutros'] += 1
        conteo['total'] = conteo['neutros'] + conteo['negativos'] + conteo['positivos']

        if conteo['total'] > 0:
            analisis[e['nombre']] = {'mensajes':conteo,'servicio':{}}
            conteo2 = {'total': 0, 'positivos': 0, 'negativos': 0, 'neutros': 0}
            for i in data['mensajes']:
                # Si la fecha y nombre de la empresa coinciden
                if i['fecha'] == fecha and e['nombre'].lower() in i['texto'].lower():
                    coincide = False
                    #Buscamos coincidencias con el nombre del servicio en el texto del mensaje
                    if e['servicio']['nombre'] in i['texto']:
                        coincide = True
                    #Si no coincide el nombre del servicio buscamos con sus alias
                    if coincide == False:
                        for j in e['servicio']['alias']:
                            if j in i['texto']:
                                coincide = True
                    #Si coincide con el servicio contamos los tipos de mensajes
                    if coincide:
                        # Contamos la cantidad de palabras positivas
                        positivas = 0
                        for j in data['palabras positivas']:
                            if j.lower() in i['texto'].lower():
                                positivas += 1
                        # Contamos la cantidad de palabras negativas
                        negativas = 0
                        for j in data['palabras negativas']:
                            if j.lower() in i['texto'].lower():
                                negativas += 1

                        # Si el mensaje es positivo
                        if positivas > negativas:
                            conteo2['positivos'] += 1
                        elif negativas > positivas:
                            conteo2['negativos'] += 1
                        else:
                            conteo2['neutros'] += 1

                        conteo2['total'] = conteo2['neutros'] + conteo2['negativos'] + conteo2['positivos']
            analisis[e['nombre']]['servicio'] = {'mensajes':conteo2,'nombre':e['servicio']['nombre']}

    return analisis

def analizarSolicitud(root:ET.Element):
    """
    Funcion que analaliza la solicitud que es un objeto XML
    """
    data = {}
    # Obtengo las palabras positivas, negativas
    palabrasPositivas = [i.text.strip() for i in root.findall('diccionario/sentimientos_positivos/')]
    palabrasNegativas = [i.text.strip() for i in root.findall('diccionario/sentimientos_negativos/')]
    etiquetasEmpresa = root.findall('diccionario/empresas_analizar/')
    # Obtengo el nombre de las empresas y el servicio
    empresas = []
    for i in etiquetasEmpresa:
        empresa = {}
        empresa['nombre'] = re.sub(r" +"," ",i.find('nombre').text.strip())
        empresa['servicio'] = {
            'nombre': i.find('servicio').attrib['nombre'],
            'alias': [i.text.strip() for i in i.findall('./servicio/alias')]
        }
        empresas.append(empresa)
    # Obtenemos los mensajes
    etiquetaMensajes = root.findall('lista_mensajes/')
    mensajes = []
    for i in etiquetaMensajes:
        text = i.text.strip()
        # Eliminar saltos de linea y tabulaicones
        text = re.sub(r"[\n\t]", "", text, flags=re.I)
        # Elimnar espacion de más
        text = re.sub(r" +", " ", text, flags=re.I)
        # Obtener los titulos en el texto
        tituloFecha = re.search("lugar y fecha:", text.lower())
        tituloUsuario = re.search("usuario:", text.lower())
        tituloRedSocial = re.search("red social:", text.lower())

        # Diccionario para guardar los datos del mensaje
        mensaje = {}
        # Obtener lugar, fecha y hora
        datos = text[tituloFecha.end():tituloUsuario.start()].strip().split(',')
        mensaje['lugar'] = datos[0].strip()
        fecha = datos[1].strip().split(' ')
        mensaje['fecha'] = fecha[0]
        mensaje['hora'] = fecha[1]
        # Obtener el usuario
        mensaje['usuario'] = text[tituloUsuario.end():tituloRedSocial.start()].strip()
        # Obtener la red social
        datos = text[tituloRedSocial.end():].strip().split(' ')
        mensaje['red social'] = datos[0]
        mensaje['texto'] = ' '.join(datos[1:])

        # Agregar mensajes a la lista
        mensajes.append(mensaje)

    data['palabras positivas'] = palabrasPositivas
    data['palabras negativas'] = palabrasNegativas
    data['empresas'] = empresas
    data['mensajes'] = mensajes

    return data


def responderSolicitud(data:dict) -> ET.Element:
    """
    Funcion que retorna un objeto XML con la respuesta de una solicitud
    """
    root = ET.Element("lista_respuesta")

    #Ordenamos los mensajes
    ordenarMensajes(data['mensajes'])
    #Obtener las fechas sin que se repitan
    fechas = []
    for i in data['mensajes']:
        if i['fecha'] not in fechas:
            fechas.append(i['fecha'])
    for fecha in fechas:
        nodoRespuesta = ET.Element("respuesta")
        #Agregamos el nodo fecha
        nodoFecha = ET.SubElement(nodoRespuesta,"fecha")
        nodoFecha.text = fecha
        #Creamos el nodo mensajes
        nodoMensajes = ET.SubElement(nodoRespuesta,'mensajes')
        #Obtenemos los mensajes con esta fecha
        conteo = calcularMensajes(data,fecha)
        #Agregamos los nodos(total,positivos,negativos,neutros)
        for j in conteo:
            nodo = ET.SubElement(nodoMensajes,j)
            nodo.text = str(conteo[j])

        #Obtnemos el analisis de la empresa
        analisis = analisisEmpresa(data,fecha)
        #Agregamos el analisis de los mensajes y servicios al xml
        nodoAnalisis = ET.SubElement(nodoRespuesta,"analisis")
        for i in analisis:
            nodo1 = ET.SubElement(nodoAnalisis,"empresa")
            nodo1.set('nombre',i)
            nodo2 = ET.SubElement(nodo1, "mensajes")
            for j in analisis[i]['mensajes']:
                nodo3 = ET.SubElement(nodo2,j)
                nodo3.text = str(analisis[i]['mensajes'][j])
            nodo2 = ET.SubElement(nodo1, "servicios")
            nodo3 = ET.SubElement(nodo2, "servicio")
            nodo3.set('nombre', analisis[i]['servicio']['nombre'])
            nodo4 = ET.SubElement(nodo3, "mensajes")
            for j in analisis[i]['servicio']['mensajes']:
                nodo5 = ET.SubElement(nodo4,j)
                nodo5.text = str(analisis[i]['servicio']['mensajes'][j])

        #Agregamos la respuesta a la raiz
        root.append(nodoRespuesta)
    return root

def analizarRespuestas():
    data = []

    archivos = os.listdir('./archivos')
    for filename in archivos:
        root = ET.fromstring(''.join(open(f'archivos/{filename}', encoding='utf-8').readlines()))
        nodos = root.findall('./')
        for i in nodos:
            respuesta = {}
            respuesta['fecha'] = i.find('fecha').text
            respuesta['mensajes'] = {}
            for j in i.findall('./mensajes/'):
                respuesta['mensajes'][j.tag] = int(j.text)
            empresas = {}
            for j in i.findall('./analisis/empresa'):
                mensajes = {}
                servicios = {}
                for k in j.findall('./mensajes/'):
                    mensajes[k.tag] = int(k.text)
                for k in j.findall('./servicios/servicio'):
                    servicios[k.attrib['nombre']] = {}
                    for l in k.findall('./mensajes/'):
                        servicios[k.attrib['nombre']][l.tag] = int(l.text)
                empresas[j.attrib['nombre']] = {'mensajes':mensajes,'servicios':servicios}


            respuesta['empresas'] = empresas
            data.append(respuesta)

    return data
analizarRespuestas()