import tkinter as tk
from tkinter import ttk, messagebox

import sqlite3
import config

# Funciones para botones
def agregar_proveedor(nombre, direccion, telefono):
    try:
        cone = config.ConexionBaseDeDatos()
        query = cone.cursor()
        sql = "INSERT INTO Proveedores (nombre, direccion, telefono) VALUES (?, ?, ?);"
        valores = (nombre, direccion, telefono)
        query.execute(sql, valores)
        cone.commit()
        cone.close()
        messagebox.showinfo("Agregado", "Proveedor agregado correctamente")
    except sqlite3.Error as error:
        print(f"Error al guardar registro de Proveedores: {error}")

def modificar_proveedor(id, nombre, telefono, direccion):
    try:
        cone = config.ConexionBaseDeDatos()
        query = cone.cursor()
        sql = "UPDATE Proveedores SET nombre = ?, telefono = ?, direccion = ? WHERE id = ?;"
        valores = (nombre, telefono, direccion, id)
        query.execute(sql, valores)
        cone.commit()
        cone.close()
        messagebox.showinfo("Modificado", "Proveedor modificado correctamente")
    except sqlite3.Error as error:
        print(f"Error al actualizar registro de Proveedores: {error}")

def eliminar_proveedor(id):
    try:
        cone = config.ConexionBaseDeDatos()
        query = cone.cursor()
        sql = "DELETE FROM Proveedores WHERE id = ?;"
        valores = (id,)
        query.execute(sql, valores)
        cone.commit()
        cone.close()
        messagebox.showinfo("Eliminado", "Proveedor eliminado correctamente")
    except sqlite3.Error as error:
        print(f"Error al eliminar registro de Proveedores: {error}")

def mostrar_proveedores():
    try:
        cone = config.ConexionBaseDeDatos()
        query = cone.cursor()
        query.execute("SELECT * FROM Proveedores;")
        resultados = query.fetchall()
        cone.close()
        return resultados
    except sqlite3.Error as error:
        print(f"Error al mostrar los Proveedores: {error}")
        return []

def seleccionar_registro(event):
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        if valores:
            id_seleccionado.set(valores[0])
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, valores[1])
            entry_direccion.delete(0, tk.END)
            entry_direccion.insert(0, valores[2])
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, valores[3])

def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    for row in mostrar_proveedores():
        tabla.insert("", "end", values=row)

def proveedores():
    global tabla, columnas, entry_direccion, entry_telefono, entry_nombre, id_seleccionado
    
    supplier_Window = tk.Toplevel()
    supplier_Window.title("Gestión de proveedores")
    supplier_Window.geometry("500x400")

    # Variable para almacenar el ID seleccionado
    id_seleccionado = tk.StringVar()

    # Función para seleccionar registro
    def seleccionar_registro(event):
        seleccionado = tabla.focus()
        if seleccionado:
            valores = tabla.item(seleccionado, "values")
            if valores:
                id_seleccionado.set(valores[0])
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, valores[1])
                entry_telefono.delete(0, tk.END)
                entry_telefono.insert(0, valores[2])
                entry_direccion.delete(0, tk.END)
                entry_direccion.insert(0, valores[3])

    def buscar_proveedores():
        id_buscar = entry_buscar.get().strip()
        if not id_buscar:
            messagebox.showwarning("Advertencia", "Ingresa un ID para buscar")
            return

        for row in tabla.get_children():
            tabla.delete(row)

        encontrado = False
        for row in mostrar_proveedores():
            if str(row[0]) == id_buscar:
                tabla.insert("", "end", values=row)
                encontrado = True
                break

        if not encontrado:
            messagebox.showwarning("Advertencia", f"No se encontró un proveedor con ID {id_buscar}")

    def modificar_registro():
        if id_seleccionado.get():
            modificar_proveedor(id_seleccionado.get(), entry_nombre.get(), entry_telefono.get(), entry_direccion.get())
            actualizar_tabla()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un proveedor primero")

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        for row in mostrar_proveedores():
            tabla.insert("", "end", values=row)

    frame_tabla = tk.Frame(supplier_Window)
    frame_tabla.pack(pady=10)

    columnas = ("ID", "Nombre", "Dirección", "Teléfono")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120)
    
    actualizar_tabla()
    
    tabla.pack()
    tabla.bind("<Double-1>", seleccionar_registro)

    frame_botones = tk.Frame(supplier_Window)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_botones, text="Agregar", command=lambda: (agregar_proveedor(entry_nombre.get(), entry_direccion.get(), entry_telefono.get()), actualizar_tabla()))
    btn_agregar.grid(row=0, column=0, padx=5)

    btn_modificar = tk.Button(frame_botones, text="Modificar", command=lambda: modificar_registro())
    btn_modificar.grid(row=0, column=1, padx=5)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=lambda: (eliminar_proveedor(id_seleccionado.get()), actualizar_tabla()))
    btn_eliminar.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botones, text="Buscar", command=buscar_proveedores)
    btn_buscar.grid(row=0, column=3, padx=5)

    frame_datos = tk.Frame(supplier_Window)
    frame_datos.pack(pady=10)

    tk.Label(frame_datos, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    entry_buscar = tk.Entry(frame_datos)
    entry_buscar.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_datos, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(frame_datos)
    entry_nombre.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_datos, text="Dirección:").grid(row=2, column=0, padx=5, pady=5)
    entry_direccion = tk.Entry(frame_datos)
    entry_direccion.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_datos, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5)
    entry_telefono = tk.Entry(frame_datos)
    entry_telefono.grid(row=3, column=1, padx=5, pady=5)
