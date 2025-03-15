import tkinter as tk
from config import obtener_configuracion, verificar_login

# Ventana de Login
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

frame_login = tk.Frame(login_window, padx=20, pady=20)
frame_login.pack(expand=True)

tk.Label(frame_login, text="Usuario:").grid(row=0, column=0, pady=5)
e_user = tk.Entry(frame_login)
e_user.grid(row=0, column=1, pady=5)

tk.Label(frame_login, text="Clave:").grid(row=1, column=0, pady=5)
e_password = tk.Entry(frame_login, show="*")
e_password.grid(row=1, column=1, pady=5)

btn_Ingresar = tk.Button(frame_login, text="Ingresar", width=10, command=lambda: verificar_login(e_user, e_password, login_window))
btn_Ingresar.grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()