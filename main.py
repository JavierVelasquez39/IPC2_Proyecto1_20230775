from xml.dom import minidom
from xml.dom.minidom import Document
import time
from os import startfile, system
import unicodedata
import re

def normalizar_nombre(nombre):
    # Eliminar acentos y caracteres especiales
    nombre_normalizado = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('ASCII')
    # Reemplazar caracteres no alfanuméricos por guiones bajos
    nombre_normalizado = re.sub(r'[^a-zA-Z0-9_]', '_', nombre_normalizado)
    return nombre_normalizado

class Nodo:
    def __init__(self, nombre, n, m, datos=None):
        self.nombre = nombre
        self.n = n
        self.m = m
        self.datos = datos
        self.siguiente = None

class NodoGrupo:
    def __init__(self, patron, grupo):
        self.patron = patron
        self.grupo = grupo
        self.siguiente = None

class ListaGrupos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, patron, grupo):
        nuevo_nodo = NodoGrupo(patron, grupo)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente
            temp.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def buscar(self, patron):
        if not self.cabeza:
            return None
        temp = self.cabeza
        while True:
            if temp.patron == patron:
                return temp
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return None

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

class NodoFrecuencia:
    def __init__(self, patron, frecuencia):
        self.patron = patron
        self.frecuencia = frecuencia
        self.siguiente = None

class ListaFrecuencias:
    def __init__(self):
        self.cabeza = None

    def agregar(self, patron, frecuencia):
        nuevo_nodo = NodoFrecuencia(patron, frecuencia)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente
            temp.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def buscar(self, patron):
        if not self.cabeza:
            return None
        temp = self.cabeza
        while True:
            if temp.patron == patron:
                return temp
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return None

    def contar(self):
        if not self.cabeza:
            return 0
        temp = self.cabeza
        count = 0
        while True:
            count += 1
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return count

    def mostrar(self):
        temp = self.cabeza
        if not temp:
            print("Lista de frecuencias vacía")
            return
        while True:
            print(f"Patrón: {temp.patron}, Frecuencia: {temp.frecuencia}")
            temp = temp.siguiente
            if temp == self.cabeza:
                break

