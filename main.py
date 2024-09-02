from xml.dom import minidom
from xml.dom.minidom import Document
import time

class Nodo:
    def __init__(self, nombre, n, m, datos=None):
        self.nombre = nombre
        self.n = n
        self.m = m
        self.datos = datos
        self.siguiente = None

class ListaCircular:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre, n, m, datos=None):
        nuevo_nodo = Nodo(nombre, n, m, datos)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente
            temp.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def buscar_por_indice(self, indice):
        if not self.cabeza:
            return None
        temp = self.cabeza
        for _ in range(indice):
            if temp.siguiente == self.cabeza:
                return None
            temp = temp.siguiente
        return temp

    def buscar(self, nombre):
        if not self.cabeza:
            return None
        temp = self.cabeza
        while True:
            if temp.nombre == nombre:
                return temp
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return None

    def mostrar(self):
        temp = self.cabeza
        if not temp:
            print("Lista circular vacía")
            return
        while True:
            print(f"Matriz: {temp.nombre}, n: {temp.n}, m: {temp.m}")
            fila_temp = temp.datos.cabeza
            for i in range(temp.n):
                fila = ""
                if fila_temp:
                    celda_temp = fila_temp.datos.cabeza
                    for j in range(temp.m):
                        if celda_temp:
                            fila += str(celda_temp.nombre) + " "
                            celda_temp = celda_temp.siguiente
                        else:
                            fila += "0 "
                    print(fila.strip())
                    fila_temp = fila_temp.siguiente
                    if fila_temp == temp.datos.cabeza:
                        break
                else:
                    fila += "0 " * temp.m
                    print(fila.strip())
                    break
            temp = temp.siguiente
            if temp == self.cabeza:
                break

class NodoFila:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class ListaFilas:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre):
        nuevo_nodo = NodoFila(nombre)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente
            temp.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def buscar(self, nombre):
        if not self.cabeza:
            return None
        temp = self.cabeza
        while True:
            if temp.nombre == nombre:
                return temp
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return None

class MatrizBinaria:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = matriz.n
        self.m = matriz.m
        self.nombre = matriz.nombre  # Añadir el nombre de la matriz
        self.datos_binarios = ListaCircular()


    def convertir_a_binaria(self):
        print("Generando patrones de acceso...")
        for i in range(self.n):
            fila_patron = ListaCircular()
            fila = self.matriz.datos.buscar_por_indice(i)
            if fila:
                fila_temp = fila.datos.cabeza
                for j in range(self.m):
                    if fila_temp:
                        valor = int(fila_temp.nombre)
                        valor_patron = "1" if valor > 0 else "0"
                        fila_patron.agregar(valor_patron, 0, 0, None)
                        fila_temp = fila_temp.siguiente
                    else:
                        fila_patron.agregar("0", 0, 0, None)
            else:
                for _ in range(self.m):
                    fila_patron.agregar("0", 0, 0, None)

            self.datos_binarios.agregar("", self.n, self.m, fila_patron)

    def mostrar(self):
        print("Matriz Reducida:")
        temp = self.datos_binarios.cabeza
        if not temp:
            print("Matriz reducida vacía")
            return
        while True:
            fila_temp = temp.datos.cabeza
            fila = ""
            for j in range(self.m):
                if fila_temp:
                    fila += fila_temp.nombre + " "
                    fila_temp = fila_temp.siguiente
                else:
                    fila += "0 "
            print(fila.strip())
            temp = temp.siguiente
            if temp == self.datos_binarios.cabeza:
                break

    def reducir_matriz(self):
        print("Obteniendo matriz reducida...")
        patrones = ListaFilas()
        matriz_reducida = ListaCircular()

        temp = self.matriz.datos.cabeza
        for i in range(self.n):
            fila_temp = temp.datos.cabeza
            patron = ""
            for j in range(self.m):
                if fila_temp:
                    patron += "1" if int(fila_temp.nombre) > 0 else "0"
                    fila_temp = fila_temp.siguiente
                else:
                    patron += "0"
            
            fila_patron = patrones.buscar(patron)
            if fila_patron:
                # Sumar fila
                fila_reducida = matriz_reducida.buscar(fila_patron.nombre)
                if fila_reducida:
                    fila_reducida_temp = fila_reducida.datos.cabeza
                    fila_temp = temp.datos.cabeza
                    for j in range(self.m):
                        if fila_temp and fila_reducida_temp:
                            fila_reducida_temp.nombre = str(int(fila_reducida_temp.nombre) + int(fila_temp.nombre))
                            fila_temp = fila_temp.siguiente
                            fila_reducida_temp = fila_reducida_temp.siguiente
            else:
                # Crear una nueva fila con el patrón
                nueva_fila = ListaCircular()
                fila_temp = temp.datos.cabeza
                for j in range(self.m):
                    if fila_temp:
                        nueva_fila.agregar(fila_temp.nombre, 0, 0, None)
                        fila_temp = fila_temp.siguiente
                    else:
                        nueva_fila.agregar("0", 0, 0, None)
                matriz_reducida.agregar(patron, self.n, self.m, nueva_fila)
                patrones.agregar(patron)

            temp = temp.siguiente
            if temp == self.matriz.datos.cabeza:
                break

        # Actualizar la matriz binaria con la matriz reducida
        self.datos_binarios = matriz_reducida
        print("Matriz reducida generada exitosamente.")

