import tkinter as tk
from tkinter import ttk
import op1_reporte, op2_conf, op3_inventario, op4_clients, op5_porveedorees

# Función para iniciar el punto de venta
def iniciar_punto_venta():
    from config import boton_buscar, actualizar_fecha_hora

    global root, fecha_label, hora_label
    root = tk.Tk()
    root.title("Punto de Venta")
    root.geometry("895x455")
    
    # Groupbox 1: Fecha, Hora, Turno
    groupbox1 = tk.LabelFrame(root, text="Información", padx=10, pady=10)
    groupbox1.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Configurar columnas para mejor distribución
    groupbox1.columnconfigure(1, weight=1)  # Permite que la segunda columna se expanda

    # Estilo Fuente
    font=("Arial", 12, "bold")

    # Etiquetas de fecha y hora
    tk.Label(groupbox1, text="Fecha:", font=font).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    fecha_label = tk.Label(groupbox1, text="", font=font)
    fecha_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(groupbox1, text="Hora:", font=font).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    hora_label = tk.Label(groupbox1, text="", font=font)
    hora_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Etiqueta de turno en una nueva fila centrada
    turno_label = tk.Label(groupbox1, text="Turno Activo", font=font, fg="green")
    turno_label.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
    
    # Actualizar la fecha y hora cada segundo
    actualizar_fecha_hora(fecha_label, hora_label, root)
    
    # Groupbox 2: Botones de opciones
    groupbox2 = tk.LabelFrame(root, text="Operaciones", padx=10, pady=10)
    groupbox2.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="ew")

    # Diccionario de botones con sus respectivas funciones
    botones = {
        "Cerrar Turno": op1_reporte.cerrar_turno,
        "Configuración": op2_conf.configuracion,
        "Inventario": op3_inventario.inventario,
        "Clientes": op4_clients.clientes,
        "Proveedores": op5_porveedorees.proveedores
    }

    # Crear los botones dinámicamente con comandos
    for i, (texto, funcion) in enumerate(botones.items()):
        boton = tk.Button(groupbox2, text=texto, width=15, height=1, command=funcion)
        boton.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
    
    
    # Groupbox 3: Entrada, tabla y botones
    groupbox3 = tk.LabelFrame(root, text="Productos", padx=10, pady=10)
    groupbox3.grid(row=1, column=0, rowspan=2, padx=10, pady=5, sticky="ew")
    
    tk.Label(groupbox3, text="Codigo:", padx=10, pady=10).grid(row=0, column=0)
    entry_producto = tk.Entry(groupbox3, width=60)
    entry_producto.grid(row=0, column=1, columnspan=2)
    BtnBuscar = tk.Button(groupbox3, text="Buscar", command=boton_buscar, width=10)
    BtnBuscar.grid(row=0, column=3, padx=10, pady=5)
    
    # Definir las columnas
    columnas = ("Codigo", "Articulo", "Cantidad", "Precio", "Total")

    tree = ttk.Treeview(groupbox3, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)

    # Ajustar el ancho de las columnas
    tree.column("Codigo", width=150)          # Ancho de la columna "#"
    tree.column("Articulo", width=200)  # Ancho de la columna "Articulo"
    tree.column("Cantidad", width=100)  # Ancho de la columna "Cantidad"
    tree.column("Precio", width=100)    # Ancho de la columna "Precio"
    tree.column("Total", width=100)     # Ancho de la columna "Total"

    # Posicionar el Treeview en la ventana
    tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
    #BtnBorrar = tk.Button(groupbox3, text="Borrar", width=10)
    #BtnBorrar.grid(row=2, column=0, padx=10, pady=10)
    
    # Groupbox 4: Resumen de venta
    groupbox4 = tk.LabelFrame(root, text="Resumen de Venta", padx=10, pady=10)
    groupbox4.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    sub_groupbox = tk.LabelFrame(groupbox4, text="Total a Pagar", padx=10, pady=10)
    sub_groupbox.pack(pady=5)
    total_label = tk.Label(sub_groupbox, text="$0.00", font=("Arial", 16))
    total_label.pack()
    tk.Button(groupbox4, text="Cobrar", width=10).pack(pady=10)
    
    root.mainloop()