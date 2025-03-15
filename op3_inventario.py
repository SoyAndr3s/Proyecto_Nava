import tkinter as tk
from tkinter import ttk, messagebox

# ==== FUNCIONES ====
def limpiar_campos(entradas, categoria_cb, proveedor_cb):
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
        categoria_cb.current(0)
        proveedor_cb.current(0)

def agregar_producto(entradas, categoria_cb, proveedor_cb, tabla_inv):
        datos = [entrada.get() for entrada in entradas.values()] + [categoria_cb.get(), proveedor_cb.get()]
        
        if any(not dato for dato in datos):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        
        tabla_inv.insert("", "end", values=(len(tabla_inv.get_children()) + 1, *datos))
        limpiar_campos(entradas, categoria_cb, proveedor_cb)
        messagebox.showinfo("Éxito", "Producto agregado correctamente")

def modificar_producto(entradas, categoria_cb, proveedor_cb, tabla_inv, frame_botones):
        selected_item = tabla_inv.selection()
        if not selected_item:
            messagebox.showwarning("Modificar", "Selecciona un producto para modificar")
            return
        
        item = selected_item[0]
        valores = tabla_inv.item(item, "values")
        
        for i, key in enumerate(entradas):
            entradas[key].delete(0, tk.END)
            entradas[key].insert(0, valores[i + 1])

        categoria_cb.set(valores[-2])
        proveedor_cb.set(valores[-1])

        def guardar_modificacion():
            nuevos_valores = [entrada.get() for entrada in entradas.values()] + [categoria_cb.get(), proveedor_cb.get()]
            
            if any(not dato for dato in nuevos_valores):
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return

            tabla_inv.item(item, values=(valores[0], *nuevos_valores))
            limpiar_campos(entradas, categoria_cb, proveedor_cb)
            messagebox.showinfo("Éxito", "Producto modificado correctamente")

        tk.Button(frame_botones, text="Guardar cambios", command=guardar_modificacion).grid(row=1, column=1, padx=5, pady=5)

def eliminar_producto(tabla_inv):
        selected_item = tabla_inv.selection()
        if not selected_item:
            messagebox.showwarning("Eliminar", "Selecciona un producto para eliminar")
            return
        
        for item in selected_item:
            tabla_inv.delete(item)
        
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")

def buscar_producto(entradas, tabla_inv):
        query = entradas["Nombre"].get().lower()
        for item in tabla_inv.get_children():
            valores = tabla_inv.item(item, "values")
            if query in valores[2].lower():
                tabla_inv.selection_set(item)
                tabla_inv.focus(item)
                return
        messagebox.showinfo("Búsqueda", "Producto no encontrado")
        
def obtener_datos():
    import config
    cone = config.ConexionBaseDeDatos()
    cursor = cone.cursor()
    
    cursor.execute("SELECT Nombre_Cat FROM Categorias;")
    categorias = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT Nombre FROM Proveedores;")
    proveedores = [row[0] for row in cursor.fetchall()]
    
    cone.close()
    return categorias, proveedores

# Obtener categorías y proveedores desde la base de datos
categorias, proveedores = obtener_datos()

# ==== FUNCIONES ====
def limpiar_campos(entry_cat):
    entry_cat.delete(0, tk.END)

def agregar_tipo(entry_cat, tabla_tipo):
    import config
    
    categoria = entry_cat.get()
    if not categoria:
        messagebox.showwarning("Error", "El campo de categoría es obligatorio")
        return
    
    cone = config.ConexionBaseDeDatos()
    cursor = cone.cursor()
    cursor.execute("INSERT INTO Categorias (Nombre_Cat) VALUES (?)", (categoria,))
    cone.commit()
    cone.close()
    
    cargar_tipos(tabla_tipo)
    limpiar_campos(entry_cat)
    messagebox.showinfo("Éxito", "Categoría agregada correctamente")

def eliminar_tipo(tabla_tipo, entry_cat):
    import config
    
    selected_item = tabla_tipo.selection()
    if not selected_item:
        messagebox.showwarning("Eliminar", "Selecciona una categoría para eliminar")
        return
    
    item = selected_item[0]
    valores = tabla_tipo.item(item, "values")
    
    cone = config.ConexionBaseDeDatos()
    cursor = cone.cursor()
    cursor.execute("DELETE FROM Categorias WHERE ID_Cat = ?", (valores[0],))
    cone.commit()
    cone.close()
    
    cargar_tipos(tabla_tipo)
    limpiar_campos(entry_cat)
    messagebox.showinfo("Éxito", "Categoría eliminada correctamente")

def modificar_tipo(tabla_tipo, entry_cat):
    import config
    
    selected_item = tabla_tipo.selection()
    if not selected_item:
        messagebox.showwarning("Modificar", "Selecciona una categoría para modificar")
        return
    
    item = selected_item[0]
    valores = tabla_tipo.item(item, "values")
    nueva_categoria = entry_cat.get()
    
    if not nueva_categoria:
        messagebox.showwarning("Error", "El campo de categoría es obligatorio")
        return
    
    cone = config.ConexionBaseDeDatos()
    cursor = cone.cursor()
    cursor.execute("UPDATE Categorias SET Nombre_Cat = ? WHERE ID_Cat = ?", (nueva_categoria, valores[0]))
    cone.commit()
    cone.close()
    
    cargar_tipos(tabla_tipo)
    limpiar_campos(entry_cat)
    messagebox.showinfo("Éxito", "Categoría modificada correctamente")