class MatrizBinaria:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = matriz.n
        self.m = matriz.m
        self.nombre = matriz.nombre
        self.datos_binarios = ListaCircular()
        self.patrones = ListaFilas()
        self.frecuencias = ListaFrecuencias()

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

    def reducir_matriz(self):
        print("Obteniendo matriz reducida...")
        matriz_reducida = ListaCircular()
        filas_unicas = 0

        temp = self.matriz.datos.cabeza
        for i in range(self.matriz.n):  
            fila_temp = temp.datos.cabeza
            patron = ""
            for j in range(self.m):
                if fila_temp:
                    patron += "1" if int(fila_temp.nombre) > 0 else "0"
                    fila_temp = fila_temp.siguiente
                else:
                    patron += "0"
            
            fila_patron = self.patrones.buscar(patron)
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
                frecuencia_nodo = self.frecuencias.buscar(patron)
                if frecuencia_nodo:
                    frecuencia_nodo.frecuencia += 1
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
                matriz_reducida.agregar(patron, self.matriz.n, self.m, nueva_fila)  
                self.patrones.agregar(patron)
                self.frecuencias.agregar(patron, 1)
                filas_unicas += 1

            temp = temp.siguiente
            if temp == self.matriz.datos.cabeza:
                break

        self.datos_binarios = matriz_reducida
        self.n = filas_unicas
        print("Matriz reducida generada exitosamente.")

    def mostrar(self):
        print(f"Matriz Reducida '{self.nombre}':")
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

    def crearGraphviz(self):
        if self.matriz.n == 0 or self.m == 0:  
            print("Dimensiones inválidas")
            return
        
        nombre_normalizado = normalizar_nombre(self.nombre)
        textoDOT = '''digraph G {
    node[shape=plaintext];
    edge[style=invis];

    label="nombre Matriz = ''' + self.nombre + '''"
    matriz [
    label=<<TABLE border="1" cellspacing="0" cellpadding="10">
    <tr><td colspan="''' + str(self.m) + '''">n = ''' + str(self.matriz.n) + ''', m = ''' + str(self.m) + '''</td></tr>
    '''

        actual = self.matriz.datos.cabeza
        for i in range(self.matriz.n):  
            textoDOT += "   <tr>\n"
            for j in range(self.m):
                textoDOT += f"<td>{actual.datos.cabeza.nombre}</td>\n"
                actual.datos.cabeza = actual.datos.cabeza.siguiente
            textoDOT += "   </tr>\n"
            actual = actual.siguiente

        textoDOT += ''' </TABLE>
    >];
}
'''

        with open("matriz.dot", "w") as dot_file:
            dot_file.write(textoDOT)

        system('dot -Tpdf matriz.dot -o ' + nombre_normalizado + ".pdf")
        startfile(nombre_normalizado + ".pdf")

    def crearGraphvizReducida(self):
        if self.n == 0 or self.m == 0:
            print("Dimensiones inválidas")
            return
        
        nombre_normalizado = normalizar_nombre(self.nombre)
        textoDOT = '''digraph G {
    node[shape=plaintext];
    edge[style=invis];

    label="nombre Matriz Reducida = ''' + self.nombre + '''"
    matriz [
    label=<<TABLE border="1" cellspacing="0" cellpadding="10">
    <tr><td colspan="''' + str(self.m) + '''">n = ''' + str(self.n) + ''', m = ''' + str(self.m) + ''', g = ''' + str(self.frecuencias.contar()) + '''</td></tr>
    '''

        actual = self.datos_binarios.cabeza
        for i in range(self.n):
            textoDOT += "   <tr>\n"
            for j in range(self.m):
                textoDOT += f"<td>{actual.datos.cabeza.nombre}</td>\n"
                actual.datos.cabeza = actual.datos.cabeza.siguiente
            textoDOT += "   </tr>\n"
            actual = actual.siguiente

        textoDOT += ''' </TABLE>
    >];
}
'''

        with open("matriz_reducida.dot", "w") as dot_file:
            dot_file.write(textoDOT)

        system('dot -Tpdf matriz_reducida.dot -o ' + nombre_normalizado + "_reducida.pdf")
        startfile(nombre_normalizado + "_reducida.pdf")

def leer_archivo(ruta):
    doc = minidom.parse(ruta)
    root = doc.documentElement

    matrices = ListaCircular()

    for matriz in root.getElementsByTagName('matriz'):
        nombre = matriz.getAttribute('nombre')
        n = int(matriz.getAttribute('n'))
        m = int(matriz.getAttribute('m'))

        if n == 0 or m == 0:
            print(f"Advertencia: La matriz '{nombre}' tiene dimensiones inválidas (n={n}, m={m}) y será omitida.")
            continue

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

