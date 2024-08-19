import xml.etree.ElementTree as ET
from xml.dom import minidom

def Menu():
    print(' ------------- Menu Principal -------------')
    print('1. Cargar archivo XML')
    print('2. Procesar XML')
    print('3. Escribir archivo salida')
    print('4. Mostrar datos del estudiante')
    print('5. Generar gráfica')
    print('6. Salir')
    print('------------------------------------------')

    opc = int(input('Ingrese la opción: '))
    return opc

def LeerArchivoET(rutaArchivo):
    tree = ET.parse(rutaArchivo) 
    root = tree.getroot() 

if __name__ == '__main__':
    opc = 0
    rutaArchivo = None
    while opc != 6:
        opc = Menu()

        if opc == 1:
            rutaArchivo = input("Ingrese la ruta del archivo: ")
        elif opc == 2:
            if rutaArchivo:
                LeerArchivoET(rutaArchivo)
            else:
                print("Primero debe cargar un archivo.")
        elif opc == 3:
            if rutaArchivo:
                pass
            else:
                print("Primero debe cargar un archivo.")
        elif opc == 4:
            print("------------------------------------------")
            print("Datos del estudiante:")
            print("Javier Andrés Velásquez Bonilla\n202307775\nIngeniería en Ciencias y Sistemas\n4to Semestre\nIntroducción a la Programación y Computación 2 Sección 'A'")
            print("------------------------------------------")
        elif opc == 5:
            pass
        elif opc == 6:
            print('Saliendo...')
            break
        else:
            print('Opción no válida')
            continue

    