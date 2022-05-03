from src.modelo.error import Error
from src.modelo.token import Token


class AnalizadorLexico:
    def __init__(self):
        self.tokens = []
        self.errores = []

    def analizarXML(self, cadena: str):
        #Boorrar informacion
        self.tokens = []
        self.errores = []

        # variables
        linea = 1
        columna = 0
        buffer = ''
        estado = 'SIGNO'

        #Iterar sobre cada caracter
        for caracter in cadena.strip():
            if estado == 'SIGNO':
                if caracter == '<':
                    buffer = caracter
                    self.tokens.append(Token(buffer, 'MENOR QUE', linea, columna))
                    buffer = ''
                    estado = 'ETIQUETA'
                    columna += 1
                elif caracter.isalnum():
                    columna += 1
                    buffer = caracter
                    estado = 'CADENA'
                elif caracter == '\t' or caracter == ' ':
                    columna += 1
                elif caracter == '\n':
                    linea += 1
                    columna = 0
                else:
                    self.errores.append(Error(caracter + " no reconocido como token.", 'LEXICO', linea, columna))
                    buffer = ''
                    columna += 1
            elif estado == 'ETIQUETA':
                if caracter == '>':
                    self.tokens.append(Token(buffer, 'ETIQUETA', linea, columna))
                    buffer = ''
                    estado = 'SIGNO'
                    columna += 1

                    self.tokens.append(Token(caracter, 'MAYOR QUE', linea, columna))
                    columna += 1
                elif caracter == '/':
                    self.tokens.append(Token(buffer, 'ETIQUETA', linea, columna))
                    buffer = ''
                    estado = 'ETIQUETA'
                    columna += 1

                    self.tokens.append(Token(caracter, 'BARRA', linea, columna))
                    columna += 1
                else:
                    buffer += caracter
                    columna += 1
            elif estado == 'CADENA':
                if caracter == '<':
                    self.tokens.append(Token(buffer, 'CADENA', linea, columna))
                    buffer = ''
                    estado = 'ETIQUETA'
                    columna += 1

                    self.tokens.append(Token(caracter, 'MENOR QUE', linea, columna))
                    columna += 1
                else:
                    buffer += caracter
                    columna += 1

    def obtenerInformacion(self):
        data = {}
        if len(self.tokens) > 0:
            None
        return data

xml = """
<mensajes>
 <total> 3 </total>
 <positivos> 1 </positivos>
 <negativos> 1 </negativos>
 <neutros> 1 </neutros>
 </mensajes>
"""

a = AnalizadorLexico()
a.analizarXML(xml)
for i in a.tokens:
    print('*'*30)
    print(i)
