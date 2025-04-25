import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import ConexionBaseDeDatos

def reporte_venta():
    ventana = tk.Toplevel()
    ventana.title("Reportes")
    ventana.geometry("500x400")

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True)

    # ==== TAB 1: VENTAS REALIZADAS ====
    frame_ventas = tk.Frame(notebook)
    notebook.add(frame_ventas, text="Ventas Realizadas")

    columnas_ventas = ("ID", "Fecha", "Total", "Cliente")
    tree_ventas = ttk.Treeview(frame_ventas, columns=columnas_ventas, show="headings")
    for col in columnas_ventas:
        tree_ventas.heading(col, text=col)
        tree_ventas.column(col, anchor="center", width=100 if col != "Fecha" else 150)
    tree_ventas.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_ventas():
        try:
            conn = ConexionBaseDeDatos()
            cursor = conn.cursor()
            query = """
                SELECT v.id_Venta, v.Fecha_Hora, v.total, c.nombre 
                FROM ventas v
                LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                ORDER BY v.Fecha_Hora DESC
            """
            cursor.execute(query)
            filas = cursor.fetchall()
            for row in filas:
                tree_ventas.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las ventas:\n{e}")

    cargar_ventas()

    # ==== TAB 2: COMPRAS REALIZADAS ====
    frame_compras = tk.Frame(notebook)
    notebook.add(frame_compras, text="Compras Realizadas")

    columnas_compras = ("ID", "Fecha", "Proveedor", "Producto", "Cantidad", "Costo")
    tree_compras = ttk.Treeview(frame_compras, columns=columnas_compras, show="headings")
    for col in columnas_compras:
        tree_compras.heading(col, text=col)
        tree_compras.column(col, anchor="center", width=100 if col != "Producto" else 150)
    tree_compras.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_compras():
        try:
            conn = ConexionBaseDeDatos()
            cursor = conn.cursor()
            query = """
                SELECT dc.ID_Compra, c.Fecha_Hora, p.nombre, dc.ID_Producto, dc.Cantidad, dc.Precio_Ud
                FROM detalle_compras dc
                JOIN compras c ON dc.ID_Compra = c.ID_Compra
                LEFT JOIN Proveedores p ON c.id_proveedor = p.id_proveedor
                ORDER BY c.Fecha_Hora DESC
            """
            cursor.execute(query)
            filas = cursor.fetchall()
            for row in filas:
                tree_compras.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las compras:\n{e}")

    cargar_compras()
