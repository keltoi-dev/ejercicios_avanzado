"""
observador.py:
    Observador constante de la funcion de alta de la aplicación.
"""

from record_log import RecordLog


class Subject:
    observers = []

    def add_observer(self, obj: object) -> None:
        """
        Adiciona los observadores instanciados en el controlador en una lista.

        :param obj: de la clase que pide su incorporacion a la lista
        """
        self.observers.append(obj)

    def substract_observer(self, obj: object) -> None:
        """
        Elimina de la lista a un observadore instanciado.

        :param obj: de la clase que pide su eliminacion a la lista
        """
        self.observers.remove(obj)

    def notify_observer(self, *args: list) -> None:
        """
        Envia a informar lo recolectado por cada observador en la lista.

        :param args: Lista
        """
        for observer in self.observers:
            observer.update(args)


class Observer:
    def update(self):
        raise NotImplementedError("Delegacion de actualizacion")


class ConcreteObserverA(Observer):
    def __init__(self, obj: object) -> None:
        self.obs_a = obj
        self.obs_a.add_observer(self)

    def update(self, *args: list) -> None:
        """
        Toma los datos recolectado por el observador, los muestra por terminal y los guarda en un archivo txt

        :param args: Lista
        """
        print("Estas en el observador A")
        print(f"Los parametros son: {args}")
        file_name = "observer_log.txt"
        message = (
            f"Resultado del Observador A - Se cargaron los siguientes datos:\n{args}"
        )
        RecordLog().save_log(file_name, message)
