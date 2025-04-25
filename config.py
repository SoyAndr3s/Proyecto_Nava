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
    
def maquina_usasda(mache_label):
    mache_label.config(text="Maquina 1")

def busqueda_articulo(tree_principal, productos_agregados, total_label):
    ventana_buscar = tk.Toplevel()
    ventana_buscar.title("Buscar Artículo")
    ventana_buscar.geometry("600x400")

    etiqueta = tk.Label(ventana_buscar, text="Ingrese el código o nombre del artículo:")
    etiqueta.pack(pady=10)

    entrada_buscar = tk.Entry(ventana_buscar, width=50)
    entrada_buscar.pack(pady=5)

    columnas = ("Codigo", "Articulo", "Cantidad", "Precio", "Categoria")
    tabla = ttk.Treeview(ventana_buscar, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100 if col != "Articulo" else 150)

    tabla.pack(pady=10, expand=True, fill="both")

    def cargar_datos(filtro=""):
        conn = ConexionBaseDeDatos()
        cursor = conn.cursor()

        if filtro:
            query = """
                SELECT Codigo_Barras, nombre, Cantidad, precio_Venta, categoria 
                FROM productos 
                WHERE Codigo_Barras LIKE ? OR nombre LIKE ?
            """
            filtro = f"%{filtro}%"
            cursor.execute(query, (filtro, filtro))
        else:
            cursor.execute("SELECT Codigo_Barras, nombre, Cantidad, precio_Venta, categoria FROM productos")

        resultados = cursor.fetchall()
        conn.close()

        for item in tabla.get_children():
            tabla.delete(item)
        for row in resultados:
            tabla.insert("", tk.END, values=row)

    def actualizar_busqueda(event=None):
        texto = entrada_buscar.get()
        cargar_datos(texto)

    entrada_buscar.bind("<KeyRelease>", actualizar_busqueda)

    def limpiar_entrada():
        entrada_buscar.delete(0, tk.END)
        cargar_datos()

    boton_limpiar = tk.Button(ventana_buscar, text="Limpiar", command=limpiar_entrada)
    boton_limpiar.pack(pady=10)

    def seleccionar_producto(event):
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        codigo, nombre, stock, precio, categoria = valores

        if codigo in productos_agregados:
            productos_agregados[codigo]["cantidad"] += 1
        else:
            productos_agregados[codigo] = {
                "nombre": nombre,
                "precio": float(precio),
                "cantidad": 1
            }

        actualizar_tabla(tree_principal, productos_agregados)
        actualizar_total(total_label, productos_agregados)
        ventana_buscar.destroy()

    tabla.bind("<Double-1>", seleccionar_producto)

    cargar_datos()

    
def boton_buscar():
    print("Buscar_Btn")
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

def ConexionBaseDeDatos():
    import sqlite3
    try:
        conexion = sqlite3.connect("tiendaV2.db")
        print("Conexión Correcta")
        return conexion
    except sqlite3.Error as error:
        print("Error en la conexión a la base de Datos: " + str(error))
        return None
    
def actualizar_tabla(tree, productos_agregados):
    for item in tree.get_children():
        tree.delete(item)
    for codigo, datos in productos_agregados.items():
        total = datos["precio"] * datos["cantidad"]
        tree.insert("", "end", iid=codigo, values=(codigo, datos["nombre"], datos["cantidad"], datos["precio"], total))


def actualizar_total(total_label, productos_agregados):
    total = sum(datos["precio"] * datos["cantidad"] for datos in productos_agregados.values())
    total_label.config(text=f"${total:.2f}")

    
