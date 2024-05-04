import socketserver

global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        log_errors = open("server_log.txt", "a")
        print(data.decode("UTF-8"), file=log_errors)
        print("Se recibe la informacion y se guarda en server_log.txt")
        print(data)

        message = "Actualizado el log del servidor"
        socket.sendto(message.encode("UTF-8"), self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