def cargar_tipos(tabla_tipo):
    import config
    
    cone = config.ConexionBaseDeDatos()
    cursor = cone.cursor()
    cursor.execute("SELECT ID_Cat, Nombre_Cat FROM Categorias")
    datos = cursor.fetchall()
    cone.close()
    
    tabla_tipo.delete(*tabla_tipo.get_children())
    for fila in datos:
        tabla_tipo.insert("", "end", values=fila)

def seleccionar_tipo(tabla_tipo, entry_cat):
    selected_item = tabla_tipo.selection()
    if not selected_item:
        return
    
    item = selected_item[0]
    valores = tabla_tipo.item(item, "values")
    entry_cat.delete(0, tk.END)
    entry_cat.insert(0, valores[1])

def inventario():
    inv_Window = tk.Toplevel()
    inv_Window.title("Gestión de Inventario")
    inv_Window.geometry("850x620")

    # ==== TABLA DE INVENTARIO ====
    frame_tabla = tk.Frame(inv_Window)
    frame_tabla.pack(pady=10)

    columnas_inv = ("ID_Producto", "Código_Barras", "Nombre", "Cantidad", "Precio_Compra", "Precio_Venta", "Categoria", "Proveedor")
    tabla_inv = ttk.Treeview(frame_tabla, columns=columnas_inv, show="headings")

    for col in columnas_inv:
        tabla_inv.heading(col, text=col)
        tabla_inv.column(col, width=100)
    
    tabla_inv.column("ID_Producto", width=75)
    tabla_inv.column("Cantidad", width=75)
    tabla_inv.pack()

    # ==== CONTENEDOR PRINCIPAL ====
    frame_contenedor = tk.Frame(inv_Window)
    frame_contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # ==== GROUPBOX PARA DATOS DEL PRODUCTO ====
    groupbox_productos = tk.LabelFrame(frame_contenedor, text="Datos del Producto")
    groupbox_productos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    etiquetas = ["Código de Barras", "Nombre", "Cantidad", "Precio Compra", "Precio Venta"]
    entradas = {}

    for i, label in enumerate(etiquetas):
        tk.Label(groupbox_productos, text=label + ":").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entradas[label] = tk.Entry(groupbox_productos)
        entradas[label].grid(row=i, column=1, padx=5, pady=5)

    # ==== LISTAS DESPLEGABLES ====
    tk.Label(groupbox_productos, text="Categoria:").grid(row=len(etiquetas), column=0, padx=5, pady=5, sticky="e")
    categoria_cb = ttk.Combobox(groupbox_productos, values=categorias)
    categoria_cb.grid(row=len(etiquetas), column=1, padx=5, pady=5)
    categoria_cb.current(0)

    tk.Label(groupbox_productos, text="Proveedor:").grid(row=len(etiquetas) + 1, column=0, padx=5, pady=5, sticky="e")
    proveedor_cb = ttk.Combobox(groupbox_productos, values=proveedores)
    proveedor_cb.grid(row=len(etiquetas) + 1, column=1, padx=5, pady=5)
    proveedor_cb.current(0)

    # ==== BOTONES ====    
    frame_botones = tk.Frame(groupbox_productos)
    frame_botones.grid(row=len(etiquetas) + 2, column=0, columnspan=2, pady=10)

    tk.Button(frame_botones, text="Agregar", command=lambda: agregar_producto(entradas, categoria_cb, proveedor_cb, tabla_inv)).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Modificar", command=lambda: modificar_producto(entradas, categoria_cb, proveedor_cb, tabla_inv, frame_botones)).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar", command=lambda: eliminar_producto(tabla_inv)).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Buscar", command=lambda: buscar_producto(entradas, tabla_inv)).grid(row=0, column=3, padx=5)

    # ==== TABLA DE TIPOS DE PRODUCTO ====
    groupbox_tipos = tk.LabelFrame(frame_contenedor, text="Tipos de Producto")
    groupbox_tipos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    columnas_tipo = ("ID_Tipo", "Categoria")
    tabla_tipo = ttk.Treeview(groupbox_tipos, columns=columnas_tipo, show="headings")

    tabla_tipo.heading("ID_Tipo", text="ID")
    tabla_tipo.column("ID_Tipo", width=50)

    tabla_tipo.heading("Categoria", text="Categoria")
    tabla_tipo.column("Categoria", width=150)

    # Empaquetar la tabla correctamente
    tabla_tipo.pack(padx=5, pady=5, fill="both", expand=True)

    # Entrada de texto para mostrar ID seleccionado
    frame_entry = tk.Frame(groupbox_tipos)
    frame_entry.pack(pady=10)
    
    cat = tk.Label(frame_entry, text="Categoria:")
    cat.grid(row=0, column=0, padx=5)
    
    entry_cat = tk.Entry(frame_entry)
    entry_cat.grid(row=0, column=1, padx=5)

    # Botones para gestionar la tabla (ahora en un frame separado dentro del groupbox)
    frame_botones = tk.Frame(groupbox_tipos)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_botones, text="Agregar", command=lambda: agregar_tipo(entry_cat, tabla_tipo))
    btn_agregar.grid(row=0, column=0, padx=5)
    
    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=lambda: eliminar_tipo(tabla_tipo, entry_cat))
    btn_eliminar.grid(row=0, column=1, padx=5)
    
    btn_modificar = tk.Button(frame_botones, text="Modificar", command=lambda: modificar_tipo(tabla_tipo, entry_cat))
    btn_modificar.grid(row=0, column=2, padx=5)
    
    tabla_tipo.bind("<ButtonRelease-1>", lambda event: seleccionar_tipo(tabla_tipo, entry_cat))
    
    cargar_tipos(tabla_tipo)
    
    inv_Window.mainloop()
    