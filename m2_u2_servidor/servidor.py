"""
servidor.py
    Objeto servidor que estable la comunicacion con los clientes.
"""

import socketserver
from manejo_base import ManageBase
from record_log import RecordLog


global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        """
        Función para recibir las solicitudes de los clientes, dar una respuesta a estas y
        dejar registro de actividad en un archivo txt.
        """
        base = ManageBase()

        data = self.request[0].strip()
        socket = self.request[1]

        indice = data.decode("UTF-8")
        print("Se recibe para consultar el siguiente dni:", indice)

        try:
            data_list = base.search_one(indice)
            message = str(data_list[0]).encode("UTF-8")
            print(type(message))
        except:
            data_list = ["" for _ in range(11)]
            message = str(data_list).encode("UTF-8")
        finally:
            print("se envia la siguiente información:", message)
            socket.sendto(message, self.client_address)

            message = f"Se recibe para consultar el siguiente dni: {indice}\nDireccion IP: {self.client_address}"
            file_name = "server_log.txt"
            RecordLog().save_log(file_name, message)


if __name__ == "__main__":
    HOST, PORT = "localhost", 456
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
