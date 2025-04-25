import tkinter as tk
from tkinter import ttk, messagebox
import op1_cierre, op2_conf, op3_inventario, op4_clients, op5_porveedorees, op6_reporte

# Función para iniciar el punto de venta
def iniciar_punto_venta():
    from config import busqueda_articulo, actualizar_fecha_hora, procesar_codigo, abrir_ventana_cobro, maquina_usasda
    global root, fecha_label, hora_label, productos_agregados, cliente_seleccionado_id
    
    productos_agregados = {}
    cliente_seleccionado_id = 1  # Cliente por defecto
    
    root = tk.Tk()
    root.title("Punto de Venta")
    root.geometry("965x525")
    
    # Groupbox 1: Fecha, Hora, Turno
    groupbox1 = tk.LabelFrame(root, text="Información", padx=10, pady=10)
    groupbox1.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Configurar columnas para mejor distribución
    groupbox1.columnconfigure(1, weight=1)  # Permite que la segunda columna se expanda

    # Estilo Fuente
    font=("Arial", 12, "bold")
    
    tk.Label(groupbox1, text="Fecha:", font=font).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    fecha_label = tk.Label(groupbox1, text="", font=font)
    fecha_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(groupbox1, text="Hora:", font=font).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    hora_label = tk.Label(groupbox1, text="", font=font)
    hora_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Etiqueta de turno en una nueva fila centrada
    estado_label = tk.Label(groupbox1, text="Estado:", font=font, fg="green")
    estado_label.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    
    turno_label = tk.Label(groupbox1, text="Turno Activo", font=font, fg="green")
    turno_label.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
    
    # Etiquetas de maquina, fecha y hora
    tk.Label(groupbox1, text="Maquina:", font=font).grid(row=1, column=2, padx=10, pady=5, sticky="ew")
    mache_label = tk.Label(groupbox1, text="", font=font)
    mache_label.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    
    # Actualizar la fecha y hora cada segundo
    actualizar_fecha_hora(fecha_label, hora_label, root)
    
    # Mostrar maquina usada
    maquina_usasda(mache_label)
    
    # Groupbox 2: Botones de opciones
    groupbox2 = tk.LabelFrame(root, text="Operaciones", padx=10, pady=10)
    groupbox2.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="ew")

    # Diccionario de botones con sus respectivas funciones
    botones = {
        "Cerrar Turno": op1_cierre.cerrar_turno,
        "Configuración": op2_conf.configuracion,
        "Inventario": op3_inventario.inventario,
        "Clientes": op4_clients.clientes,
        "Proveedores": op5_porveedorees.proveedores,
        "Reportes": op6_reporte.reporte_venta
    }

    # Crear los botones dinámicamente con comandos
    for i, (texto, funcion) in enumerate(botones.items()):
        tk.Button(groupbox2, text=texto, width=15, height=1, command=funcion).grid(row=i, column=0, padx=10, pady=10)

    # Groupbox 3: Entrada, tabla y botones
    groupbox3 = tk.LabelFrame(root, text="Productos", padx=10, pady=10)
    groupbox3.grid(row=1, column=0, rowspan=2, padx=10, pady=5, sticky="ew")
    
    # === Nivel 1 ===
    nivel1 = tk.Frame(groupbox3)
    nivel1.grid(row=0, column=0, sticky="w", pady=5)
    
    tk.Label(nivel1, text="Codigo:", padx=10, pady=10).grid(row=0, column=0)
    entry_producto = tk.Entry(nivel1, width=60)
    entry_producto.grid(row=0, column=1)
    
    BtnBuscar = tk.Button(nivel1, text="🔍", fg="red", command=lambda: busqueda_articulo(tree, productos_agregados, total_label))
    BtnBuscar.grid(row=0, column=3, padx=10)
    
    
    
    def ConexionBaseDeDatos():
        import sqlite3
        try:
            conexion = sqlite3.connect("tiendaV2.db")
            print("Conexión Correcta")
            return conexion
        except sqlite3.Error as error:
            print("Error en la conexión a la base de Datos: " + str(error))
            return None
    
    
    # ==== LISTAS DESPLEGABLES ====
    def seleccionar_cliente_especial():
        def buscar_cliente():
            try:
                conn = ConexionBaseDeDatos()
                cursor = conn.cursor()
                cursor.execute("SELECT id_cliente, nombre FROM clientes WHERE id_cliente=?", (entry_id.get(),))
                result = cursor.fetchone()
                conn.close()
                if result:
                    global cliente_seleccionado_id
                    cliente_seleccionado_id = result[0]
                    lbl_nombre.config(text=f"Nombre: {result[1]}")
                else:
                    messagebox.showerror("No encontrado", "Cliente no encontrado.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ventana_cliente = tk.Toplevel(root)
        ventana_cliente.title("Buscar Cliente")
        ventana_cliente.geometry("300x150")
        tk.Label(ventana_cliente, text="ID del Cliente:").pack(pady=5)
        entry_id = tk.Entry(ventana_cliente)
        entry_id.pack(pady=5)
        tk.Button(ventana_cliente, text="Buscar", command=buscar_cliente).pack(pady=5)
        lbl_nombre = tk.Label(ventana_cliente, text="Nombre: ")
        lbl_nombre.pack(pady=5)
        
    def cambio_cliente(event):
        if cliente_cb.get() == "Cliente Especial":
            seleccionar_cliente_especial()
        else:
            global cliente_seleccionado_id
            cliente_seleccionado_id = 1

    clientes = ['Publico General', 'Cliente Especial']
    tk.Label(nivel1, text="Cliente:").grid(row=0, column=6)
    cliente_cb = ttk.Combobox(nivel1, values=clientes)
    cliente_cb.grid(row=0, column=7)
    cliente_cb.current(0)
    cliente_cb.bind("<<ComboboxSelected>>", cambio_cliente)
    
    # === Nivel 2 ===
    nivel2 = tk.Frame(groupbox3)
    nivel2.grid(row=1, column=0, sticky="w", pady=5)
    columnas = ("Codigo", "Articulo", "Cantidad", "Precio", "Total")
    tree = ttk.Treeview(nivel2, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col != "Articulo" else 320)
    tree.grid(row=1, column=0, padx=10, pady=10)

    # === Nivel 3 ===
    nivel3 = tk.Frame(groupbox3)
    nivel3.grid(row=2, column=0, sticky="w", pady=5)

    tk.Label(nivel3, text="Codigo:").grid(row=2, column=0)
    code_label = tk.Label(nivel3, text="            ", font=font)
    code_label.grid(row=2, column=1)
    tk.Label(nivel3, text="Articulo:").grid(row=2, column=2)
    name_label = tk.Label(nivel3, text="            ", font=font)
    name_label.grid(row=2, column=3)
    tk.Label(nivel3, text="Cantidad:").grid(row=2, column=4)
    cantidad_label = ttk.Spinbox(nivel3, from_=0, to=30, increment=1)
    cantidad_label.grid(row=2, column=5)
    tk.Label(nivel3, text="Precio:").grid(row=2, column=6)
    precio_label = tk.Label(nivel3, text="            ", font=font)
    precio_label.grid(row=2, column=7)

    def actualizar_nivel3(event):
        selected = tree.focus()
        if selected:
            valores = tree.item(selected, "values")
            codigo, nombre, cantidad, precio, _ = valores
            code_label.config(text=codigo)
            name_label.config(text=nombre)
            precio_label.config(text=precio)

            conn = ConexionBaseDeDatos()
            cursor = conn.cursor()
            cursor.execute("SELECT Cantidad FROM productos WHERE Codigo_Barras=?", (codigo,))
            stock = cursor.fetchone()[0]
            conn.close()

            cantidad_label.config(from_=0, to=stock)
            cantidad_label.delete(0, "end")
            cantidad_label.insert(0, cantidad)

    def actualizar_cantidad(*args):
        codigo = code_label.cget("text")
        if not codigo or codigo not in productos_agregados:
            return
        nueva = int(cantidad_label.get())
        if nueva == 0:
            del productos_agregados[codigo]
            tree.delete(codigo)
            messagebox.showinfo("Producto eliminado", f"{codigo} eliminado de la lista")
        else:
            productos_agregados[codigo]["cantidad"] = nueva

        from config import actualizar_tabla, actualizar_total
        actualizar_tabla(tree, productos_agregados)
        actualizar_total(total_label, productos_agregados)

    tree.bind("<<TreeviewSelect>>", actualizar_nivel3)
    cantidad_label.bind("<Return>", actualizar_cantidad)

    entry_producto.bind("<Return>", lambda event: procesar_codigo(event, entry_producto, tree, total_label, productos_agregados))

    # Groupbox 4: Resumen de venta
    groupbox4 = tk.LabelFrame(root, text="Resumen de Venta", padx=10, pady=10)
    groupbox4.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    sub_groupbox = tk.LabelFrame(groupbox4, text="Total a Pagar", padx=10, pady=10)
    sub_groupbox.pack(pady=5)
    total_label = tk.Label(sub_groupbox, text="$0.00", font=("Arial", 16))
    total_label.pack()
    
    tk.Button(groupbox4, text="Cobrar", width=10, command=lambda: abrir_ventana_cobro(root, productos_agregados)).pack(pady=10)
    
    root.mainloop()