def escribir_archivo(matrices_binarias, ruta_salida):
    doc = Document()
    matrices = doc.createElement('matrices')
    doc.appendChild(matrices)

    temp = matrices_binarias.cabeza
    while True:
        matriz_binaria = temp.datos
        if matriz_binaria is None:
            temp = temp.siguiente
            if temp == matrices_binarias.cabeza:
                break
            continue

        matriz = doc.createElement('matriz')
        matriz.setAttribute('nombre', matriz_binaria.nombre)
        matriz.setAttribute('n', str(matriz_binaria.n))
        matriz.setAttribute('m', str(matriz_binaria.m))
        matriz.setAttribute('g', str(matriz_binaria.frecuencias.contar()))  
        matrices.appendChild(matriz)

        fila_actual = matriz_binaria.datos_binarios.cabeza
        y = 1
        while fila_actual:
            celda_actual = fila_actual.datos.cabeza
            x = 1
            while celda_actual:
                dato = doc.createElement('dato')
                dato.setAttribute('x', str(y))
                dato.setAttribute('y', str(x))
                dato.appendChild(doc.createTextNode(celda_actual.nombre))
                matriz.appendChild(dato)

                celda_actual = celda_actual.siguiente
                x += 1
                if celda_actual == fila_actual.datos.cabeza:
                    break

            fila_actual = fila_actual.siguiente
            y += 1
            if fila_actual == matriz_binaria.datos_binarios.cabeza:
                break

        # Escribir las frecuencias después de todos los datos
        frecuencia_actual = matriz_binaria.frecuencias.cabeza
        grupos = ListaGrupos()
        grupo = 1
        fila_actual = matriz_binaria.datos_binarios.cabeza
        while frecuencia_actual:
            patron = frecuencia_actual.patron
            nodo_grupo = grupos.buscar(patron)
            if not nodo_grupo:
                grupos.agregar(patron, grupo)
                grupo += 1
                nodo_grupo = grupos.buscar(patron)

            frecuencia_element = doc.createElement('frecuencia')
            frecuencia_element.setAttribute('g', str(nodo_grupo.grupo))  # Asignar el número de grupo
            frecuencia_element.appendChild(doc.createTextNode(str(frecuencia_actual.frecuencia)))
            matriz.appendChild(frecuencia_element)

            frecuencia_actual = frecuencia_actual.siguiente
            if frecuencia_actual == matriz_binaria.frecuencias.cabeza:
                break

        temp = temp.siguiente
        if temp == matrices_binarias.cabeza:
            break

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

def main():
    matrices = None
    matrices_binarias = ListaCircular()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ruta = input("Ingrese la ruta completa del archivo de entrada: ")
            matrices = leer_archivo(ruta)
            print("Archivo cargado exitosamente.")
            print("Matrices cargadas:")
            matrices.mostrar()
        elif opcion == '2':
            if not matrices:
                print("Primero cargue un archivo.")
                continue
            print("Procesar archivo seleccionado.")
            temp = matrices.cabeza
            while True:
                print(f"Datos de la matriz: {temp.nombre}, n: {temp.n}, m: {temp.m}")
                matriz_binaria = MatrizBinaria(temp)
                matriz_binaria.convertir_a_binaria()
                time.sleep(2)
                print("Obteniendo matriz reducida")
                matriz_binaria.reducir_matriz()
                matriz_binaria.mostrar()
                matrices_binarias.agregar(matriz_binaria.nombre, matriz_binaria.n, matriz_binaria.m, matriz_binaria)
                temp = temp.siguiente
                if temp == matrices.cabeza:
                    break
        elif opcion == '3':
            if not matrices_binarias.cabeza:
                print("Primero procese el archivo (opción 2).")
                continue
            ruta_salida = input("Ingrese la ruta completa del archivo de salida: ")
            if not ruta_salida.endswith('.xml'):
                print("Error: La ruta del archivo de salida debe tener la extensión .xml")
                continue
            try:
                escribir_archivo(matrices_binarias, ruta_salida)
                print("Archivo de salida generado exitosamente.")
            except Exception as e:
                print(f"Error al generar el archivo de salida: {e}")
        elif opcion == '4':
            print("--------- Datos del estudiante ---------")
            print("Nombre: Javier Andrés Velásquez Bonilla")
            print("Carné: 202307775")
            print("Ingeniería en Ciencias y Sistemas")
            print("Curso: Introducción a la Programación y Computación 2")
            print("Semetre: 4to")
            print("----------------------------------------")
        elif opcion == '5':
            if not matrices_binarias.cabeza:
                print("Primero procese el archivo (opción 2).")
                continue
            nombre_matriz = input("Ingrese el nombre de la matriz para generar la gráfica: ")
            matriz_binaria = matrices_binarias.buscar(nombre_matriz)
            if not matriz_binaria:
                print("Matriz no encontrada.")
                continue
            matriz_binaria.datos.crearGraphviz()
            matriz_binaria.datos.crearGraphvizReducida()
        elif opcion == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()

