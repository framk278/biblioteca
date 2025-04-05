import json
import os

# -----------------------------------
# ESTRUCTURAS DE DATOS PRINCIPALES
# -----------------------------------
libros = []
usuarios = []
cola_prestamos = []
pila_devoluciones = []

# -----------------------------------
# FUNCIONES DE ARCHIVOS (PERSISTENCIA)
# -----------------------------------
def guardar_datos():
    with open('libros.json', 'w') as f:
        json.dump(libros, f)
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f)
    with open('cola_prestamos.json', 'w') as f:
        json.dump(cola_prestamos, f)
    with open('pila_devoluciones.json', 'w') as f:
        json.dump(pila_devoluciones, f)

def cargar_datos():
    global libros, usuarios, cola_prestamos, pila_devoluciones
    if os.path.exists('libros.json'):
        with open('libros.json', 'r') as f:
            libros = json.load(f)
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
    if os.path.exists('cola_prestamos.json'):
        with open('cola_prestamos.json', 'r') as f:
            cola_prestamos = json.load(f)
    if os.path.exists('pila_devoluciones.json'):
        with open('pila_devoluciones.json', 'r') as f:
            pila_devoluciones = json.load(f)

# -----------------------------------
# FUNCIONES PRINCIPALES
# -----------------------------------
def agregar_libro(titulo, autor):
    id_libro = len(libros) + 1
    libros.append({'id': id_libro, 'titulo': titulo, 'autor': autor, 'disponible': True})
    guardar_datos()
    print(f"✅ Libro agregado: {titulo} (ID: {id_libro})")

def registrar_usuario(nombre):
    id_usuario = len(usuarios) + 1001
    usuarios.append({'id': id_usuario, 'nombre': nombre, 'libros_prestados': []})
    guardar_datos()
    print(f"✅ Usuario registrado: {nombre} (ID: {id_usuario})")

def solicitar_prestamo(id_usuario, id_libro):
    cola_prestamos.append((id_usuario, id_libro))
    guardar_datos()
    print("📥 Solicitud de préstamo registrada.")

def procesar_prestamo():
    if cola_prestamos:
        id_usuario, id_libro = cola_prestamos.pop(0)
        libro = next((l for l in libros if l['id'] == id_libro and l['disponible']), None)
        if libro:
            libro['disponible'] = False
            for usuario in usuarios:
                if usuario['id'] == id_usuario:
                    usuario['libros_prestados'].append(libro['titulo'])
                    guardar_datos()
                    print(f"📚 Préstamo exitoso: {libro['titulo']} a {usuario['nombre']}")
                    return
        print("❌ Libro no disponible o no encontrado.")
    else:
        print("ℹ️ No hay solicitudes de préstamo.")
    guardar_datos()

def devolver_libro(id_usuario, titulo_libro):
    for usuario in usuarios:
        if usuario['id'] == id_usuario:
            if titulo_libro in usuario['libros_prestados']:
                usuario['libros_prestados'].remove(titulo_libro)
                for libro in libros:
                    if libro['titulo'] == titulo_libro:
                        libro['disponible'] = True
                        pila_devoluciones.append(titulo_libro)
                        guardar_datos()
                        print(f"✅ Libro devuelto: {titulo_libro}")
                        return
            print("❌ El usuario no tiene ese libro.")
            return
    print("❌ Usuario no encontrado.")

def mostrar_historial_devoluciones():
    print("📤 Historial de devoluciones (últimos primero):")
    if not pila_devoluciones:
        print("No hay devoluciones aún.")
    else:
        for libro in reversed(pila_devoluciones):
            print(f"- {libro}")

def mostrar_libros():
    print("\n📚 LIBROS REGISTRADOS EN LA BIBLIOTECA:")
    if not libros:
        print("No hay libros registrados aún.")
    else:
        for libro in libros:
            estado = "Disponible ✅" if libro['disponible'] else "Prestado ❌"
            print(f"- ID: {libro['id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Estado: {estado}")

# -----------------------------------
# MENÚ INTERACTIVO
# -----------------------------------
def menu():
    while True:
        print("\n--- MENÚ BIBLIOTECA ---")
        print("1. Agregar libro")
        print("2. Registrar usuario")
        print("3. Solicitar préstamo")
        print("4. Procesar préstamo")
        print("5. Devolver libro")
        print("6. Ver libros registrados")
        print("7. Ver historial de devoluciones")
        print("8. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            agregar_libro(titulo, autor)
        elif opcion == '2':
            nombre = input("Nombre del usuario: ")
            registrar_usuario(nombre)
        elif opcion == '3':
            id_usuario = int(input("ID del usuario: "))
            id_libro = int(input("ID del libro: "))
            solicitar_prestamo(id_usuario, id_libro)
        elif opcion == '4':
            procesar_prestamo()
        elif opcion == '5':
            id_usuario = int(input("ID del usuario: "))
            titulo_libro = input("Título del libro: ")
            devolver_libro(id_usuario, titulo_libro)
        elif opcion == '6':
            mostrar_libros()
        elif opcion == '7':
            mostrar_historial_devoluciones()
        elif opcion == '8':
            print("¡Gracias por usar la biblioteca! 📚")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# -----------------------------------
# INICIO DEL PROGRAMA
# -----------------------------------
cargar_datos()
menu()
