
class Error:
    def __init__(self, descripcion, tipo, linea, columna):
        self.descripcion = descripcion
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def __str__(self) -> str:
        return f'Descripcion: {self.descripcion}\nTipo: {self.tipo}\nLinea:{self.linea}\nColumna: {self.columna}'
