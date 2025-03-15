from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Función para actualizar la fecha y hora
def actualizar_fecha_hora(fecha_label, hora_label, root):
    def actualizar():
        ahora = datetime.now()
        fecha_label.config(text=ahora.strftime("%Y-%m-%d"))
        hora_label.config(text=ahora.strftime("%H:%M:%S"))
        root.after(1000, actualizar)  # Actualiza cada segundo

    actualizar()

def busqueda_articulo():
    # Crear la nueva ventana
    ventana_buscar = tk.Toplevel()  # Toplevel crea una nueva ventana
    ventana_buscar.title("Buscar Artículo")
    ventana_buscar.geometry("360x370")  # Tamaño de la ventana

    # Etiqueta en la parte superior
    etiqueta = tk.Label(ventana_buscar, text="Ingrese el código o nombre del artículo:")
    etiqueta.pack(pady=10)

    # Entrada de texto para buscar
    entrada_buscar = tk.Entry(ventana_buscar, width=40)
    entrada_buscar.pack(pady=5)

    # Crear la tabla para mostrar los resultados
    columnas = ("Codigo", "Articulo", "Cantidad", "Precio", "Total")
    tabla = ttk.Treeview(ventana_buscar, columns=columnas, show="headings")
    
    # Configurar las columnas de la tabla
    for col in columnas:
        if col == "Codigo" or col == "Articulo":
            tabla.heading(col, text=col)
            tabla.column(col, width=100)
        else:
            tabla.heading(col, text=col)
            tabla.column(col, width=50)
    
    tabla.pack(pady=10)

    # Función para agregar una fila a la tabla
    def agregar_fila():
        codigo = entrada_buscar.get()
        if codigo:  # Si hay algo en la entrada
            print("Aqui se puede agregar algo")

    # Función para limpiar la entrada de texto
    def limpiar_entrada():
        entrada_buscar.delete(0, tk.END)

    # Botón para agregar la fila
    boton_agregar = tk.Button(ventana_buscar, text="Agregar", command=agregar_fila)
    boton_agregar.pack(side=tk.LEFT, padx=10, pady=10)

    # Botón para limpiar la entrada de texto
    boton_limpiar = tk.Button(ventana_buscar, text="Limpiar", command=limpiar_entrada)
    boton_limpiar.pack(side=tk.RIGHT, padx=10, pady=10)

# Función para el botón "Buscar" en la ventana principal
def boton_buscar():
    busqueda_articulo()
    

def obtener_configuracion():
    try:
        conexion = ConexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT User, Password, Mode FROM Configuracion LIMIT 1")
            config = cursor.fetchone()
            conexion.close()
            return config if config else ("", "", "light")
        else:
            return ("", "", "light")
    except sqlite3.Error as error:
        print(f"Error al obtener la configuración: {error}")
        return ("", "", "light")

def actualizar_configuracion(usuario, clave, modo):
    try:
        conexion = ConexionBaseDeDatos()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("UPDATE Configuracion SET User=?, Password=?, Mode=?", (usuario, clave, modo))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Configuración actualizada correctamente")
        else:
            print("No se pudo establecer la conexión a la base de datos.")
    except sqlite3.Error as error:
        print(f"Error al actualizar la configuración: {error}")

# Función para verificar login
def verificar_login(entry_usuario, entry_clave, login_window):
    from vPrincipal import iniciar_punto_venta
    
    usuario, clave, _ = obtener_configuracion()
    if entry_usuario.get() == usuario and entry_clave.get() == clave:
        login_window.destroy()
        # Aquí debes agregar lo que ocurre después de hacer login, por ejemplo iniciar el punto de venta
        print("Login exitoso")
        iniciar_punto_venta()
    else:
        messagebox.showerror("Error", "Usuario o clave incorrectos")
        entry_usuario.delete(0, tk.END)
        entry_clave.delete(0, tk.END)

# config.py
def ConexionBaseDeDatos():
    import sqlite3
    try:
        conexion = sqlite3.connect("tiendaV2.db")
        print("Conexión Correcta")
        return conexion
    except sqlite3.Error as error:
        print("Error en la conexión a la base de Datos: " + str(error))
        return None