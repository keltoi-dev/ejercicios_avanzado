"""
record_log.py:
    Guarda la información recibida en un archivo txt con el nombre que recibe de cada función.
"""

import os


class RecordLog:

    def __init__(self) -> None:
        pass

    def save_log(self, name: str, data: str) -> None:
        """
        Función que establece la ruta, nombre de archivo y guarda la linea correspondiente.
        """
        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(BASE_DIR, "logs", name)
        log_function = open(ruta, "a", encoding="UTF-8")
        print(data, file=log_function)