def procesar_codigo(event=None, entry_producto=None, tree=None, total_label=None, productos_agregados=None):

    entrada = entry_producto.get().strip()
    cantidad = 1

    if "*" in entrada:
        try:
            cantidad_str, codigo = entrada.split("*")
            cantidad = int(cantidad_str)
        except ValueError:
            messagebox.showerror("Formato inválido", "Usa el formato '2*12345678'")
            entry_producto.delete(0, tk.END)
            return
    else:
        codigo = entrada

    conn = ConexionBaseDeDatos()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio_Venta, Cantidad FROM productos WHERE Codigo_Barras = ?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre, precio, stock = resultado
        if cantidad > stock:
            messagebox.showwarning("Sin stock", f"Solo hay {stock} unidades disponibles.")
            return

        if codigo in productos_agregados:
            productos_agregados[codigo]["cantidad"] += cantidad
        else:
            productos_agregados[codigo] = {
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad
            }

        actualizar_tabla(tree, productos_agregados)
        actualizar_total(total_label, productos_agregados)
        entry_producto.delete(0, tk.END)
    else:
        messagebox.showerror("No encontrado", f"No se encontró el producto con código: {codigo}")
        entry_producto.delete(0, tk.END)

def abrir_ventana_cobro(root, productos_agregados, cliente_id=1):
    total = sum(datos["precio"] * datos["cantidad"] for datos in productos_agregados.values())

    ventana_cobro = tk.Toplevel(root)
    ventana_cobro.title("Cobrar")
    ventana_cobro.geometry("350x300")

    tk.Label(ventana_cobro, text=f"Total a pagar: ${total:.2f}", font=("Arial", 14)).pack(pady=5)

    # Entrada de pago
    Cantidad_recibida = tk.LabelFrame(ventana_cobro, text="Cantidad recibida:")
    Cantidad_recibida.pack(pady=5)
    entrada_pago = tk.Entry(Cantidad_recibida, font=("Arial", 12), justify="center")
    entrada_pago.grid(column=0, row=0, padx=10, pady=5)

    def limpiar():
        entrada_pago.delete(0, tk.END)
    tk.Button(Cantidad_recibida, text="Clear", bg="red", fg="white", command=limpiar).grid(column=1, row=0)

    # Botones rápidos
    total_pago = tk.LabelFrame(ventana_cobro, text="Pagos Rápidos")
    total_pago.pack(pady=5)
    for i, valor in enumerate([50, 100, 200, 500]):
        tk.Button(total_pago, text=f"${valor}", width=8,
                  command=lambda v=valor: entrada_pago.insert(tk.END, str(v))).grid(row=0, column=i, padx=5)

    cambio_label = tk.Label(ventana_cobro, text="Cambio: $0.00", fg="red", font=("Arial", 14))
    cambio_label.pack(pady=10)

    def cobrar():
        try:
            pago = float(entrada_pago.get())
        except ValueError:
            cambio_label.config(text="Cantidad inválida", fg="red")
            return

        if pago < total:
            cambio_label.config(text="Pago insuficiente", fg="red")
            return

        cambio = pago - total
        cambio_label.config(text=f"Cambio: ${cambio:.2f}", fg="green")

        # === GUARDAR EN BASE DE DATOS ===
        try:
            conn = ConexionBaseDeDatos()
            cursor = conn.cursor()

            # Insertar en tabla 'ventas'
            from datetime import datetime
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO Ventas (Fecha_Hora, Total, ID_Cliente) VALUES (?, ?, ?)", (fecha, total, cliente_id))
            venta_id = cursor.lastrowid

            # Insertar detalle y actualizar stock
            for codigo, datos in productos_agregados.items():
                precio = datos["precio"]
                cantidad = datos["cantidad"]
                subtotal = cantidad * precio
                cursor.execute("INSERT INTO Detalle_Ventas (ID_Venta, ID_Producto, cantidad, Precio_Ud, Subtotal) VALUES (?, ?, ?, ?, ?)",
                               (venta_id, codigo, cantidad, precio, subtotal))

                cursor.execute("UPDATE Productos SET Cantidad = Cantidad - ? WHERE Codigo_Barras = ?", (cantidad, codigo))

            conn.commit()
            conn.close()
            messagebox.showinfo("Venta Registrada", f"Venta registrada correctamente. Cambio: ${cambio:.2f}")
            ventana_cobro.destroy()
            root.destroy()  # cerrar y reiniciar para nueva venta
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")

    tk.Button(ventana_cobro, text="Cobrar", command=cobrar, bg="green", fg="white").pack(pady=5)
