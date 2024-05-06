"""
verifica_campos.py:
    Verificacion de datos con un regex especifico.
"""

import re
from datetime import datetime
from record_log import RecordLog


class RegexError(Exception):

    def __init__(self, detalle: str) -> None:
        self.detalle = detalle

    def guardar_error(self) -> None:
        """
        Función que guarda el tipo de error, donde se localizó y la fecha y hora.
        """
        message = (
            datetime.now().strftime("%H:%M:%S--%d/%m/%y")
            + "- Se ingreso mal el dato del "
            + self.detalle
        )
        file_name = "error_log.txt"
        RecordLog().save_log(file_name, message)


class RegexCampos:

    def __init__(self, codigo: str, data: str, funcion: str) -> None:
        self.codigo = codigo
        self.data = data
        self.funcion = funcion

    def verificar(self) -> None:
        """
        Función que controla el cumplimiento de los parámetros enviados en la instancia y
        en caso de no concordancia genera un raise.

        :raises: RegexError
        """
        if not re.match(self.codigo, self.data):
            raise RegexError(self.funcion)
