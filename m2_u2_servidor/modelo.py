"""
modelo.py:
    Modelo de la aplicación - Altas, bajas y modificaciones
"""

from manejo_base import ManageBase, BaseError
from aux_modelo import Auxiliares
from verifica_campos import RegexCampos, RegexError
from datetime import datetime
from observador import Subject
from record_log import RecordLog


# ***** DECORADORES *****
"""
Se implementan decoradores para controlar la ejecución de los métodos de alta, baja y modificación.
Generando una salida por consola y un archivo log.
"""


# Decorador para el metodo alta
def decorador_alta(func) -> list:
    def envelope(*args, **kwargs):
        data = func(*args, **kwargs)
        if isinstance(data, list):
            print("Se ejecuto el metodo de alta")
            funcion_log(func.__name__, data)
        else:
            return data

    return envelope


# Decorador para el metodo baja
def decorador_baja(func) -> list:
    def envelope(*args, **kwargs):
        data = func(*args, **kwargs)
        print("Se ejecuto el metodo de baja")
        funcion_log(func.__name__, data)

    return envelope


# Decorador para el metodo modificar
def decorador_modificacion(func) -> list:
    def envelope(*args, **kwargs):
        data = func(*args, **kwargs)
        print("Se ejecuto el metodo de modificar")
        funcion_log(func.__name__, data)

    return envelope


# Funcion para guardar un log en un archivo txt
def funcion_log(parameter: str, data: list) -> None:

    file_name = "decorator_log.txt"
    message = (
        datetime.now().strftime("%H:%M:%S--%d/%m/%y")
        + f"- Se utilizo el metodo {parameter}"
        + f"\nDatos: {data}\n"
    )
    RecordLog().save_log(file_name, message)


# ***** FUNCIONES PARA ALTAS - BAJAS - MODIFICACIONES *****


class ManageData(Subject):
    def __init__(self, l_status: object, tree: object, aux_vista: object) -> None:
        self.l_status = l_status
        self.tree = tree
        self.aux = Auxiliares()
        self.base = ManageBase()
        self.aux_vista = aux_vista

    # ----- FUNCION ALTA DE REGISTRO -----
    @decorador_alta
    def create_record(self, data: list) -> str:
        """
        Función de alta de los datos capturados en una lista de los campos entry de la vista.
        Verifica que los campos dni, cuil, nombre y apellido no esten vacios.
        Instancia RegexCampos en la variable dni y cuil para control de estos campos.
        Accede al método del ORM para grabar los datos en la tabla de la base sqlite3.
        Actualiza el treeview y vacia los campos entry de la vista.
        En caso de error retorna textos con el detalle del error, de acuerdo al manejo de las excepciones.

        :param data: Lista con la información de los campos
        :type data: list

        :returns: un texto para la información de los message error
        :rtype: string
        """
        self.data = data
        if not self.data[0] or not self.data[1] or not self.data[2] or not self.data[3]:
            self.l_status.config(
                text="Complete todos los campos.", background="#FF5656"
            )
            return "Se deben completar los campos obligatorios."
        else:
            try:
                self.dni = RegexCampos("^\d{7,8}$", self.data[0], "Dni en alta")
                self.cuil = RegexCampos("^\d{11}$", self.data[1], "CUIL en alta")
                self.dni.verificar()
                self.cuil.verificar()

                try:
                    self.base.save_row(data)

                    # LLamado al notificador del observador
                    self.notify_observer(data)

                    self.l_status.config(
                        text="Los datos han sido guardados correctamente.",
                        background="#B9F582",
                    )
                    self.aux.update_treeview(self.tree)
                    self.aux_vista.set_entry([["" for _ in range(11)]])
                    return self.data
                except:
                    BaseError().guardar_error()
                    self.l_status.config(
                        text="El DNI ingresado ya está cargado en la base de datos.",
                        background="#FF5656",
                    )
                    return "El DNI ingresado ya fue cargado."

            except RegexError as log:
                log.guardar_error()
                self.l_status.config(
                    text="Verifique los datos ingresados.", background="#FF5656"
                )
                return "La informacion cargada es incorrecta."

    # ----- FUNCION DE BAJA DE REGISTRO -----
    @decorador_baja
    def delete_record(self, data: list) -> list:
        """
        Funcion de baja de registro seleccionado de la base de datos.
        Recibe la informacion del metodo auxiliar de la vista.
        Llama al metodo del ORM para eliminar la fila de la base de datos.
        Actualiza el treeview e informa en la barra de status la accion.

        :param data: Lista con la informacion de los campos
        :type data: list

        :returns: Una lista vacia para limpieza de los campos
        :rtype: list
        """
        self.data = data
        self.base.delete_row(self.data[0])
        self.aux.update_treeview(self.tree)
        self.l_status.config(
            text="Los datos han sido eliminados correctamente.",
            background="#B9F582",
        )
        self.aux_vista.set_entry([["" for _ in range(11)]])

        return self.data

    # ----- FUNCION DE MODIFICACION DE REGISTROS -----
    @decorador_modificacion
    def modify_record(self, data: list) -> list:
        """
        Funcion para la modificacion del registro seleccionado de la base de datos.
        Los datos los recibe del metodo auxiliar de la vista.
        Llama al metodo del ORM para el update de la fila en la base de datos.

        :param data: Lista con la informacion de los campos
        :type data: list

        :returns: Una lista vacia para limpieza de los campos
        :rtype: list
        """
        self.data = data
        self.base.modify_row(self.data)
        self.l_status.config(
            text="Los datos han sido modificados correctamente.",
            background="#B9F582",
        )
        self.aux.update_treeview(self.tree)
        self.aux_vista.set_entry([["" for _ in range(11)]])

        return self.data
