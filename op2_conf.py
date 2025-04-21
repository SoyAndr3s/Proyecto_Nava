import tkinter as tk
from tkinter import messagebox
import sqlite3

def configuracion():
    from config import obtener_configuracion, actualizar_configuracion
    
    config_window = tk.Toplevel()
    config_window.geometry("360x160")
    config_window.title("Configuración de Usuario")

    usuario_actual, clave_actual, modo_actual = obtener_configuracion()

    groupboxConfig = tk.LabelFrame(config_window, text="Cambio de Usuario-Clave")
    groupboxConfig.grid(column=0, row=0, padx=10, pady=10)
    
    tk.Label(groupboxConfig, text="Usuario:").grid(row=0, column=0, padx=10, pady=5)
    entry_usuario = tk.Entry(groupboxConfig)
    entry_usuario.insert(0, usuario_actual)
    entry_usuario.grid(column=1, row=0, padx=10, pady=5)
    
    tk.Label(groupboxConfig, text="Clave:").grid(row=1, column=0, padx=10, pady=5)
    entry_clave = tk.Entry(groupboxConfig, show="*")
    entry_clave.insert(0, clave_actual)
    entry_clave.grid(column=1, row=1, padx=10, pady=5)
    
    groupboxModo = tk.LabelFrame(config_window, text="Cambio de Modo")
    groupboxModo.grid(column=1, row=0, padx=10, pady=10)
    
    modo_var = tk.StringVar(value=modo_actual)
    tk.Radiobutton(groupboxModo, text="Dark", variable=modo_var, value="dark").pack()
    tk.Radiobutton(groupboxModo, text="Light", variable=modo_var, value="light").pack()
    tk.Radiobutton(groupboxModo, text="System", variable=modo_var, value="system").pack()
    
    def guardar_config():
        actualizar_configuracion(entry_usuario.get(), entry_clave.get(), modo_var.get())

    btn_guardar = tk.Button(config_window, text="Guardar", command=guardar_config)
    btn_guardar.grid(column=0, row=1, padx=10, pady=10)
