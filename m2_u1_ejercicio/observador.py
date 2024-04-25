import os


class Subject:
    observers = []

    def add_observer(self, obj):
        self.observers.append(obj)

    def substract_observer(self, obj):
        self.observers.remove(obj)

    def notify_observer(self, *args):
        for observer in self.observers:
            observer.update(args)


class Observer:
    def update(self):
        raise NotImplementedError("Delegacion de actualizacion")


class CreateLog:
    # Funcion para guardar un log en un archivo txt
    def observer_log(name, data):
        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(BASE_DIR, "observer_log.txt")
        log_function = open(ruta, "a")
        print(
            f"Resultado del {name} - Se cargaron los siguientes datos:\n",
            data,
            file=log_function,
        )


class ConcreteObserverA(Observer):
    def __init__(self, obj):
        self.obs_a = obj
        self.obs_a.add_observer(self)

    def update(self, *args):
        print("Estas en el observador A")
        print(f"Los parametros son: {args}")
        CreateLog.observer_log("Observador A", args)
