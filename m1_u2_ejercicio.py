class VerificacionMail:

    def __get__(self, instance, owner):
        return instance._edad

    def __set__(self, instance, valor):
        instance._edad = valor
        print(f"La edad actual: {instance._edad}")

        if instance._edad < 0:
            raise TypeError("El valor de la edad es negativo")
        elif instance._edad == 64:
            print("Esta a un año de jubilarse")


class Empleados:

    def __init__(self, nombre, edad, salario):
        self.nombre = nombre
        self._edad = edad
        self.salario = salario

    edad = VerificacionMail()


empleado1 = Empleados("Juan", 33, 10000)
print(
    f"Empleado: {empleado1.nombre} - Edad: {empleado1._edad} - Salario: {empleado1.salario}"
)
empleado1.edad = 64

try:
    empleado1.edad = -1
except TypeError as e:
    print(e)
