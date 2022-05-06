from flask import request
import xml.etree.ElementTree as ET
import shortuuid
import os

from src.ayuda import analizarSolicitud, responderSolicitud, analizarRespuestas


def solicitud(request:request):
    """
    Funcion que recibe en el request un archivo.xml
    """
    if request.files['archivo']:
        file = request.files['archivo']
        if file.content_type == 'application/xml':
            filename = 'temporal.xml'
            file.save(filename)
            #Lo convierto un arbol de xml
            root = ET.fromstring(''.join(open(filename,encoding='utf-8').readlines()))
            try:
                #Analizamos el xml
                data = analizarSolicitud(root)
                #Realizar respuesta
                respuesta = responderSolicitud(data)
                #Guardamos la respuesta en un archivo
                arbol = ET.ElementTree(respuesta)
                arbol.write('ultimaConsulta.xml')
                arbol.write(f'archivos/{shortuuid.uuid()}.xml')
                return ET.tostring(respuesta, encoding='unicode', method='xml')
            except Exception as e:
                root = ET.Element("error")
                nodo = ET.SubElement(root, 'mensaje')
                nodo.text = e
                return ET.tostring(root, encoding='unicode', method='xml')
    root = ET.Element("error")
    nodo = ET.SubElement(root,'mensaje')
    nodo.text = "No ha enviado el archivo XML"
    return ET.tostring(root, encoding='unicode', method='xml')

def consulta():
    """
    Funcion que retorna el ultimo archivo devuelto
    :return:
    """
    root = ET.fromstring(''.join(open('ultimaConsulta.xml', encoding='utf-8').readlines()))
    return ET.tostring(root, encoding='unicode', method='xml')

def calsificacionFecha(empresa, fecha):
    data = analizarRespuestas()
    if len(data) > 0:
        None
    root = ET.Element("error")
    nodo = ET.SubElement(root, 'mensaje')
    nodo.text = "No hay datos"
    return ET.tostring(root, encoding='unicode', method='xml')