def leer_archivo(ruta):
    doc = minidom.parse(ruta)
    root = doc.documentElement

    matrices = ListaCircular()

    for matriz in root.getElementsByTagName('matriz'):
        nombre = matriz.getAttribute('nombre')
        n = int(matriz.getAttribute('n'))
        m = int(matriz.getAttribute('m'))

        datos = ListaCircular()
        for i in range(n):
            fila = ListaCircular()
            for j in range(m):
                fila.agregar("0", 0, 0, None)
            datos.agregar("", 0, 0, fila)

        for dato in matriz.getElementsByTagName('dato'):
            x = int(dato.getAttribute('x')) - 1
            y = int(dato.getAttribute('y')) - 1
            valor = dato.firstChild.data.strip()
            fila = datos.buscar_por_indice(x)
            if fila:
                celda = fila.datos.buscar_por_indice(y)
                if celda:
                    celda.nombre = valor

        matrices.agregar(nombre, n, m, datos)

    return matrices

def escribir_archivo(matriz_binaria, ruta_salida):
    # Crear un nuevo documento XML
    doc = Document()

    # Crear el nodo raíz <matriz>
    root = doc.createElement('matriz')
    root.setAttribute('nombre', matriz_binaria.nombre)
    root.setAttribute('n', str(matriz_binaria.n))
    root.setAttribute('m', str(matriz_binaria.m))
    doc.appendChild(root)

    # Recorrer la matriz reducida y agregar los elementos <dato>
    fila_actual = matriz_binaria.lista_patrones.cabeza
    while fila_actual is not None:
        for i in range(len(fila_actual.patron.valores)):
            dato = doc.createElement('dato')
            dato.setAttribute('x', str(fila_actual.patron.x))
            dato.setAttribute('y', str(i))
            dato.appendChild(doc.createTextNode(str(fila_actual.patron.valores[i])))
            root.appendChild(dato)

        # Agregar la frecuencia de la fila
        frecuencia = doc.createElement('frecuencia')
        frecuencia.appendChild(doc.createTextNode(str(fila_actual.patron.frecuencia)))
        root.appendChild(frecuencia)

        fila_actual = fila_actual.siguiente

    # Escribir el documento XML a un archivo
    with open(ruta_salida, 'w') as archivo:
        archivo.write(doc.toprettyxml(indent="  "))

    print(f"Archivo XML guardado exitosamente en: {ruta_salida}")


def mostrar_menu():
    print("\nMenú principal:")
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Salida")

# Función principal del programa
def main():
    matrices = None
    matriz_binaria = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Cargar archivo
            ruta = input("Ingrese la ruta completa del archivo de entrada: ")
            matrices = leer_archivo(ruta)
            print("Archivo cargado exitosamente.")
            print("Matrices cargadas:")
            matrices.mostrar()  # Mostrar las matrices cargadas
        elif opcion == '2':
            # Procesar archivo
            if not matrices:
                print("Primero cargue un archivo.")
                continue
            print("Procesar archivo seleccionado.")
            primera_matriz = matrices.cabeza  # Acceder a la primera matriz
            if primera_matriz:
                print(f"Datos de la primera matriz: {primera_matriz.nombre}, n: {primera_matriz.n}, m: {primera_matriz.m}")
                matriz_binaria = MatrizBinaria(primera_matriz)  # Crear una instancia de MatrizBinaria
                matriz_binaria.convertir_a_binaria()  # Convertir la matriz a binaria
                time.sleep(2)
                print("Obteniendo matriz reducida")  # Modificación en el mensaje
                matriz_binaria.reducir_matriz()  # Reducir la matriz
                matriz_binaria.mostrar()  # Mostrar la matriz reducida
            else:
                print("No hay matrices cargadas.")
        elif opcion == '3':
            # Escribir archivo de salida
            if not matriz_binaria:
                print("Primero procese el archivo (opción 2).")
                continue
            ruta_salida = input("Ingrese la ruta completa del archivo de salida: ")
            if not ruta_salida.endswith('.xml'):
                print("Error: La ruta del archivo de salida debe tener la extensión .xml")
                continue
            try:
                escribir_archivo(matriz_binaria, ruta_salida)  # Escribir el archivo XML
                print("Archivo de salida generado exitosamente.")
            except Exception as e:
                print(f"Error al generar el archivo de salida: {e}")
        elif opcion == '4':
            # Mostrar datos del estudiante
            print("Función de mostrar datos del estudiante no implementada.")  # Espacio para agregar esta funcionalidad
        elif opcion == '5':
            # Generar gráfica
            print("Función de generar gráfica no implementada.")  # Espacio para implementar gráficos
        elif opcion == '6':
            # Salir del programa
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
    
