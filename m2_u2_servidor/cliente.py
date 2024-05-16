"""
cliente.py:
    Aplicacion cliente para consulta al servidor.
"""

from tkinter import Tk
from tkinter import Menu, Label, Button, Frame
from tkinter import StringVar, Entry
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel
import os
import socket
import re

__author__ = "German Fraga"
__maintainer__ = "German Fraga"
__email__ = "gdfraga@gmail.com"
__copyright__ = "Copyright 2024"
__version__ = "0.0.1"


class MasterWindow:
    def __init__(self, window: object) -> None:
        self.window = window

        """
        Se dibuja un menú con solo el Acerca de... con la información de la aplicación.
        Construye una ventana principal con un frame. Esta ventana contiene también el título y la barra de estado.
        El frame engloba a todas las cajas de entrada para mostrar la información recuperada de la base de datos.
        En la parte inferior estan los botones para la limpieza de los campos y salir de la aplicación.
        """

        # ----- DECLARACION DE TEXTO PARA VENTANA ACERCA DE ... -----
        info = """
                Aplicación para el cliente. Consulta un número
                de dni al servidor y recibe toda la informacion
                correspondiente.
                
                AUTOR: Germán Fraga

                Entrega final - Diplomatura Python 3
                Nivel avanzado.
                Paradigama de Programación Orientada a Objetos,
                patrón observador, decoradores, socket, etc.
                04/05/2024
                """

        # Construccion de la ventana principal
        self.window.title("Aplicación cliente - Python Avanzado")
        self.window.resizable(False, False)
        ruta = os.getcwd() + os.sep + "img" + os.sep
        self.window.iconbitmap(ruta + "python.ico")

        menubar = Menu(self.window, relief="solid")
        menubar.add_cascade(
            label="Acerca de ...", command=lambda: showinfo("Acerca de ...", info)
        )
        self.window.config(menu=menubar)

        Label(
            self.window,
            text="GESTION DE NOMINA DE EMPLEADOS - CLIENTE",
            bg="#B9F582",
            font="Bold",
        ).grid(row=0, column=0, columnspan=2, sticky="w" + "e")

        # ----- DEFINICIONN DE VARIABLES -----
        self.var_dni, self.var_cuil = StringVar(), StringVar()
        self.var_nombre, self.var_apellido, self.var_domicilio = (
            StringVar(),
            StringVar(),
            StringVar(),
        )
        self.var_fnacimiento, self.var_falta = StringVar(), StringVar()
        self.var_obra, self.var_art = StringVar(), StringVar()
        self.var_jornal, self.var_filtro = StringVar(), StringVar()

        # ===== FRAMES =====

        # ----- FRAME DE DATOS -----
        frame_datos = Frame(self.window, padx=10, pady=10, bd=1, relief="solid")
        frame_datos.grid(row=1, column=0)

        # ===== LABELS =====

        Label(frame_datos, text="INFORMACION DEL EMPLEADO", font="Bold").grid(
            row=0, column=0, columnspan=6, pady=10, sticky="we"
        )

        Label(frame_datos, text="D.N.I.").grid(row=1, column=0, sticky="w")
        Label(frame_datos, text="C.U.I.L").grid(row=1, column=4, sticky="e")
        Label(frame_datos, text="NOMBRES").grid(row=2, column=0, sticky="w")
        Label(frame_datos, text="APELLIDOS").grid(row=3, column=0, sticky="w")
        Label(frame_datos, text="DOMICILIO").grid(row=4, column=0, sticky="w")
        Label(frame_datos, text="FECHA DE NAC.").grid(row=5, column=0, sticky="w")
        Label(frame_datos, text="FECHA DE ALTA").grid(row=5, column=4, sticky="e")
        Label(frame_datos, text="OBRA ASIGNADA").grid(row=6, column=0, sticky="w")
        Label(frame_datos, text="ART o SEGURO").grid(row=7, column=0, sticky="w")
        Label(frame_datos, text="JORNAL $").grid(row=8, column=0, sticky="w")
        Label(
            frame_datos,
            text="* En el campo DNI solo ingrese números sin ',' o '.'.",
            fg="#ff1b1b",
        ).grid(row=9, column=1, columnspan=6, sticky="w")

        # ----- LABEL DE STATUS -----
        self.l_status = Label(self.window, text="Ok.", bg="#B9F582")
        self.l_status.grid(row=4, column=0, columnspan=2, sticky="w" + "e")

        widget_2 = WidgetsWindows(frame_datos)
        widget_1 = WidgetsWindows(window)

        # ===== BUTTONS =====

        widget_1.boton_1(
            "LIMPIAR",
            lambda: self.set_entry(["" for _ in range(11)]),
            2,
            0,
        )
        widget_1.boton_1(
            "SALIR",
            lambda: self.close_app(),
            3,
            0,
        )

        widget_2.boton_2(
            "CONSULTAR",
            lambda: self.consult_server(self.var_dni.get()),
            1,
        )

        # ===== ENTRYS =====
        e_dni = Entry(frame_datos, textvariable=self.var_dni, width=15, borderwidth=0)
        e_dni.grid(row=1, column=1)
        e_cuil = Entry(
            frame_datos,
            textvariable=self.var_cuil,
            width=15,
            borderwidth=0,
            state="readonly",
        )
        e_cuil.grid(row=1, column=5)
        e_nombre = Entry(
            frame_datos,
            textvariable=self.var_nombre,
            width=80,
            borderwidth=0,
            state="readonly",
        )
        e_nombre.grid(row=2, column=1, columnspan=5)
        e_apellido = Entry(
            frame_datos,
            textvariable=self.var_apellido,
            width=80,
            borderwidth=0,
            state="readonly",
        )
        e_apellido.grid(row=3, column=1, columnspan=5)
        e_direccion = Entry(
            frame_datos,
            textvariable=self.var_domicilio,
            width=80,
            borderwidth=0,
            state="readonly",
        )
        e_direccion.grid(row=4, column=1, columnspan=5)
        e_fnacimiento = Entry(
            frame_datos,
            textvariable=self.var_fnacimiento,
            width=15,
            borderwidth=0,
            state="readonly",
        )
        e_fnacimiento.grid(row=5, column=1)
        e_falta = Entry(
            frame_datos,
            textvariable=self.var_falta,
            width=15,
            borderwidth=0,
            state="readonly",
        )
        e_falta.grid(row=5, column=5)
        e_obra = Entry(
            frame_datos,
            textvariable=self.var_obra,
            width=80,
            borderwidth=0,
            state="readonly",
        )
        e_obra.grid(row=6, column=1, columnspan=5)
        e_art = Entry(
            frame_datos,
            textvariable=self.var_art,
            width=80,
            borderwidth=0,
            state="readonly",
        )
        e_art.grid(row=7, column=1, columnspan=5)
        e_jornal = Entry(
            frame_datos,
            textvariable=self.var_jornal,
            width=15,
            borderwidth=0,
            state="readonly",
        )
        e_jornal.grid(row=8, column=1)

    def consult_server(self, var_dni: str) -> None:
        """
        Función que lanza la consulta al servidor y recibe la informacion completa del empleado.

        :param var_dni: Valor ingresado en el campo dni
        :type var_dni: string
        """

        if re.match("^\d{7,8}$", var_dni):
            try:
                HOST, PORT = "127.0.0.1", 9999
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                message = str(var_dni)
                sock.sendto(message.encode("UTF-8"), (HOST, PORT))
                received = sock.recvfrom(1024)
                data_list = eval(received[0].decode("UTF-8"))
                if data_list[1] != "":
                    self.set_entry(data_list)
                else:
                    self.l_status.config(
                        text="El dni seleccionado no existe en la base de datos.",
                        background="#FF5656",
                    )
            except socket.timeout:
                self.l_status.config(
                    text="El servidor no esta conectado.", background="#FF5656"
                )
        else:
            self.l_status.config(
                text="Complete correctamente el campo dni.", background="#FF5656"
            )

    def set_entry(self, data: list) -> None:
        """
        Esta función se utiliza para la carga de la información, consultada al servidor, en todos los entrys.
        También se le puede enviar una lista vacia para poder limpiar todos los campos.

        :param data_list: La lista con toda la información a cargar o vacia para limpiar
        :type data_list: list[str, int]
        """

        self.var_dni.set(data[1])
        self.var_cuil.set(data[2])
        self.var_nombre.set(data[3])
        self.var_apellido.set(data[4])
        self.var_domicilio.set(data[5])
        self.var_fnacimiento.set(data[6])
        self.var_falta.set(data[7])
        self.var_obra.set(data[8])
        self.var_art.set(data[9])
        self.var_jornal.set(data[10])

        self.l_status.config(text="Ok.", background="#B9F582")

    # ----- FUNCION DE CIERRE DE LA APLICACION -----
    def close_app(self) -> None:
        """
        Función para el cierre de la aplicación, con una ventana emergente que consulta si está seguro de esta operación.
        """
        option = askokcancel("Cerrar la aplicación", "¿Está seguro que quiere salir?")
        if option:
            self.window.destroy()


