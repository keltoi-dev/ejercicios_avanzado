import os
import socket


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

    def server_log(name, data):
        HOST, PORT = "localhost", 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = str(data) + " - " + name
        sock.sendto(message.encode("UTF-8"), (HOST, PORT))
        received = sock.recvfrom(1024)
        print(received)


class ConcreteObserverA(Observer):
    def __init__(self, obj):
        self.obs_a = obj
        self.obs_a.add_observer(self)

    def update(self, *args):
        print("Estas en el observador A")
        print(f"Los parametros son: {args}")
        CreateLog.observer_log("Observador A", args)


class ConcreteObserverB(Observer):
    def __init__(self, obj):
        self.obs_b = obj
        self.obs_b.add_observer(self)

    def update(self, *args):
        print("Estas en el observador B")
        print(f"Los parametros son: {args}")
        CreateLog.server_log("Observador B", args)
