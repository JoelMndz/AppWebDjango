
class Token:
    def __init__(self, lexema, tipo, linea, columna):
        self.lexema = lexema
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f'Lexema: {self.lexema}\nTipo: {self.tipo}\nLinea:{self.linea}\nColumna: {self.columna}'