class WidgetsWindows(MasterWindow):
    def __init__(self, frame: object) -> None:
        self.frame = frame

    def boton_1(self, text_btn: str, instruction: str, x: int, y: int) -> None:
        """
        Objeto para generar botones de tkinter.

        :param text_btn: Texto del botón
        :type text_btn: string
        :param instruction: Función lambda para ejecutar desde el botón
        :type instruction: string
        :param x: Valor de la fila del botón
        :type x: integer
        :param y: Valor de la columna del botón
        :type y: integer
        """
        self.text_btn = text_btn
        self.instruction = instruction
        self.x = x
        self.y = y
        self.btn = Button(
            self.frame,
            text=self.text_btn,
            width=15,
            command=self.instruction,
            borderwidth=0.5,
        )
        self.btn.grid(row=self.x, column=self.y, padx=2, pady=9)

    def boton_2(self, text_btn: str, instruction: str, position: int) -> None:
        """
        Objeto para generar botones grises de tkinter.

        :param text_btn: Texto del botón
        :type text_btn: string
        :param instruction: Función lambda para ejecutar desde el botón
        :type instruction: string
        :param position: Valor de la fila del botón
        :type position: integer
        """
        self.text_btn = text_btn
        self.instruction = instruction
        self.position = position
        btn_buscar = Button(
            self.frame,
            text=self.text_btn,
            width=12,
            bg="#a1a1a1",
            command=self.instruction,
            borderwidth=0,
        )
        btn_buscar.grid(row=self.position, column=2, sticky="w")


if __name__ == "__main__":
    root = Tk()
    # Instancia de la ventana
    view = MasterWindow(root)
    root.mainloop()
